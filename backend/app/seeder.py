from typing import Optional, Dict
import math
import random

from scipy.stats import norm
from fastapi import APIRouter, Depends, status

from sqlmodel import Session

from app.utils import (
    Logger,
    get_session,
    create_db_and_tables,
    delete_db_and_tables,
)

from app.core.models import (
    appliance_model,
    household_model,
    twinworld_model,
)

from app.core.models.appliance_model import ApplianceType, ApplianceDays


router = APIRouter()


def add_appliance_to_session(session: Session, appliance):
    "Abstraction for adding an appliance to a session"
    if appliance is not None:
        session.add(appliance)
        session.flush()
        for day in ApplianceDays:
            timewindow = create_timewindow(day, appliance.id)
            session.add(timewindow)


def create_timewindow(
    day: ApplianceDays, appliance_id: int
) -> appliance_model.ApplianceTimeWindow:
    """Creates a time window for an appliance on a given day.

    The bitmap is a 24 bit integer where each bit represents an hour of the day

    :param day:
        Day of the week
    :param appliance_id:
        Id of the appliance the time window belongs to
    """
    bitmap = 0

    if ApplianceType.STOVE.value == appliance_id:
        # Set time window from 5-8 for the stove
        timewindow = appliance_model.ApplianceTimeWindow(
            day=day,
            bitmap_window=0b11110000,
            appliance_id=appliance_id,
        )
        return timewindow

    if ApplianceType.ELECTRIC_VEHICLE.value == appliance_id and day not in [
        ApplianceDays.SATURDAY,
        ApplianceDays.SUNDAY,
    ]:
        # Restrict hours 8-17 (8 am to 5 pm) for electric vehicle on weekdays
        restricted_hours = 0b111111111111111111111111 & ~(0b111111111111 << 8)
        bitmap |= restricted_hours

    # Random time window generation
    num_windows = random.randint(1, 100)
    amount = 1 if num_windows < 90 else 2 if num_windows < 99 else 3

    for _ in range(amount):
        start_hour = random.randint(0, 23)
        end_hour = random.randint(
            start_hour + 1, 24
        )  # Ensuring end is after start

        # Check if there is already a window in the given range
        existing_bits = bitmap & ((1 << end_hour) - 1)
        if existing_bits & ((1 << start_hour) - 1) != 0:
            start_hour = (existing_bits.bit_length() - 1) % 24

        # Set the bits in the range to 1
        window_mask = ((1 << (end_hour - start_hour)) - 1) << start_hour
        bitmap |= window_mask

    timewindow = appliance_model.ApplianceTimeWindow(
        day=day,
        bitmap_window=bitmap,
        appliance_id=appliance_id,
    )

    return timewindow


def create_appliance(
    name: ApplianceType,
    household_id: int,
    household_size: int,
    duration: int,
    availability: Dict[str, float],
    frequency: Dict[str, float],
    energy_pattern: float,
    usage_random: float,
    usage_multi: float,
    usage_addition: float,
) -> Optional[appliance_model.Appliance]:
    """Creates an appliance with the given parameters.

    daily_usage: Amount of times the appliance is used per day
    energy_usage: Amount of energy used per usage

    :param name:
        Name of the appliance
    :param household_id:
        Id of the household the appliance belongs to
    :param household_size:
        Size of the household the appliance belongs to
    :param duration:
        Duration of the appliance being used
    :param availability:
        Probability of the appliance being available in the household
    :param frequency:
        Frequency of the appliance being used per day
    :param energy_pattern:
        Energy pattern of the household
    :param usage_random:
        Random factor for energy usage
    :param usage_multi:
        Multiplier for random factor
    :param usage_addition:
        Addition to random factor
    """
    daily_usage = 0.0
    energy_usage = 0.0

    if random.random() < availability.get(str(household_size), 0):
        daily_usage = round(
            frequency.get(str(household_size), 0) * energy_pattern, 3
        )
        energy_usage = round(usage_random * usage_multi + usage_addition, 1)

        appliance = appliance_model.Appliance(
            name=name,
            power=energy_usage,
            duration=duration,
            daily_usage=daily_usage,
            household_id=household_id,
        )

        return appliance

    return None


def create_dishwasher(
    size: int, inv_norm: float, household_id: int
) -> Optional[appliance_model.Appliance]:
    available = {
        "1": 0.47,
        "2": 0.76,
        "3": 0.81,
        "4": 0.89,
        "5": 0.83,
    }

    frequency = {
        "1": 0.51,
        "2": 0.7,
        "3": 0.84,
        "4": 0.96,
        "5": 1.1,
    }

    rand = random.random()

    return create_appliance(
        ApplianceType.DISHWASHER,
        household_id,
        size,
        1 if rand < 0.5 else 2,
        available,
        frequency,
        inv_norm,
        rand,
        6,
        4,
    )


def create_washingmachine(
    size: int, inv_norm: float, household_id: int
) -> Optional[appliance_model.Appliance]:
    available = {
        "1": 0.94,
        "2": 1,
        "3": 1,
        "4": 1,
        "5": 0.97,
    }

    frequency = {
        "1": 0.52,
        "2": 0.68,
        "3": 0.93,
        "4": 1.24,
        "5": 1.4,
    }

    rand = random.random()

    return create_appliance(
        ApplianceType.WASHING_MACHINE,
        household_id,
        size,
        2 if rand < 0.5 else 3,
        available,
        frequency,
        inv_norm,
        rand,
        7,
        5,
    )


