"""The functions that help the default plan functions.

Contains the cost function, and the possible algorithms.
"""

from calendar import day_name
from math import floor

from fastapi import status

from sqlmodel import Session, SQLModel

from app.config import settings
from app.utils import Logger, SECONDS_IN_DAY, HOURS_IN_WEEK, unix_to_hour

from app.core.models.household_model import HouseholdRead
from app.core.models.energyflow_model import (
    EnergyFlowRead,
    EnergyFlowUploadRead,
)
from app.core.models.costmodel_model import CostModelRead
from app.core.models.twinworld_model import TwinWorldRead
from app.core.models.algorithm_model import AlgorithmRead
from app.core.models.appliance_model import (
    ApplianceRead,
    ApplianceDays,
    ApplianceTimeDaily,
    ApplianceTimeDailyRead,
)

from app.core.crud.appliance_crud import appliance_time_daily_crud
from app.core.crud.energyflow_crud import energyflow_crud


class SelectedOptions(SQLModel):
    twinworld: TwinWorldRead
    costmodel: CostModelRead
    algorithm: AlgorithmRead
    energyflow: EnergyFlowUploadRead
    households: list[HouseholdRead]


class SimulationData(SQLModel):
    twinworld: list[TwinWorldRead]
    costmodel: list[CostModelRead]
    algorithm: list[AlgorithmRead]
    energyflow: list[EnergyFlowUploadRead]


class SelectedModelsInput(SQLModel):
    chunkoffset: int
    households: list[HouseholdRead]
    costmodel: CostModelRead
    algorithm: AlgorithmRead
    twinworld: TwinWorldRead
    energyflow: EnergyFlowUploadRead


class SelectedModelsOutput(SQLModel):
    timedaily: list[ApplianceTimeDailyRead]
    results: list[list[float]]
    days_in_planning: int
    start_date: int
    end_date: int


def _calculate_appliance_duration_bit(duration: int, hour: int) -> int:
    """Internal function that transforms the appliance information into a
    bitmapwindow
    """

    shift = 24 - hour - duration
    return (
        (2**duration - 1) << shift
        if shift >= 0
        else (2**duration - 1) >> -shift
    )


def _get_potential_energy(
    household: HouseholdRead,
    energy_used: float,
    solar_produced: float,
    solar_panels_factor: int,
    energy_usage_factor: int,
) -> float:
    """Internal function that calculates the potential solar energy used for a
    household

    20% of the energy usage in a normal household is used for the appliances
    that are being planned in here.
    """

    return (
        solar_produced * household.solar_panels / solar_panels_factor
        - energy_used * 0.8 * household.energy_usage / energy_usage_factor
    )


