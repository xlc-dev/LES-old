from fastapi import APIRouter, Depends, HTTPException, Body, status

from sqlmodel import Session, SQLModel

import random

from app.utils import get_session

from app.core.models.costmodel_model import CostModelRead
from app.core.models.twinworld_model import TwinWorldRead
from app.core.models.algorithm_model import AlgorithmRead
from app.core.models.household_model import HouseholdRead
from app.core.models.energyflow_model import EnergyFlowRead
from app.core.models.appliance_model import (
    ApplianceTimeNoEnergyDaily,
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
    twinworld = twinworld_crud.get(session=session, id=twinworld_id)

    if not twinworld:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No twinworld found with id: {twinworld_id}",
        )

    costmodel = costmodel_crud.get(session=session, id=costmodel_id)

    if not costmodel:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No costmodel found with id: {costmodel_id}",
        )

    algorithm = algorithm_crud.get(session=session, id=algorithm_id)

    if not algorithm:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No algorithm found with id: {algorithm_id}",
        )

    results = household_crud.get_by_twinworld_sorted_solar_panels(
        session=session, id=twinworld.id
    )

    if not results:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No results found for twinworld with id: {twinworld_id}",
        )

    return results


@router.post("/reset", response_model="None")
async def reset(*, session: Session = Depends(get_session)) -> None:
    initial_planning_energy = appliance_time_daily_crud.get_multi(
        session=session, limit=10**9
    )
    initial_planning_no_energy = appliance_time_no_energy_daily_crud.get_multi(
        session=session, limit=10**9
    )
    for appliance_energy in initial_planning_energy:
        appliance_time_daily_crud.remove(
            session=session, id=appliance_energy.id
        )
    for appliance_no_energy in initial_planning_no_energy:
        appliance_time_no_energy_daily_crud.remove(
            session=session, id=appliance_no_energy.id
        )


@router.post("/stop")
async def stop(*, session: Session = Depends(get_session)):
    return {"message": "Simulation ended"}


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
        amount_of_households = household_crud.count_households(
            session=session
        )  # gets the amount of households in the planning
        start_date, end_date = energyflow_crud.get_start_end_date(
            session=session
        )
        start_date, end_date = start_date.timestamp, end_date.timestamp
        # Plan: for the loop
        # First we do one day at a time, chronologically
        # This day needs to be initialized with the right helper variables

        # Then we plan all of the devices one household at a time
        # Ordering is done by most solar panels first
        # with the result of each house useing their own energy first
        # Only later on it's allowed to use energy from other houses

        for date in range(start_date, end_date + 86400, 86400):
            day_number_in_planning = (date - start_date) / 86400 + 1
            print(int(day_number_in_planning))
            energyflow_day: EnergyFlowRead = [
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
                    hour = unix_to_hour(energyflow_day_information_init.timestamp)
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
                    usage = appliance.daily_usage                           # misschien niet nodig
                    appliance_bitmap_plan = (
                        appliance_time_daily_crud.get_appliance_time_daily(
                            session=session,
                            appliance_id=appliance.id,
                            day=day_number_in_planning,
                        )
                    )
                    if not appliance_bitmap_plan:                          # error testing
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
    initial_planning_energy = appliance_time_daily_crud.get_multi(
        session=session, limit=10
    )
    initial_planning_no_energy = appliance_time_no_energy_daily_crud.get_multi(
        session=session, limit=10
    )
    return ApplianceTime(
        appliance_time_daily=initial_planning_energy,
        appliance_time_no_energy_daily=initial_planning_no_energy,
    )
