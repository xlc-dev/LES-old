from calendar import day_name
from math import floor

from sqlmodel import Session

from app.utils import unix_to_hour

from app.core.models.household_model import HouseholdRead
from app.core.models.energyflow_model import EnergyFlowRead
from app.core.models.appliance_model import (
    ApplianceRead,
    ApplianceDays,
    ApplianceTimeDaily,
    ApplianceTimeDailyUpdate,
    ApplianceTimeNoEnergyDaily,
    ApplianceTimeNoEnergyDailyUpdate,
)

from app.core.crud.appliance_crud import (
    appliance_time_daily_crud,
    appliance_time_no_energy_daily_crud,
)


def plan_with_energy(
    session: Session,
    appliance: ApplianceRead,
    hour: int,
    appliance_bitmap_plan: ApplianceTimeDaily,
) -> None:
    appliance_duration = appliance.duration
    if (24 - hour - appliance_duration) >= 0:
        appliance_duration_bit = 2**appliance_duration - 1 << int(
            24 - hour - appliance_duration
        )
    else:
        appliance_duration_bit = 2**appliance_duration - 1 >> int(
            hour + appliance_duration - 24
        )
    if not appliance_bitmap_plan:
        if not appliance_bitmap_plan.bitmap_plan:
            new_bitmap_window = (
                appliance_duration_bit | appliance_bitmap_plan.bitmap_plan
            )
    else:
        new_bitmap_window = appliance_duration_bit

    new_appliance_time_daily = ApplianceTimeDailyUpdate(
        day=appliance_bitmap_plan.day,
        bitmap_plan=new_bitmap_window,
    )
    appliance_time_daily_crud.update(
        session=session,
        db_obj=appliance_bitmap_plan,
        obj_in=new_appliance_time_daily,
    )


def plan_no_energy(
    session: Session,
    appliance: ApplianceRead,
    unix: int,
    appliance_no_energy_bitmap_plan: ApplianceTimeNoEnergyDaily,
) -> None:
    hour = unix_to_hour(unix)
    appliance_duration = appliance.duration

    if (24 - hour - appliance_duration) >= 0:
        appliance_duration_bit = 2**appliance_duration - 1 << int(
            24 - hour - appliance_duration
        )
    else:
        appliance_duration_bit = 2**appliance_duration - 1 >> int(
            hour + appliance_duration - 24
        )
    if not appliance_no_energy_bitmap_plan.bitmap_plan:
        new_bitmap_window = appliance_duration_bit
    else:
        new_bitmap_window = (
            appliance_duration_bit
            | appliance_no_energy_bitmap_plan.bitmap_plan
        )
    new_appliance_time_no_energy_daily = ApplianceTimeNoEnergyDailyUpdate(
        day=appliance_no_energy_bitmap_plan.day,
        bitmap_plan=new_bitmap_window,
    )
    appliance_time_no_energy_daily_crud.update(
        session=session,
        db_obj=appliance_no_energy_bitmap_plan,
        obj_in=new_appliance_time_no_energy_daily,
    )


