"""This router, just like the seed_router, is a special router.

Here are all the simulation endpoints to run the simulation.

The general idea is that the frontend would call the /load-data endpoint to get
all the possible options for the simulation. Then once the user has selected
the options through the stepper, the frontend would call the /start endpoint to
start the simulation.

Once the simulation is done because the algorithm isn't finding any more
improvements, or the user has stopped the simulation, the frontend would call
the /stop endpoint to get the results of the simulation. Where you could
download the results as a CSV file, and see the results in a graph.
"""
import random
from math import exp

from fastapi import APIRouter, Depends, Body, status

from sqlmodel import Session, SQLModel

from app.utils import Logger, get_session

from app.core.models.costmodel_model import CostModelRead
from app.core.models.twinworld_model import TwinWorldRead
from app.core.models.algorithm_model import AlgorithmRead
from app.core.models.household_model import HouseholdRead
from app.core.models.energyflow_model import EnergyFlowRead
from app.core.models.appliance_model import (
    ApplianceTimeDailyRead,
    ApplianceTimeNoEnergyDailyRead,
)

from app.core.crud.costmodel_crud import costmodel_crud
from app.core.crud.twinworld_crud import twinworld_crud
from app.core.crud.algorithm_crud import algorithm_crud
from app.core.crud.household_crud import household_crud
from app.core.crud.energyflow_crud import energyflow_crud
from app.core.crud.appliance_crud import (
    appliance_time_daily_crud,
    appliance_time_no_energy_daily_crud,
)

from app.plan_helpers import (
    plan_with_energy,
    plan_no_energy,
    get_potential_energy,
    check_appliance_time,
    unix_to_hour,
    update_energy,
    energy_efficiency_day,
)

router = APIRouter()


class SimulationData(SQLModel):
    twin_world: list[TwinWorldRead]
    cost_model: list[CostModelRead]
    algorithm: list[AlgorithmRead]


class ApplianceTime(SQLModel):
    appliance_time_daily: list[ApplianceTimeDailyRead]
    appliance_time_no_energy_daily: list[ApplianceTimeNoEnergyDailyRead]


@router.get("/load-data", response_model=SimulationData)
async def get_data(*, session: Session = Depends(get_session)):
    "Get all possible options for the simulation"
    twinworlds = twinworld_crud.get_multi(session=session)
    costmodels = costmodel_crud.get_multi(session=session)
    algorithms = algorithm_crud.get_multi(session=session)

    return SimulationData(
        twin_world=twinworlds, cost_model=costmodels, algorithm=algorithms
    )


@router.post("/start", response_model=list[HouseholdRead])
async def start(
    *,
    algorithm_id: int = Body(...),
    twinworld_id: int = Body(...),
    costmodel_id: int = Body(...),
    session: Session = Depends(get_session),
):
    "Start the simulation with the given parameters from /get-data"
    twinworld = twinworld_crud.get(session=session, id=twinworld_id)

    if not twinworld:
        Logger.exception(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No twinworld found with id: {twinworld_id}",
        )

    costmodel = costmodel_crud.get(session=session, id=costmodel_id)

    if not costmodel:
        Logger.exception(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No costmodel found with id: {costmodel_id}",
        )

    algorithm = algorithm_crud.get(session=session, id=algorithm_id)

    if not algorithm:
        Logger.exception(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No algorithm found with id: {algorithm_id}",
        )

    results = household_crud.get_by_twinworld_sorted_solar_panels(
        session=session, id=twinworld.id
    )

    if not results:
        Logger.exception(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No results found for twinworld with id: {twinworld_id}",
        )

    return results


@router.post("/stop")
async def stop(*, session: Session = Depends(get_session)):
    return {"message": "Simulation ended"}


