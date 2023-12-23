from math import floor
from sqlmodel import Session

from calendar import day_name

from app.core.models.household_model import HouseholdRead
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
    hour: int,
    appliance_no_energy_bitmap_plan: ApplianceTimeNoEnergyDaily,
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
    hour = unix / 3600 % 24
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


def unix_to_hour(unix: int) -> int:
    return unix // 3600 % 24