def update_energy(
    session: Session,
    appliance: ApplianceRead,
    old_hour: int,
    has_energy: bool,
    new_hour: int,
    gets_energy: bool,
    appliance_bitmap_plan: ApplianceTimeDaily | None = None,
    appliance_no_energy_bitmap_plan: ApplianceTimeNoEnergyDaily | None = None,
) -> None:
    appliance_duration = appliance.duration
    if appliance_bitmap_plan is not None:
        day = appliance_bitmap_plan.day
    elif appliance_no_energy_bitmap_plan is not None:
        day = appliance_no_energy_bitmap_plan.day
    else:
        print(
            "Both appliance_bitmap_plan and \
                appliance_no_energy_bitmap_plan are empty, \
                which shouldn't be possible."
        )
    if (24 - old_hour - appliance_duration) >= 0:
        appliance_duration_bit_old = 2**appliance_duration - 1 << int(
            24 - old_hour - appliance_duration
        )
    else:
        appliance_duration_bit_old = 2**appliance_duration - 1 >> int(
            old_hour + appliance_duration - 24
        )

    if (24 - new_hour - appliance_duration) >= 0:
        appliance_duration_bit_new = 2**appliance_duration - 1 << int(
            24 - new_hour - appliance_duration
        )
    else:
        appliance_duration_bit_new = 2**appliance_duration - 1 >> int(
            new_hour + appliance_duration - 24
        )

    if has_energy:
        if gets_energy:  # Had energy and gets energy
            if appliance_bitmap_plan is not None:
                new_bitmap_window = (
                    appliance_bitmap_plan.bitmap_plan
                    | appliance_duration_bit_new ^ appliance_duration_bit_old
                )
        else:  # Had energy but won't get energy
            if appliance_bitmap_plan is not None:
                new_bitmap_window = (
                    appliance_bitmap_plan.bitmap_plan
                    ^ appliance_duration_bit_old
                )
            if appliance_no_energy_bitmap_plan is not None:
                new_bitmap_window_no_energy = (
                    appliance_no_energy_bitmap_plan.bitmap_plan
                    | appliance_duration_bit_new
                )
    else:
        if gets_energy:  # Had no energy but gets energy
            if appliance_bitmap_plan is not None:
                new_bitmap_window = (
                    appliance_bitmap_plan.bitmap_plan
                    | appliance_duration_bit_new
                )
            if appliance_no_energy_bitmap_plan is not None:
                new_bitmap_window_no_energy = (
                    appliance_no_energy_bitmap_plan.bitmap_plan
                    ^ appliance_duration_bit_old
                )
        else:  # Had no energy and gets no energy
            if appliance_no_energy_bitmap_plan is not None:
                new_bitmap_window_no_energy = (
                    appliance_no_energy_bitmap_plan.bitmap_plan
                    | appliance_duration_bit_new ^ appliance_duration_bit_old
                )

    if has_energy or gets_energy:
        new_appliance_time_daily = ApplianceTimeDailyUpdate(
            day=day,
            bitmap_plan=new_bitmap_window,
        )
        if appliance_bitmap_plan is not None:
            appliance_time_daily_crud.update(
                session=session,
                db_obj=appliance_bitmap_plan,
                obj_in=new_appliance_time_daily,
            )
    if has_energy is False or gets_energy is False:
        new_appliance_time_no_energy_daily = ApplianceTimeNoEnergyDailyUpdate(
            day=day,
            bitmap_plan=new_bitmap_window_no_energy,
        )
        if appliance_no_energy_bitmap_plan is not None:
            appliance_time_no_energy_daily_crud.update(
                session=session,
                db_obj=appliance_no_energy_bitmap_plan,
                obj_in=new_appliance_time_no_energy_daily,
            )


def get_potential_energy(
    household: HouseholdRead, energy_used: float, solar_produced: float
) -> float:
    energy_usage_factor = 7000  # Hardcoded, is total energy in energyflow
    solar_panels_factor = 25  # Hardcoded, amount of solar panels in energyflow
    return (
        solar_produced * household.solar_panels / solar_panels_factor
        - energy_used * 0.8 * household.energy_usage / energy_usage_factor
    )