@router.post("/plan_simulated_annealing", response_model=ApplianceTime)
async def plan_simulated_annealing(
    *, planning: list[HouseholdRead], session: Session = Depends(get_session)
):
    max_temperature = 10000
    solar_panels_factor = 25

    energyflow_data = energyflow_crud.get_by_solar_produced(session=session)
    energyflow_data_sim = energyflow_crud.get_by_solar_produced_sim(session=session)
    amount_of_households = len(planning)
    start_date, end_date = energyflow_crud.get_start_end_date(session=session)
    start_date, end_date = start_date.timestamp, end_date.timestamp
    days_in_planning = (end_date - start_date) // 86400

    # Precompute energyflow_day for each day outside the loop
    energyflow_day_per_day = {}
    for date in range(start_date, end_date, 86400):
        energyflow_day = [
            el
            for el in energyflow_data
            if (date <= el.timestamp and el.timestamp < date + 3600 * 24)
        ]
        energyflow_day_per_day[date] = energyflow_day

    results = [[0.0 for _ in range(4)] for _ in range(days_in_planning + 1)]

    # Plan: for the loop
    # First we do one day at a time, chronologically
    # This day needs to be initialized with the right helper variables

    # Then we plan all of the devices one household at a time
    # Ordering is done by most solar panels first
    # with the result of each house useing their own energy first
    # Only later on it's allowed to use energy from other houses

    for date in range(start_date, end_date, 86400):
        day_number_in_planning = (date - start_date) // 86400 + 1
        print(int(day_number_in_planning))
        energyflow_day = [
            el
            for el in energyflow_data
            if (date <= el.timestamp and el.timestamp < date + 3600 * 24)
        ]  # only check the current day for energy flow

        household_energy = [
            [0.0 for x in range(amount_of_households)] for y in range(24)
        ]  # the available excess energy to be used for scheduling loads
        total_available_energy = 0.0

        for household_idx, household in enumerate(planning, start=0):
            if household.solar_panels <= 0:
                continue
            for energyflow_day_information_init in energyflow_day:
                hour = unix_to_hour(
                    energyflow_day_information_init.timestamp
                )
                potential_energy = get_potential_energy(
                    household,
                    energyflow_day_information_init.energy_used,
                    energyflow_day_information_init.solar_produced,
                )
                household_energy[hour][household_idx] = potential_energy
                total_available_energy += potential_energy

        for household_idx, household in enumerate(planning, start=0):
            if total_available_energy <= 0:
                break

            for appliance in household.appliances:
                usage = appliance.daily_usage  # misschien niet nodig
                appliance_bitmap_plan = (
                    appliance_time_daily_crud.get_appliance_time_daily(
                        session=session,
                        appliance_id=appliance.id,
                        day=day_number_in_planning,
                    )
                )
                if not appliance_bitmap_plan:  # error testing
                    print(appliance.id, day_number_in_planning)
                appliance_no_energy_bitmap_plan = appliance_time_no_energy_daily_crud.get_appliance_time_no_energy_daily(  # noqa: E501
                    session=session,
                    appliance_id=appliance.id,
                    day=day_number_in_planning,
                )
                if not appliance_no_energy_bitmap_plan:  # error testing
                    print(appliance.id, day_number_in_planning)
                while usage > (1 - random.random()):
                    plannedin = False

                    for energyflow_day_information in energyflow_day:
                        unix = energyflow_day_information.timestamp
                        hour = unix_to_hour(unix)
                        if plannedin is True:
                            break
                        if household_energy[hour][household_idx] < 0:
                            continue
                        if (
                            check_appliance_time(
                                appliance,
                                unix,
                                appliance_bitmap_plan,
                                appliance_no_energy_bitmap_plan,
                                True,
                            )
                            is False
                        ):
                            continue

                        plan_with_energy(
                            session, appliance, hour, appliance_bitmap_plan
                        )
                        for i in range(appliance.duration):
                            energy_used = min(
                                household_energy[hour][household_idx],
                                appliance.power / appliance.duration,
                            )
                            total_available_energy -= energy_used
                            household_energy[hour][
                                household_idx
                            ] -= energy_used
                        plannedin = True
                        usage -= 1
                        break

                    if plannedin is True:
                        continue

                    for i in range(24):
                        if plannedin is True:
                            break
                        currenttime = date + 3600 * i
                        if (
                            check_appliance_time(
                                appliance,
                                currenttime,
                                appliance_bitmap_plan,
                                appliance_no_energy_bitmap_plan,
                                False,
                            )
                            is False
                        ):
                            continue
                        plan_no_energy(
                            session,
                            appliance,
                            currenttime,
                            appliance_no_energy_bitmap_plan,
                        )
                        plannedin = True
                        usage -= 1

                    if plannedin is False:
                        #     print("Not planned in", appliance, date)
                        usage = 0
        current_used = [0.0 for x in range(24)]
        current_used_new = [0.0 for x in range(24)]
        solar_produced = [0.0 for x in range(24)]
        current_available = [0.0 for x in range(24)]
        total_panels = 0

        energyflow_day_sim: list[EnergyFlowRead] = [
            el
            for el in energyflow_data_sim
            if (date <= el.timestamp and el.timestamp < date + 3600 * 24)
        ]  # only check the current day for energy flow

        for household in planning:
            total_panels += household.solar_panels
            for appliance in household.appliances:
                appliance_bitmap_plan = (
                    appliance_time_daily_crud.get_appliance_time_daily(
                        session=session,
                        appliance_id=appliance.id,
                        day=day_number_in_planning,
                    )
                )
                if appliance_bitmap_plan is None:
                    continue
                bitmap = "{0:24b}".format(
                    int(appliance_bitmap_plan.bitmap_plan)
                )
                for hour in range(24):
                    if bitmap[hour] == "1":
                        current_used[hour] += (
                            appliance.power / appliance.duration
                        )
        for hour in range(24):
            solar_produced[hour] = (
                energyflow_day_sim[hour].solar_produced
                * total_panels
                / solar_panels_factor
            )
            current_available[hour] = (
                solar_produced[hour] - current_used[hour]
            )
        temp_result = [0.0 for x in range(4)]
        (
            temp_result[0],
            temp_result[1],
            temp_result[2],
            temp_result[3],
        ) = energy_efficiency_day(
            session,
            energyflow_day_sim,
            planning,
            day_number_in_planning,
            date,
        )
        for iter in range(4):
            if temp_result[iter] > results[day_number_in_planning][iter]:
                results[day_number_in_planning][0] = temp_result[iter]

        if sum(current_used) <= 0:
            print("nothing planned in")
            continue

        for temperature in range(max_temperature):
            if all(value <= 0 for value in current_available):
                break
            effective_temperature = 1 - (temperature / max_temperature)
            household_random = random.randint(0, amount_of_households)
            for household_idx, household in enumerate(planning, start=0):
                if household_idx == household_random:
                    if len(household.appliances) == 0:
                        continue
                    elif len(household.appliances) == 1:
                        appliance_random = 0
                    else:
                        appliance_random = random.randint(
                            0, len(household.appliances) - 1
                        )
                    for appliance_idx, appliance in enumerate(
                        household.appliances, start=0
                    ):
                        if appliance_idx == appliance_random:
                            appliance_new_starttime = (
                                date + random.randint(0, 23) * 3600
                            )
                            has_energy = random.choice([True, False])
                            gets_energy = random.choice([True, False])
                            if has_energy or gets_energy:
                                appliance_bitmap_plan = appliance_time_daily_crud.get_appliance_time_daily(  # noqa: E501
                                    session=session,
                                    appliance_id=appliance.id,
                                    day=day_number_in_planning,
                                )
                                if appliance_bitmap_plan is None:
                                    continue
                                if (
                                    appliance_bitmap_plan.bitmap_plan
                                    is None
                                ):
                                    continue
                            if has_energy is False or gets_energy is False:
                                appliance_bitmap_plan_no_energy = appliance_time_no_energy_daily_crud.get_appliance_time_no_energy_daily(  # noqa: E501
                                    session=session,
                                    appliance_id=appliance.id,
                                    day=day_number_in_planning,
                                )
                                if appliance_bitmap_plan_no_energy is None:
                                    continue
                                if (
                                    appliance_bitmap_plan_no_energy.bitmap_plan  # noqa: E501
                                    is None
                                ):
                                    continue

                            if has_energy:
                                appliance_frequency = (
                                    bin(
                                        appliance_bitmap_plan.bitmap_plan
                                    ).count("1")
                                    // appliance.duration
                                )
                            else:
                                appliance_frequency = (
                                    bin(
                                        appliance_bitmap_plan_no_energy.bitmap_plan  # noqa: E501
                                    ).count("1")
                                    // appliance.duration
                                )
                            # print(appliance_frequency)
                            if appliance_frequency == 0:
                                continue
                            appliance_old = random.randint(
                                0, appliance_frequency - 1
                            )
                            if has_energy:
                                bitmap = "{0:24b}".format(
                                    appliance_bitmap_plan.bitmap_plan
                                )
                            else:
                                bitmap = "{0:24b}".format(
                                    appliance_bitmap_plan_no_energy.bitmap_plan  # noqa: E501
                                )
                            ones_in_bitmap = 0

                            for position in range(24):
                                if bitmap[position] == "1":
                                    ones_in_bitmap += 1
                                    if (
                                        ones_in_bitmap
                                        == appliance_old
                                        * appliance.duration
                                        + 1
                                    ):
                                        appliance_old_starttime = position

                            if (
                                check_appliance_time(
                                    appliance,
                                    appliance_new_starttime,
                                    appliance_bitmap_plan,
                                    appliance_no_energy_bitmap_plan,
                                    gets_energy,
                                )
                                is False
                            ):
                                continue

                            current_used_new = current_used.copy()

                            for duration in range(appliance.duration):
                                if has_energy:
                                    if (
                                        appliance_old_starttime + duration
                                        < 24
                                    ):
                                        current_used_new[
                                            appliance_old_starttime
                                            + duration
                                        ] -= (
                                            appliance.power
                                            / appliance.duration
                                        )
                                if gets_energy:
                                    if (
                                        appliance_new_starttime + duration
                                        < 24
                                    ):
                                        current_used_new[
                                            appliance_new_starttime
                                            + duration
                                        ] += (
                                            appliance.power
                                            / appliance.duration
                                        )

                            improvement = 0.0
                            for hour in range(24):
                                improvement += min(
                                    solar_produced[hour],
                                    current_used_new[hour],
                                ) - min(
                                    solar_produced[hour],
                                    current_used[hour],
                                )

                            if (
                                improvement > 0
                                or exp(
                                    3 * improvement / effective_temperature
                                )
                                < random.random()
                            ):
                                update_energy(
                                    session,
                                    appliance,
                                    appliance_old_starttime,
                                    has_energy,
                                    appliance_new_starttime,
                                    gets_energy,
                                    appliance_bitmap_plan,
                                    appliance_bitmap_plan_no_energy,
                                )
                                # print("Geupdate")
        (
            temp_result[0],
            temp_result[1],
            temp_result[2],
            temp_result[3],
        ) = energy_efficiency_day(
            session,
            energyflow_day_sim,
            planning,
            day_number_in_planning,
            date,
        )
        for iter in range(4):
            if temp_result[iter] > results[day_number_in_planning][iter]:
                results[day_number_in_planning][iter] = temp_result[iter]

    initial_planning_energy = appliance_time_daily_crud.get_multi(
        session=session, limit=10
    )
    initial_planning_no_energy = appliance_time_no_energy_daily_crud.get_multi(
        session=session, limit=10
    )
    print(results)
    # TODO: stuur ook results nog mee misschien?
    return ApplianceTime(
        appliance_time_daily=initial_planning_energy,
        appliance_time_no_energy_daily=initial_planning_no_energy,
    )


