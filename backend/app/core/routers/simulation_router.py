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

from sqlmodel import Session

from app.utils import Logger, get_session, SECONDS_IN_DAY

from app.core.crud.costmodel_crud import costmodel_crud
from app.core.crud.twinworld_crud import twinworld_crud
from app.core.crud.algorithm_crud import algorithm_crud
from app.core.crud.household_crud import household_crud

from app.plan_helpers import (
    SimulationData,
    SelectedOptions,
    SelectedModelsInput,
    SelectedModelsOutput,
    plan_energy,
    get_potential_energy,
    check_appliance_time,
    unix_to_hour,
    update_energy,
    energy_efficiency_day,
    setup_planning,
    loop_helpers,
)

router = APIRouter()


@router.get("/load-data", response_model=SimulationData)
async def get_data(*, session: Session = Depends(get_session)):
    "Get all possible options for the simulation"
    twinworlds = twinworld_crud.get_multi(session=session)
    costmodels = costmodel_crud.get_multi(session=session)
    algorithms = algorithm_crud.get_multi(session=session)

    return SimulationData(
        twinworld=twinworlds, costmodel=costmodels, algorithm=algorithms
    )


@router.post("/start", response_model=SelectedOptions)
async def start(
    *,
    algorithm_id: int = Body(...),
    twinworld_id: int = Body(...),
    costmodel_id: int = Body(...),
    session: Session = Depends(get_session),
) -> SelectedOptions:
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

    households = household_crud.get_by_twinworld_sorted_solar_panels(
        session=session, id=twinworld.id
    )

    if not households:
        Logger.exception(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No households found for twinworld with id: {twinworld_id}",  # noqa: E501
        )

    return SelectedOptions(
        twinworld=twinworld,
        costmodel=costmodel,
        algorithm=algorithm,
        households=households,
    )


@router.post("/stop")
async def stop(*, session: Session = Depends(get_session)):
    return {"message": "Simulation ended"}


