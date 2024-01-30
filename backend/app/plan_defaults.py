from math import exp
from random import random, randint, choice

from fastapi import status

from app.utils import Logger, SECONDS_IN_DAY, unix_to_hour
from app.plan_helpers import (
    check_appliance_time,
    plan_energy,
    update_energy,
)

from app.core.models.household_model import HouseholdRead
from app.core.models.energyflow_model import EnergyFlowRead
from app.core.models.algorithm_model import AlgorithmRead
from app.core.models.appliance_model import (
    ApplianceRead,
    ApplianceTimeDaily,
)


def cost_default(
    *,
    buy_consumer: float,
    sell_consumer: float,
    ratio: float,
) -> float:
    return buy_consumer * ratio + sell_consumer * (1 - ratio)


def plan_greedy(
    *,
    date: int,
    household_idx: int,
    days_in_planning: int,
    day_number_in_planning: int,
    total_available_energy: float,
    household_energy: list[list[float]],
    appliance: ApplianceRead,
    appliance_time: list[ApplianceTimeDaily],
    energyflow_day: list[EnergyFlowRead],
    total_start_date: int,
) -> tuple[list[ApplianceTimeDaily], float, list[list[float]]]:
    usage = appliance.daily_usage

    index = days_in_planning * (appliance.id - 1) + day_number_in_planning - 1

    if appliance_time[index].day != day_number_in_planning:
        Logger.exception(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Day {day_number_in_planning} not found",
        )

    while usage > (1 - random()):
        plannedin = False

        bitmap_energy = appliance_time[index].bitmap_plan_energy
        bitmap_no_energy = appliance_time[index].bitmap_plan_no_energy

        if total_available_energy > 0:
            for energyflow_day_information in energyflow_day:
                unix = energyflow_day_information.timestamp
                hour = unix_to_hour(unix)
                if plannedin or household_energy[hour][household_idx] < 0:
                    break

                if not check_appliance_time(
                    appliance=appliance,
                    unix=unix,
                    appliance_bitmap_plan=bitmap_energy,
                ):
                    continue

                appliance_time[index].bitmap_plan_energy = plan_energy(
                    hour=hour,
                    appliance_duration=appliance.duration,
                    appliance_bitmap_plan=bitmap_energy,
                )

                for i in range(appliance.duration):
                    energy_used = min(
                        household_energy[hour][household_idx],
                        appliance.power / appliance.duration,
                    )
                    total_available_energy -= energy_used
                    household_energy[hour][household_idx] -= energy_used

                plannedin = True
                usage -= 1
                break

        if not plannedin:
            for i in range(24):
                currenttime = (
                    total_start_date
                    + (day_number_in_planning - 1) * SECONDS_IN_DAY
                    + i * 3600
                )
                if not check_appliance_time(
                    appliance=appliance,
                    unix=currenttime,
                    appliance_bitmap_plan=bitmap_no_energy,
                ):
                    continue

                appliance_time[index].bitmap_plan_no_energy = plan_energy(
                    hour=unix_to_hour(currenttime),
                    appliance_duration=appliance.duration,
                    appliance_bitmap_plan=bitmap_no_energy,
                )
                plannedin = True
                usage -= 1
                break

        if not plannedin:
            usage = 0  # Appliance not plannedin

    return (
        appliance_time,
        total_available_energy,
        household_energy,
    )


def plan_simulated_annealing(
    *,
    date: int,
    days_in_planning: int,
    day_number_in_planning: int,
    length_planning: int,
    current_available: list[float],
    solar_produced: list[float],
    current_used: list[float],
    algorithm: AlgorithmRead,
    household_planning: list[HouseholdRead],
    appliance_time: list[ApplianceTimeDaily],
) -> None:
    for temperature in range(algorithm.max_temperature):  # type: ignore # noqa: E501
        if all(value <= 0 for value in current_available):
            break

        effective_temperature = 1 - (
            temperature / algorithm.max_temperature  # type: ignore  # noqa: E501
        )
        household_random = randint(0, length_planning - 1)
        selected_household = household_planning[household_random]

        if len(selected_household.appliances) == 0:
            continue

        selected_appliance = choice(selected_household.appliances)
        appliance_new_starttime = date + randint(0, 23) * 3600
        has_energy = choice([True, False])
        gets_energy = choice([True, False])

        index = (
            days_in_planning * (selected_appliance.id - 1)
            + day_number_in_planning
        )

        bitmap_energy = appliance_time[index].bitmap_plan_energy
        bitmap_no_energy = appliance_time[index].bitmap_plan_no_energy

        # Calculate the current appliance schedule and frequency
        bitmap = "{0:024b}".format(
            bitmap_energy if has_energy else bitmap_no_energy
        )

        appliance_frequency = bitmap.count("1") // selected_appliance.duration

        if appliance_frequency == 0:
            continue

        appliance_timeslot = randint(0, appliance_frequency - 1)

        # Find the old scheduled hour
        ones_in_bitmap = 0
        appliance_old_starttime = None
        for position, bit in enumerate(bitmap):
            if bit == "1":
                ones_in_bitmap += 1
                if (
                    ones_in_bitmap
                    == appliance_timeslot * selected_appliance.duration + 1
                ):
                    appliance_old_starttime = position
                    break

        if appliance_old_starttime is None:
            continue

        if not check_appliance_time(
            appliance=selected_appliance,
            unix=appliance_new_starttime,
            appliance_bitmap_plan=bitmap_energy
            if gets_energy
            else bitmap_no_energy,
        ):
            continue

        current_used_new = current_used.copy()

        # Update the usage calculation
        for duration in range(selected_appliance.duration):
            old_start_hour = (appliance_old_starttime + duration) % 24
            new_start_hour = (
                unix_to_hour(appliance_new_starttime) + duration
            ) % 24

            if has_energy:
                current_used_new[old_start_hour] -= (
                    selected_appliance.power / selected_appliance.duration
                )

            if gets_energy:
                current_used_new[new_start_hour] += (
                    selected_appliance.power / selected_appliance.duration
                )

        improvement = sum(
            min(solar_produced[hour], current_used_new[hour])
            - min(solar_produced[hour], current_used[hour])
            for hour in range(24)
        )

        if (
            improvement > 0
            or exp(3 * improvement / effective_temperature) < random()
        ):
            (
                appliance_time[index].bitmap_plan_energy,
                appliance_time[index].bitmap_plan_no_energy,
            ) = update_energy(
                old_hour=appliance_old_starttime,
                new_hour=unix_to_hour(appliance_new_starttime),
                has_energy=has_energy,
                gets_energy=gets_energy,
                appliance=selected_appliance,
                appliance_bitmap_plan_energy=bitmap_energy,
                appliance_bitmap_plan_no_energy=bitmap_no_energy,
            )