def check_appliance_time(
    appliance: ApplianceRead,
    unix: int,
    appliance_bitmap_plan: ApplianceTimeDaily,
    appliance_no_energy_bitmap_plan: ApplianceTimeNoEnergyDaily,
    has_energy: bool,
) -> bool:
    hour = unix_to_hour(unix)
    for window in appliance.appliance_windows:
        current_day = day_name[(floor(unix / 86400 + 4) % 7)]
        day_string = ApplianceDays(current_day).name
        day_number = ApplianceDays[day_string.upper()].value
        if window.day == day_number:
            bitmap_window = window.bitmap_window

    appliance_duration = appliance.duration
    appliance_duration_bit = 2**appliance.duration - 1
    if 24 - hour - appliance_duration >= 0:
        current_time_window = bitmap_window >> int(
            24 - hour - appliance_duration
        )
    else:
        current_time_window = bitmap_window << int(
            hour + appliance_duration - 24
        )
    if appliance_duration_bit & current_time_window:
        return False
    if has_energy:
        if not appliance_bitmap_plan.bitmap_plan:
            return True
        if 24 - hour - appliance_duration >= 0:
            current_appliance_task = appliance_bitmap_plan.bitmap_plan >> int(
                24 - hour - appliance_duration
            )
        else:
            current_appliance_task = appliance_bitmap_plan.bitmap_plan << int(
                hour + appliance_duration - 24
            )
        if appliance_duration_bit & current_appliance_task:
            return False
    else:
        if not appliance_no_energy_bitmap_plan.bitmap_plan:
            return True
        if 24 - hour - appliance_duration >= 0:
            current_appliance_no_energy_task = (
                appliance_no_energy_bitmap_plan.bitmap_plan
                >> int(24 - hour - appliance_duration)
            )
        else:
            current_appliance_no_energy_task = (
                appliance_no_energy_bitmap_plan.bitmap_plan
                << int(hour + appliance_duration - 24)
            )

        if appliance_duration_bit & current_appliance_no_energy_task:
            return False
    return True


def cost_static() -> float:
    return 0.25


def energy_efficiency_day(
    session: Session,
    energy_flow: list[EnergyFlowRead],
    planning: list[HouseholdRead],
    day: int,
    date: int,
):
    # Hardcoded
    solar_panels_factor = 25
    buy_price = 0.4
    sell_price = 0.1

    solar_energy_produced = [0.0 for x in range(24)]
    solar_energy_used_self = [0.0 for x in range(24)]
    solar_energy_used_total = [0.0 for x in range(24)]
    household_energy_available = [0.0 for x in range(24)]
    previous_total_usage = [0.0 for x in range(24)]
    current_total_usage = [0.0 for x in range(24)]

    total_panels = 0
    for household in planning:
        total_panels += household.solar_panels
        for hour in range(24):
            household_energy_available[hour] = (
                energy_flow[hour].solar_produced
                * household.solar_panels
                / solar_panels_factor
            )
        for appliance in household.appliances:
            appliance_bitmap_plan = (
                appliance_time_daily_crud.get_appliance_time_daily(
                    session=session,
                    appliance_id=appliance.id,
                    day=day,
                )
            )
            if appliance_bitmap_plan is None:
                continue
            if appliance_bitmap_plan.bitmap_plan is None:
                continue
            bitmap = "{0:24b}".format(appliance_bitmap_plan.bitmap_plan)
            for hour in range(24):
                if bitmap[hour] == "1":
                    solar_energy_used_total[hour] += (
                        appliance.power / appliance.duration
                    )
                    solar_energy_used_self[hour] += min(
                        appliance.power / appliance.duration,
                        household_energy_available[hour],
                    )
                    household_energy_available[hour] -= min(
                        appliance.power / appliance.duration,
                        household_energy_available[hour],
                    )

    for hour in range(24):
        solar_energy_produced[hour] = (
            energy_flow[hour].solar_produced
            * total_panels
            / solar_panels_factor
        )
        previous_total_usage[hour] = min(
            solar_energy_used_self[hour], solar_energy_produced[hour]
        )
        current_total_usage[hour] = min(
            solar_energy_used_total[hour], solar_energy_produced[hour]
        )

    if sum(solar_energy_produced) > 0:
        previous_efficiency = sum(previous_total_usage) / sum(
            solar_energy_produced
        )
        current_efficiency = sum(current_total_usage) / sum(
            solar_energy_produced
        )
    else:
        previous_efficiency = 1
        current_efficiency = 1

    if sum(previous_total_usage) == 0:
        previous_efficiency = 1
    if sum(current_total_usage) == 0:
        current_efficiency = 1

    energy_price = buy_price * previous_efficiency + sell_price * (
        1 - previous_efficiency
    )
    cost_savings = (sum(current_total_usage) - sum(previous_total_usage)) * (
        buy_price - energy_price
    )

    return previous_efficiency, current_efficiency, energy_price, cost_savings