def _energy_efficiency_day(
    day: int,
    date: int,
    solar_panels_factor: int,
    energy_flow: list[EnergyFlowRead],
    planning: list[HouseholdRead],
    appliance_bitmap_plan: list[ApplianceTimeDaily],
    costmodel: CostModelRead,
) -> tuple[float, float, float, float, float]:
    """Internal function that calculates the energy efficiency of a day.

    This is done by checking for each house how much energy they produce and
    use themselves at a certain time, and how much of the available solar
    energy in total gets used at a certain time.

    The self efficiency is how much energy all of the houses combined use of
    their own generated solar power.

    The total efficiency is how much energy all of the houses combined use of
    all the available generated solar power.
    """

    total_panels = sum(household.solar_panels for household in planning)
    solar_energy_produced = [
        ef.solar_produced * total_panels / solar_panels_factor
        for ef in energy_flow
    ]

    solar_energy_used_self = [0.0] * 24
    solar_energy_used_total = [0.0] * 24

    for household in planning:
        household_energy_available = [
            ef.solar_produced * household.solar_panels / solar_panels_factor
            for ef in energy_flow
        ]

        for appliance in household.appliances:
            bitmap = f"{appliance_bitmap_plan[appliance.id - 1].bitmap_plan_energy:024b}"  # noqa: E501

            for hour, bit in enumerate(bitmap):
                if bit == "1":
                    power_per_hour = appliance.power / appliance.duration
                    used_energy = min(
                        power_per_hour, household_energy_available[hour]
                    )
                    solar_energy_used_total[hour] += power_per_hour
                    solar_energy_used_self[hour] += used_energy
                    household_energy_available[hour] -= used_energy

    previous_total_usage = [
        min(used_self, produced)
        for used_self, produced in zip(
            solar_energy_used_self, solar_energy_produced
        )
    ]
    current_total_usage = [
        min(used_total, produced)
        for used_total, produced in zip(
            solar_energy_used_total, solar_energy_produced
        )
    ]

    sum_produced = sum(solar_energy_produced)

    previous_efficiency = (
        sum(previous_total_usage) / sum_produced if sum_produced > 0 else 0
    )
    current_efficiency = (
        sum(current_total_usage) / sum_produced if sum_produced > 0 else 0
    )

    ratio = previous_efficiency

    if costmodel.name == "Fixed Price":
        ratio = costmodel.fixed_price_ratio  # type: ignore

    algo = costmodel.algorithm

    if costmodel.name != "Fixed Price" and costmodel.name != "TEMO":
        print(algo)
        algo = algo.replace("cost_default():", f"""{algo}(
        buy_consumer={costmodel.price_network_buy_consumer},
        sell_consumer={costmodel.price_network_sell_consumer},
        ratio={ratio})""")

        energy_price_code_with_params = algo
        print(energy_price_code_with_params)
    else:
        algo = algo.rstrip("()")
        # Adding parameters to the code
        energy_price_code_with_params = f"""{algo}(
        buy_consumer={costmodel.price_network_buy_consumer},
        sell_consumer={costmodel.price_network_sell_consumer},
        ratio={ratio})"""

    # Execute the modified code using eval
    from app.plan_defaults import cost_default  # noqa: F401

    energy_price = eval(energy_price_code_with_params)

    if sum(solar_energy_used_self) <= 0:
        energy_price = costmodel.price_network_buy_consumer

    cost_savings = (sum(current_total_usage) - sum(previous_total_usage)) * (
        costmodel.price_network_buy_consumer - energy_price
    )

    return (
        previous_efficiency,
        current_efficiency,
        energy_price,
        cost_savings,
        sum_produced,
    )


def plan_energy(
    hour: int, appliance_duration: int, appliance_bitmap_plan: int
) -> int:
    "Creates the updated bitmap window with the new usage added in."

    appliance_duration_bit = _calculate_appliance_duration_bit(
        duration=appliance_duration, hour=hour
    )

    return appliance_duration_bit | appliance_bitmap_plan


def update_energy(
    old_hour: int,
    new_hour: int,
    has_energy: bool,
    gets_energy: bool,
    appliance: ApplianceRead,
    appliance_bitmap_plan_energy: int,
    appliance_bitmap_plan_no_energy: int,
) -> tuple[int, int]:
    "Updates both bitmap windows with the newly planned in appliance."

    appliance_duration_bit_old = _calculate_appliance_duration_bit(
        appliance.duration, old_hour
    )
    appliance_duration_bit_new = _calculate_appliance_duration_bit(
        appliance.duration, new_hour
    )

    new_bitmap_window_energy = appliance_bitmap_plan_energy
    new_bitmap_window_no_energy = appliance_bitmap_plan_no_energy

    if has_energy:
        new_bitmap_window_energy ^= appliance_duration_bit_old
    else:
        new_bitmap_window_no_energy ^= appliance_duration_bit_old

    if gets_energy:
        new_bitmap_window_energy |= appliance_duration_bit_new
    else:
        new_bitmap_window_no_energy |= appliance_duration_bit_new

    return new_bitmap_window_energy, new_bitmap_window_no_energy


def check_appliance_time(
    appliance: ApplianceRead,
    unix: int,
    appliance_bitmap_plan: int,
) -> bool:
    """Checks whether an appliance can be planned in at a certain time.

    This is done by retrieving the correctly daily bitmap window and then
    comparing that to the new planned in time. Also the old planning is
    checked with the newly planned in time.
    """

    hour = unix_to_hour(unix)
    current_day = day_name[(floor(unix / SECONDS_IN_DAY + 3) % 7)]
    day_number = ApplianceDays[current_day.upper()].value

    bitmap_window = next(
        (
            window.bitmap_window
            for window in appliance.appliance_windows
            if window.day == day_number
        ),
        None,
    )

    appliance_duration_bit = 2**appliance.duration - 1
    shift = 24 - hour - appliance.duration
    current_time_window = (
        appliance_duration_bit << shift
        if shift >= 0
        else appliance_duration_bit >> -shift
    )

    if (bitmap_window & current_time_window) != current_time_window:
        return False

    if current_time_window & appliance_bitmap_plan:
        return False

    return True