@router.post("/plan", response_model=ApplianceTime)
async def plan(
    *, planning: list[HouseholdRead], session: Session = Depends(get_session)
):
    if (
        appliance_time_daily_crud.get_non_empty_timewindow(session=session)
        is None
    ):  # niet de goede verwijzing meer, moeten een andere checken
        random.seed(27)
        energyflow_data = energyflow_crud.get_by_solar_produced(
            session=session
        )  # gets all the energy flow in (unix, energy used, solar produced)`
        energyflow_data_sim = energyflow_crud.get_by_solar_produced_sim(
            session=session
        )
        amount_of_households = household_crud.count_households(
            session=session
        )  # gets the amount of households in the planning
        start_date, end_date = energyflow_crud.get_start_end_date(
            session=session
        )
        start_date, end_date = start_date.timestamp, end_date.timestamp
        days_in_planning = (end_date - start_date) // 86400
        results = [
            [0.0 for x in range(4)] for y in range(days_in_planning + 1)
        ]

        # Plan: for the loop
        # First we do one day at a time, chronologically
        # This day needs to be initialized with the right helper variables

        # Then we plan all of the devices one household at a time
        # Ordering is done by most solar panels first
        # with the result of each house useing their own energy first
        # Only later on it's allowed to use energy from other houses

        for date in range(start_date, end_date, 86400):
            day_number_in_planning = (date - start_date) // 86400 + 1
            print(int(day_number_in_planning))
            energyflow_day = [
                el
                for el in energyflow_data
                if (date <= el.timestamp and el.timestamp < date + 3600 * 24)
            ]  # only check the current day for energy flow
            energyflow_day = sorted(
                energyflow_day,
                key=lambda energyflow: energyflow.timestamp,
                reverse=True,
            )  # sort it with the goal of filling the sunnier times first
            household_energy = [
                [0.0 for x in range(amount_of_households)] for y in range(24)
            ]  # the available excess energy to be used for scheduling loads
            total_available_energy = 0.0

            for household_idx, household in enumerate(planning, start=0):
                if household.solar_panels <= 0:
                    continue

                for energyflow_day_information_init in energyflow_day:
                    hour = unix_to_hour(
                        energyflow_day_information_init.timestamp
                    )
                    potential_energy = get_potential_energy(
                        household,
                        energyflow_day_information_init.energy_used,
                        energyflow_day_information_init.solar_produced,
                    )
                    household_energy[hour][household_idx] = potential_energy
                    total_available_energy += potential_energy

            for household_idx, household in enumerate(planning, start=0):
                if total_available_energy <= 0:
                    break

                for appliance in household.appliances:
                    usage = appliance.daily_usage  # misschien niet nodig
                    appliance_bitmap_plan = (
                        appliance_time_daily_crud.get_appliance_time_daily(
                            session=session,
                            appliance_id=appliance.id,
                            day=day_number_in_planning,
                        )
                    )
                    if not appliance_bitmap_plan:  # error testing
                        print(appliance.id, day_number_in_planning)
                    appliance_no_energy_bitmap_plan = appliance_time_no_energy_daily_crud.get_appliance_time_no_energy_daily(  # noqa: E501
                        session=session,
                        appliance_id=appliance.id,
                        day=day_number_in_planning,
                    )
                    while usage > (1 - random.random()):
                        plannedin = False

                        for energyflow_day_information in energyflow_day:
                            unix = energyflow_day_information.timestamp
                            hour = unix_to_hour(unix)
                            if plannedin is True:
                                break
                            if household_energy[hour][household_idx] < 0:
                                continue
                            if (
                                check_appliance_time(
                                    appliance,
                                    unix,
                                    appliance_bitmap_plan,
                                    appliance_no_energy_bitmap_plan,
                                    True,
                                )
                                is False
                            ):
                                continue

                            plan_with_energy(
                                session, appliance, hour, appliance_bitmap_plan
                            )
                            for i in range(appliance.duration):
                                energy_used = min(
                                    household_energy[hour][household_idx],
                                    appliance.power / appliance.duration,
                                )
                                total_available_energy -= energy_used
                                household_energy[hour][
                                    household_idx
                                ] -= energy_used
                            plannedin = True
                            usage -= 1
                            break

                        if plannedin is True:
                            continue

                        for i in range(24):
                            if plannedin is True:
                                break
                            currenttime = date + 3600 * i
                            if (
                                check_appliance_time(
                                    appliance,
                                    currenttime,
                                    appliance_bitmap_plan,
                                    appliance_no_energy_bitmap_plan,
                                    False,
                                )
                                is False
                            ):
                                continue
                            plan_no_energy(
                                session,
                                appliance,
                                currenttime,
                                appliance_no_energy_bitmap_plan,
                            )
                            plannedin = True
                            usage -= 1

                        if plannedin is False:
                            #     print("Not planned in", appliance, date)
                            usage = 0
            energyflow_day_sim: list[EnergyFlowRead] = [
                el
                for el in energyflow_data_sim
                if (date <= el.timestamp and el.timestamp < date + 3600 * 24)
            ]  # only check the current day for energy flow
            temp_result = [0.0 for x in range(4)]
            (
                temp_result[0],
                temp_result[1],
                temp_result[2],
                temp_result[3],
            ) = energy_efficiency_day(
                session,
                energyflow_day_sim,
                planning,
                day_number_in_planning,
                date,
            )
            for iter in range(4):
                if temp_result[iter] > results[day_number_in_planning][iter]:
                    results[day_number_in_planning][iter] = temp_result[iter]

    initial_planning_energy = appliance_time_daily_crud.get_multi(
        session=session, limit=10
    )
    initial_planning_no_energy = appliance_time_no_energy_daily_crud.get_multi(
        session=session, limit=10
    )
    # TODO: Stuur results nog mee?
    print(results)
    return ApplianceTime(
        appliance_time_daily=initial_planning_energy,
        appliance_time_no_energy_daily=initial_planning_no_energy,
    )