@router.post("/plan", response_model=SelectedModelsOutput)
async def plan(
    *, planning: SelectedModelsInput, session: Session = Depends(get_session)
) -> SelectedModelsOutput:
    (
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
        energyflow_by_day,
    ) = setup_planning(session=session, planning=planning)

    for day_iterator in range(1, days_in_chunk + 1):
        (
            date,
            energyflow_day,
            household_energy,
            total_available_energy,
            day_number_in_planning,
        ) = loop_helpers(
            start_date=start_date,
            total_start_date=total_start_date,
            day_iterator=day_iterator,
            length_planning=length_planning,
            household_planning=household_planning,
            energyflow_data=energyflow_data,
            twinworld=planning.twinworld,
        )

        # Optimization of the appliance scheduling process
        for household_idx, household in enumerate(household_planning):
            for appliance in household.appliances:
                usage = appliance.daily_usage

                index = (
                    days_in_planning * (appliance.id - 1)
                    + day_number_in_planning
                    - 1
                )

                if appliance_time[index].day != day_number_in_planning:
                    Logger.exception(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Day {day_number_in_planning} not found",
                    )

                bitmap_energy = appliance_time[index].bitmap_plan_energy
                bitmap_no_energy = appliance_time[index].bitmap_plan_no_energy

                while usage > (1 - random.random()):
                    plannedin = False

                    if total_available_energy > 0:
                        for energyflow_day_information in energyflow_day:
                            unix = energyflow_day_information.timestamp
                            hour = unix_to_hour(unix)
                            if (
                                plannedin
                                or household_energy[hour][household_idx] < 0
                            ):
                                break

                            if not check_appliance_time(
                                appliance=appliance,
                                unix=unix,
                                has_energy=True,
                                appliance_bitmap_plan=bitmap_energy,
                            ):
                                continue

                            appliance_time[
                                index
                            ].bitmap_plan_energy = plan_energy(
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
                                household_energy[hour][
                                    household_idx
                                ] -= energy_used

                            plannedin = True
                            usage -= 1
                            break

                    if not plannedin:
                        for i in range(24):
                            currenttime = date + 3600 * i
                            if not check_appliance_time(
                                appliance=appliance,
                                unix=currenttime,
                                has_energy=False,
                                appliance_bitmap_plan=bitmap_no_energy,
                            ):
                                continue
                            appliance_time[
                                index
                            ].bitmap_plan_no_energy = plan_energy(
                                hour=unix_to_hour(currenttime),
                                appliance_duration=appliance.duration,
                                appliance_bitmap_plan=bitmap_no_energy,
                            )
                            plannedin = True
                            usage -= 1
                            break

                    if not plannedin:
                        usage = 0  # Appliance not planned

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
                / planning.twinworld.solar_panels_factor
            )

            current_available[hour] = solar_produced[hour] - current_used[hour]

        current_day_appliance = [
            el for el in appliance_time if el.day == day_number_in_planning
        ]

        # Update results based on energy efficiency of the day
        temp_result = energy_efficiency_day(
            day=day_number_in_planning,
            date=date,
            solar_panels_factor=planning.twinworld.solar_panels_factor,
            energy_flow=energyflow_day_sim,
            planning=household_planning,
            appliance_bitmap_plan=current_day_appliance,
            costmodel=planning.costmodel,
        )

        for iter in range(4):
            if temp_result[iter] > results[day_iterator - 1][iter]:
                results[day_iterator - 1][iter] = temp_result[iter]

        if total_available_energy <= 0:
            continue

        # Temperature-based optimization loop
        for temperature in range(planning.algorithm.max_temperature):
            if all(value <= 0 for value in current_available):
                break

            effective_temperature = 1 - (
                temperature / planning.algorithm.max_temperature
            )
            household_random = random.randint(0, length_planning - 1)
            selected_household = household_planning[household_random]

            if len(selected_household.appliances) == 0:
                continue

            selected_appliance = random.choice(selected_household.appliances)
            appliance_new_starttime = date + random.randint(0, 23) * 3600
            has_energy = random.choice([True, False])
            gets_energy = random.choice([True, False])

            index = (
                days_in_planning * (selected_appliance.id - 1)
                + day_number_in_planning
                - 1
            )

            # For some reason only 1 of the values becomes a tuple after a
            # while, this is a stupid hack to just get the first value in
            # the tuple so the program doesn't break (gigabrain moment).
            bitmap_no_energy = (
                bitmap_no_energy[0]
                if isinstance(bitmap_no_energy, tuple)
                else bitmap_no_energy
            )
            bitmap_energy = (
                bitmap_energy[0]
                if isinstance(bitmap_energy, tuple)
                else bitmap_energy
            )

            # Calculate the current appliance schedule and frequency
            bitmap = "{0:024b}".format(
                bitmap_energy if has_energy else bitmap_no_energy
            )

            appliance_frequency = (
                bitmap.count("1") // selected_appliance.duration
            )

            if appliance_frequency == 0:
                continue

            # Find the old scheduled hour
            ones_in_bitmap = 0
            appliance_old_starttime = None
            for position, bit in enumerate(bitmap):
                if bit == "1":
                    ones_in_bitmap += 1
                    if ones_in_bitmap == appliance_frequency:
                        appliance_old_starttime = position
                        break

            if appliance_old_starttime is None:
                continue

            if not check_appliance_time(
                appliance=selected_appliance,
                unix=appliance_new_starttime,
                has_energy=gets_energy,
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
                or exp(3 * improvement / effective_temperature)
                < random.random()
            ):
                appliance_time[index].bitmap_plan_energy,
                appliance_time[index].bitmap_plan_no_energy = update_energy(
                    old_hour=appliance_old_starttime,
                    new_hour=appliance_new_starttime,
                    has_energy=has_energy,
                    gets_energy=gets_energy,
                    appliance=selected_appliance,
                    appliance_bitmap_plan_energy=bitmap_energy,
                    appliance_bitmap_plan_no_energy=bitmap_no_energy,
                )

        current_day_appliance = [
            el for el in appliance_time if el.day == day_number_in_planning
        ]

        temp_result = energy_efficiency_day(
            day=day_number_in_planning,
            date=date,
            solar_panels_factor=planning.twinworld.solar_panels_factor,
            energy_flow=energyflow_day_sim,
            planning=household_planning,
            appliance_bitmap_plan=current_day_appliance,
            costmodel=planning.costmodel,
        )

        for iter in range(4):
            if temp_result[iter] > results[day_iterator - 1][iter]:
                results[day_iterator - 1][iter] = temp_result[iter]

    start_day = (start_date - total_start_date) // SECONDS_IN_DAY + 1

    time_daily = [
        el
        for el in appliance_time
        if el.day >= start_day and el.day < start_day + days_in_chunk
    ]

    return SelectedModelsOutput(
        results=results,
        timedaily=time_daily,
        start_date=start_date,
        end_date=end_date,
    )