def create_tumbledryer(
    size: int, inv_norm: float, household_id: int
) -> Optional[appliance_model.Appliance]:
    available = {
        "1": 0.63,
        "2": 0.63,
        "3": 0.63,
        "4": 0.63,
        "5": 0.63,
    }

    frequency = {
        "1": 0.52,
        "2": 0.68,
        "3": 0.93,
        "4": 1.24,
        "5": 1.4,
    }

    rand = random.random()

    return create_appliance(
        ApplianceType.TUMBLE_DRYER,
        household_id,
        size,
        1 if rand < 0.5 else 2,
        available,
        frequency,
        inv_norm,
        rand,
        2,
        1,
    )


def create_electricvehicle(
    size: int, household_id: int
) -> Optional[appliance_model.Appliance]:
    available = {
        "1": 0.2,
        "2": 0.2,
        "3": 0.2,
        "4": 0.2,
        "5": 0.2,
    }

    frequency = {
        "1": 1.0,
        "2": 1.0,
        "3": 1.0,
        "4": 1.0,
        "5": 1.0,
    }

    rand = random.random()

    return create_appliance(
        ApplianceType.ELECTRIC_VEHICLE,
        household_id,
        size,
        4 if rand < 0.5 else 5,
        available,
        frequency,
        random.random() * 0.8 + 0.2,
        rand,
        10,
        50,
    )


def create_stove(
    size: int, household_id: int
) -> Optional[appliance_model.Appliance]:
    available = {
        "1": 0.49,
        "2": 0.49,
        "3": 0.49,
        "4": 0.49,
        "5": 0.49,
    }

    frequency = {
        "1": 1.0,
        "2": 1.0,
        "3": 1.0,
        "4": 1.0,
        "5": 1.0,
    }

    rand = random.random()

    return create_appliance(
        ApplianceType.STOVE,
        household_id,
        size,
        1 if rand < 0.5 else 2,
        available,
        frequency,
        random.random() * 0.15 + 0.85,
        rand,
        5,
        2,
    )


def create_household(
    name: str, twinworld_id: int, inv_norm: float
) -> household_model.Household:
    # Map for household size to energy usage
    default_energy_usage = {
        "1": 1600,
        "2": 2500,
        "3": 3400,
        "4": 4300,
        "5": 5000,
    }

    # Calculate household size
    randint = random.randint(1, 100)
    household_size = 5
    if randint <= 43:
        household_size = 1
    elif randint <= 67:
        household_size = 2
    elif randint <= 81:
        household_size = 3
    elif randint <= 95:
        household_size = 4

    # Calculate energy usage
    total_energy_usage = int(
        round(inv_norm * default_energy_usage[str(household_size)], 0)
    )

    # Calculate solar panels
    solar_panels = 0
    if random.random() < 0.38:
        inv_norm_solar = norm.ppf(random.random(), loc=1, scale=0.1)
        solar_panels = math.ceil(3 + 2 * household_size * inv_norm_solar)

    # TODO: transform
    solar_yield = solar_panels * 340

    household = household_model.Household(
        name=name,
        size=household_size,
        energy_usage=total_energy_usage,
        solar_panels=solar_panels,
        solar_yield=solar_yield,
        twinworld_id=twinworld_id,
    )

    return household


@router.post("/", status_code=status.HTTP_201_CREATED)
def seed(session: Session = Depends(get_session)) -> None:
    "Seeds the database with initial data for the twinworld"
    delete_db_and_tables()
    create_db_and_tables()
    random.seed()

    # TODO: name + description
    twinworld_1 = twinworld_model.TwinWorld(
        name="TwinWorld 1",
        description="A world with a twin",
    )

    session.add(twinworld_1)

    twinworld_2 = twinworld_model.TwinWorld(
        name="TwinWorld 2",
        description="A world with a twin",
    )

    session.add(twinworld_2)

    for i in range(1, 101):
        inv_norm = norm.ppf(random.random(), loc=1, scale=0.2)

        # Min inv cap is 0.3
        if inv_norm < 0.3:
            inv_norm = 0.3

        if random.random() < 0.75:
            household = create_household(f"Household {i}", 1, inv_norm)
        else:
            household = create_household(f"Household {i}", 2, inv_norm)

        session.add(household)
        session.flush()

        dishwasher = create_dishwasher(household.size, inv_norm, household.id)
        vehicle = create_electricvehicle(household.size, household.id)
        stove = create_stove(household.size, household.id)
        washingmachine = create_washingmachine(
            household.size, inv_norm, household.id
        )
        session.flush()

        add_appliance_to_session(session, vehicle)
        add_appliance_to_session(session, dishwasher)
        add_appliance_to_session(session, stove)
        add_appliance_to_session(session, washingmachine)

        if washingmachine is not None:
            tumbledryer = create_tumbledryer(
                household.size, inv_norm, household.id
            )
            add_appliance_to_session(session, tumbledryer)

    try:
        session.commit()
    except Exception:
        session.rollback()

        Logger.exception(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not add seed data",
        )