def setup_planning(
    *, session: Session, planning: SelectedModelsInput
) -> tuple[
    int,
    int,
    int,
    int,
    int,
    int,
    list[EnergyFlowRead],
    list[EnergyFlowRead],
    list[ApplianceTimeDaily],
    list[HouseholdRead],
    list[list[float]],
]:
    """Retrieves all the data for starting the planning.

    This contains the following data:
    days_in_chunk, the timeframe that will be planned in, in this loop
    days_in_planning, the current day that will be planned in
    length_planning, the total timeframe that will be planned in
    start_date, the start date of this chunk
    end_date, the end date of this chunk
    total_start_date, the start date of the total planning
    energyflow_data_sim, all of the energyflows in this chunk
    energyflow_data, the energyflows where the solar power is greater than 0
    appliance_time, all of the appliance time windows
    household_planning, all of the households available in this planning
    results, the results of this chunk
    """

    energyflow_data = energyflow_crud.get_by_solar_produced(
        session=session,
        limit=HOURS_IN_WEEK,
        offset=planning.chunkoffset * 24,
    )

    if len(energyflow_data) == 0:
        Logger.exception(
            status_code=status.HTTP_204_NO_CONTENT,
            detail="Energyflow data not found",
        )

    energyflow_data_sim = energyflow_crud.get_all_sorted_by_timestamp(
        session=session,
        limit=HOURS_IN_WEEK,
        offset=planning.chunkoffset * 24,
        id=planning.energyflow.id,
    )

    appliance_time = appliance_time_daily_crud.get_multi(session=session)

    total_start_date, total_end_date = energyflow_crud.get_start_end_date(
        session=session,
        id=planning.energyflow.id,
    )

    total_start_date = total_start_date.timestamp
    total_end_date = total_end_date.timestamp

    start_date = energyflow_data_sim[0].timestamp
    end_date = energyflow_data_sim[-1].timestamp - SECONDS_IN_DAY + 3600

    days_in_chunk = (end_date - start_date) // SECONDS_IN_DAY + 1

    days_in_planning = (
        total_end_date - total_start_date
    ) // SECONDS_IN_DAY + 1

    results = [[0.0 for _ in range(7)] for _ in range(days_in_chunk)]

    household_planning = planning.households
    length_planning = len(household_planning)

    return (  # type: ignore
        days_in_chunk,
        days_in_planning,
        length_planning,
        start_date,
        end_date,
        total_start_date,
        energyflow_data_sim,
        energyflow_data,
        appliance_time,
        household_planning,
        results,
    )


def loop_helpers(
    *,
    start_date: int,
    total_start_date: int,
    day_iterator: int,
    length_planning: int,
    household_planning: list[HouseholdRead],
    energyflow_data: list[EnergyFlowRead],
    energyflow: EnergyFlowUploadRead,
    twinworld: TwinWorldRead,
) -> tuple[int, list[EnergyFlowRead], list[list[float]], float, int]:
    """All of the helper variables in the loop.

    This results in the following data:
    date, the current time in unix for this day
    energyflow_day, the energy flows for this day where solar power > 0
    household_energy, how much energy each household has available for usage
    total_available_energy, how much energy is available in total
    day_number_in_planning, the current day in planning
    """

    day_number_in_planning = (
        start_date - total_start_date
    ) // SECONDS_IN_DAY + day_iterator

    if settings.development:
        print(day_number_in_planning)

    date = start_date + day_number_in_planning * SECONDS_IN_DAY
    energyflow_day = [
        el
        for el in energyflow_data
        if (el.timestamp - start_date) // SECONDS_IN_DAY == day_iterator - 1
    ]

    # Initialize data structures for the current day
    household_energy = [
        [0.0 for _ in range(length_planning)] for _ in range(24)
    ]
    total_available_energy = 0.0

    for household_idx, household in enumerate(household_planning):
        if household.solar_panels <= 0:
            continue
        for flow in energyflow_day:
            hour = unix_to_hour(flow.timestamp)
            potential_energy = _get_potential_energy(
                household=household,
                energy_used=flow.energy_used,
                solar_produced=flow.solar_produced,
                solar_panels_factor=energyflow.solar_panels_factor,
                energy_usage_factor=energyflow.energy_usage_factor,
            )

            household_energy[hour][household_idx] += potential_energy
            total_available_energy += potential_energy

    return (
        date,
        energyflow_day,
        household_energy,
        total_available_energy,
        day_number_in_planning,
    )