# @router.post("/plan", response_model=ApplianceTime)
# async def plan(
#     *, planning: list[HouseholdRead], session: Session = Depends(get_session)
# ):
#     if (
#         appliance_time_daily_crud.get_non_empty_timewindow(session=session)
#         is None
#     ):  # niet de goede verwijzing meer, moeten een andere checken
#         random.seed(27)
#         energyflow_data = energyflow_crud.get_by_solar_produced(
#             session=session
#         )  # gets all the energy flow in (unix, energy used, solar produced)`
#         energyflow_data_sim = energyflow_crud.get_by_solar_produced_sim(
#             session=session
#         )
#         amount_of_households = household_crud.count_households(
#             session=session
#         )  # gets the amount of households in the planning
#         start_date, end_date = energyflow_crud.get_start_end_date(
#             session=session
#         )
#         start_date, end_date = start_date.timestamp, end_date.timestamp
#         days_in_planning = (end_date - start_date) // SECONDS_IN_DAY
#         results = [
#             [0.0 for x in range(4)] for y in range(days_in_planning + 1)
#         ]
#
#         # Plan: for the loop
#         # First we do one day at a time, chronologically
#         # This day needs to be initialized with the right helper variables
#
#         # Then we plan all of the devices one household at a time
#         # Ordering is done by most solar panels first
#         # with the result of each house useing their own energy first
#         # Only later on it's allowed to use energy from other houses
#
#         for date in range(start_date, end_date, SECONDS_IN_DAY):
#             day_number_in_planning = (date - start_date) // SECONDS_IN_DAY + 1
#             print(int(day_number_in_planning))
#             energyflow_day = [
#                 el
#                 for el in energyflow_data
#                 if (date <= el.timestamp and el.timestamp < date + 3600 * 24)
#             ]  # only check the current day for energy flow
#             energyflow_day = sorted(
#                 energyflow_day,
#                 key=lambda energyflow: energyflow.timestamp,
#                 reverse=True,
#             )  # sort it with the goal of filling the sunnier times first
#             household_energy = [
#                 [0.0 for x in range(amount_of_households)] for y in range(24)
#             ]  # the available excess energy to be used for scheduling loads
#             total_available_energy = 0.0
#
#             for household_idx, household in enumerate(planning, start=0):
#                 if household.solar_panels <= 0:
#                     continue
#
#                 for energyflow_day_information_init in energyflow_day:
#                     hour = unix_to_hour(
#                         energyflow_day_information_init.timestamp
#                     )
#                     potential_energy = get_potential_energy(
#                         household,
#                         energyflow_day_information_init.energy_used,
#                         energyflow_day_information_init.solar_produced,
#                     )
#                     household_energy[hour][household_idx] = potential_energy
#                     total_available_energy += potential_energy
#
#             for household_idx, household in enumerate(planning, start=0):
#                 if total_available_energy <= 0:
#                     break
#
#                 for appliance in household.appliances:
#                     usage = appliance.daily_usage  # misschien niet nodig
#                     appliance_bitmap_plan = (
#                         appliance_time_daily_crud.get_appliance_time_daily(
#                             session=session,
#                             appliance_id=appliance.id,
#                             day=day_number_in_planning,
#                         )
#                     )
#                     if not appliance_bitmap_plan:  # error testing
#                         print(appliance.id, day_number_in_planning)
#                     appliance_no_energy_bitmap_plan = appliance_time_no_energy_daily_crud.get_appliance_time_no_energy_daily(  # noqa: E501
#                         session=session,
#                         appliance_id=appliance.id,
#                         day=day_number_in_planning,
#                     )
#                     while usage > (1 - random.random()):
#                         plannedin = False
#
#                         for energyflow_day_information in energyflow_day:
#                             unix = energyflow_day_information.timestamp
#                             hour = unix_to_hour(unix)
#                             if plannedin is True:
#                                 break
#                             if household_energy[hour][household_idx] < 0:
#                                 continue
#                             if (
#                                 check_appliance_time(
#                                     appliance,
#                                     unix,
#                                     appliance_bitmap_plan,
#                                     appliance_no_energy_bitmap_plan,
#                                     True,
#                                 )
#                                 is False
#                             ):
#                                 continue
#
#                             plan_with_energy(
#                                 session, appliance, hour, appliance_bitmap_plan
#                             )
#                             for i in range(appliance.duration):
#                                 energy_used = min(
#                                     household_energy[hour][household_idx],
#                                     appliance.power / appliance.duration,
#                                 )
#                                 total_available_energy -= energy_used
#                                 household_energy[hour][
#                                     household_idx
#                                 ] -= energy_used
#                             plannedin = True
#                             usage -= 1
#                             break
#
#                         if plannedin is True:
#                             continue
#
#                         for i in range(24):
#                             if plannedin is True:
#                                 break
#                             currenttime = date + 3600 * i
#                             if (
#                                 check_appliance_time(
#                                     appliance,
#                                     currenttime,
#                                     appliance_bitmap_plan,
#                                     appliance_no_energy_bitmap_plan,
#                                     False,
#                                 )
#                                 is False
#                             ):
#                                 continue
#                             plan_no_energy(
#                                 session,
#                                 appliance,
#                                 currenttime,
#                                 appliance_no_energy_bitmap_plan,
#                             )
#                             plannedin = True
#                             usage -= 1
#
#                         if plannedin is False:
#                             #     print("Not planned in", appliance, date)
#                             usage = 0
#             energyflow_day_sim: list[EnergyFlowRead] = [
#                 el
#                 for el in energyflow_data_sim
#                 if (date <= el.timestamp and el.timestamp < date + 3600 * 24)
#             ]  # only check the current day for energy flow
#             temp_result = [0.0 for x in range(4)]
#             (
#                 temp_result[0],
#                 temp_result[1],
#                 temp_result[2],
#                 temp_result[3],
#             ) = energy_efficiency_day(
#                 session,
#                 energyflow_day_sim,
#                 planning,
#                 day_number_in_planning,
#                 date,
#             )
#             for iter in range(4):
#                 if temp_result[iter] > results[day_number_in_planning][iter]:
#                     results[day_number_in_planning][iter] = temp_result[iter]
#
#     initial_planning_energy = appliance_time_daily_crud.get_multi(
#         session=session, limit=10
#     )
#     initial_planning_no_energy = appliance_time_no_energy_daily_crud.get_multi(
#         session=session, limit=10
#     )
#     # TODO: Stuur results nog mee?
#     print(results)
#     return ApplianceTime(
#         appliance_time_daily=initial_planning_energy,
#         appliance_time_no_energy_daily=initial_planning_no_energy,
#     )