def write_results(
    *,
    date: int,
    day_iterator: int,
    day_number_in_planning: int,
    results: list[list[float]],
    energyflow: EnergyFlowUploadRead,
    twinworld: TwinWorldRead,
    costmodel: CostModelRead,
    appliance_time: list[ApplianceTimeDaily],
    energyflow_day_sim: list[EnergyFlowRead],
    household_planning: list[HouseholdRead],
) -> list[list[float]]:
    """Returns the results of a certain in the planning.

    This uses the helper function _energy_efficiency_day to determine the
    efficiency, and then puts it into an array which is send back.
    """

    current_day_appliance = [
        el for el in appliance_time if el.day == day_number_in_planning
    ]

    temp_result = _energy_efficiency_day(
        day=day_number_in_planning,
        date=date,
        solar_panels_factor=energyflow.solar_panels_factor,
        energy_flow=energyflow_day_sim,
        planning=household_planning,
        appliance_bitmap_plan=current_day_appliance,
        costmodel=costmodel,
    )

    if day_iterator == 0:
        results[day_iterator - 1][5] = (
            temp_result[0] - results[day_iterator - 1][0]
        ) * temp_result[4]
        results[day_iterator - 1][6] = (
            temp_result[1] - results[day_iterator - 1][1]
        ) * temp_result[4]
    else:
        results[day_iterator - 1][5] = (
            temp_result[0] - results[day_iterator - 1][0]
        ) * temp_result[4] + results[day_iterator - 2][0]
        results[day_iterator - 1][6] = (
            temp_result[1] - results[day_iterator - 1][1]
        ) * temp_result[4] + results[day_iterator - 2][1]

    for iter in range(5):
        if temp_result[iter] > results[day_iterator - 1][iter]:
            results[day_iterator - 1][iter] = temp_result[iter]

    return results


def create_results(
    *,
    total_start_date: int,
    day_number_in_planning: int,
    energyflow_data_sim: list[EnergyFlowRead],
    household_planning: list[HouseholdRead],
    energyflow: EnergyFlowUploadRead,
) -> tuple[list[float], list[float], list[float], list[EnergyFlowRead]]:
    """Creates the helper variables for determining the results.

    The following variables are created:
    solar_produced, the amount of energy produced by all households in a day
    current_used, the amount of energy used by all households for SL's
    current_available, the amount of energy still available for all households
    energyflow_day_sim, all the energy flows for the day
    """
    # Process to calculate energy efficiency for the day
    current_used, solar_produced, current_available = (
        [0.0] * 24,
        [0.0] * 24,
        [0.0] * 24,
    )

    total_panels = sum(
        household.solar_panels for household in household_planning
    )

    # Energy flow simulation for the current day
    energyflow_day_sim = [
        el
        for el in energyflow_data_sim
        if day_number_in_planning
        == ((el.timestamp - total_start_date) // SECONDS_IN_DAY + 1)
    ]

    for hour in range(24):
        solar_produced[hour] = (
            sum(
                el.solar_produced
                for el in energyflow_day_sim
                if unix_to_hour(el.timestamp) == hour
            )
            * total_panels
            / energyflow.solar_panels_factor
        )

        current_available[hour] = solar_produced[hour] - current_used[hour]

    return (
        solar_produced,
        current_used,
        current_available,
        energyflow_day_sim,
    )
