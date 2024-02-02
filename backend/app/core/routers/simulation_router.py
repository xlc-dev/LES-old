"""This router, just like the seed_router, is a special router.

Here are all the simulation endpoints to run the simulation.

The general idea is that the frontend would call the /load-data endpoint to get
all the possible options for the simulation. Then once the user has selected
the options through the stepper, the frontend would call the /start endpoint to
start the simulation.

Once the simulation is done because the algorithm isn't finding any more
improvements, or the user has stopped the simulation, the frontend stops
calling the /plan endpoint, and ends the simulation.
"""

# Import libraries for exec() by the researcher
import pandas  # noqa: F401
import numpy  # noqa: F401
import scipy  # noqa: F401
import math  # noqa: F401
import random  # noqa: F401

from fastapi import APIRouter, Depends, Body, status

from sqlmodel import Session

from app.utils import Logger, get_session, SECONDS_IN_DAY

from app.core.crud.costmodel_crud import costmodel_crud
from app.core.crud.twinworld_crud import twinworld_crud
from app.core.crud.algorithm_crud import algorithm_crud
from app.core.crud.household_crud import household_crud
from app.core.crud.energyflow_crud import energyflow_upload_crud

from app.plan_defaults import plan_greedy, plan_simulated_annealing
from app.plan_helpers import (
    SimulationData,
    SelectedOptions,
    SelectedModelsInput,
    SelectedModelsOutput,
    setup_planning,
    loop_helpers,
    create_results,
    write_results,
)

router = APIRouter()


@router.get("/load-data", response_model=SimulationData)
async def get_data(*, session: Session = Depends(get_session)):
    "Get all possible options for the simulation"
    twinworlds = twinworld_crud.get_multi(session=session)
    costmodels = costmodel_crud.get_multi(session=session)
    algorithms = algorithm_crud.get_multi(session=session)
    energyflows = energyflow_upload_crud.get_multi(session=session)

    return SimulationData(
        twinworld=twinworlds,
        costmodel=costmodels,
        algorithm=algorithms,
        energyflow=energyflows,
    )


@router.post("/start", response_model=SelectedOptions)
async def start(
    *,
    algorithm_id: int = Body(...),
    twinworld_id: int = Body(...),
    costmodel_id: int = Body(...),
    energyflow_id: int = Body(...),
    session: Session = Depends(get_session),
) -> SelectedOptions:
    "Start the simulation with the given parameters from /get-data"
    twinworld = twinworld_crud.get(session=session, id=twinworld_id)

    if not twinworld:
        Logger.exception(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Twinworld with id {twinworld_id} not found",
        )

    costmodel = costmodel_crud.get(session=session, id=costmodel_id)

    if not costmodel:
        Logger.exception(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Costmodel with id {costmodel_id} not found",
        )

    algorithm = algorithm_crud.get(session=session, id=algorithm_id)

    if not algorithm:
        Logger.exception(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Algorithm with id {algorithm_id} not found",
        )

    energyflow_upload = energyflow_upload_crud.get(
        session=session, id=energyflow_id
    )

    if not energyflow_upload:
        Logger.exception(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Energyflow with id {energyflow_id} not found",
        )

    households = household_crud.get_by_twinworld_sorted_solar_panels(
        session=session, id=twinworld.id
    )

    if not households:
        Logger.exception(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No households found for twinworld with id {twinworld_id}",
        )

    return SelectedOptions(
        twinworld=twinworld,
        costmodel=costmodel,
        algorithm=algorithm,
        households=households,
        energyflow=energyflow_upload,
    )


@router.post("/plan", response_model=SelectedModelsOutput)
async def plan(
    *, planning: SelectedModelsInput, session: Session = Depends(get_session)
) -> SelectedModelsOutput:
    """The plan function executing all the different subfunctions.

    The plan function is done in the following 8 steps:
    1. All the relevant data is gathered in setup_planning
    2. For each day, relevant data is gathered in loop_helpers
    3. The greedy algorithm is executed with plan_greedy, resulting in a base
    planning
    4. The framework for the results is created in create_results
    5. The results of greedy algorithm are documented in write_results
    6. If selected, the simulated annealing is performed, resulting in an
    improved planning
    7. The results, and any improvements, are recorded again in write_results
    8. The results and planned in data is send back to the frontend

    The reason for performing write_results twice is in case the random nature
    of simulated annealing causes a worse result during simulated annealing.
    While this is unlikely, it technically is possible.
    """
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
    ) = setup_planning(session=session, planning=planning)

    local_vars = locals()
    global_vars = globals()
    local_vars.update({
        "days_in_chunk": days_in_chunk,
        "days_in_planning": days_in_planning,
        "length_planning": length_planning,
        "start_date": start_date,
        "end_date": end_date,
        "total_start_date": total_start_date,
        "energyflow_data_sim": energyflow_data_sim,
        "energyflow_data": energyflow_data,
        "appliance_time": appliance_time,
        "household_planning": household_planning,
        "results": results,
    })
    global_vars.update(local_vars)

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
            energyflow=planning.energyflow,
            twinworld=planning.twinworld,
        )

        local_vars.update({
            "date": date,
            "energyflow_day": energyflow_day,
            "household_energy": household_energy,
            "total_available_energy": total_available_energy,
            "day_number_in_planning": day_number_in_planning,
        })
        global_vars.update(local_vars)

        if (
            planning.algorithm.name == "Greedy planning"
            or planning.algorithm.name == "Simulated Annealing"
        ):
            for household_idx, household in enumerate(household_planning):
                for appliance in household.appliances:
                    (
                        appliance_time,
                        total_available_energy,
                        household_energy,
                    ) = plan_greedy(
                        household_idx=household_idx,
                        days_in_planning=days_in_planning,
                        day_number_in_planning=day_number_in_planning,
                        total_available_energy=total_available_energy,
                        household_energy=household_energy,
                        appliance=appliance,
                        appliance_time=appliance_time,
                        energyflow_day=energyflow_day,
                        total_start_date=total_start_date,
                    )

        (
            solar_produced,
            current_used,
            current_available,
            energyflow_day_sim,
        ) = create_results(
            total_start_date=total_start_date,
            day_number_in_planning=day_number_in_planning,
            energyflow_data_sim=energyflow_data_sim,
            household_planning=household_planning,
            energyflow=planning.energyflow,
        )

        results = write_results(
            date=date,
            day_iterator=day_iterator,
            day_number_in_planning=day_number_in_planning,
            results=results,
            energyflow=planning.energyflow,
            twinworld=planning.twinworld,
            costmodel=planning.costmodel,
            appliance_time=appliance_time,
            energyflow_day_sim=energyflow_day_sim,
            household_planning=household_planning,
        )

        if total_available_energy <= 0:
            continue

        if planning.algorithm.name == "Simulated Annealing":
            plan_simulated_annealing(
                date=date,
                days_in_planning=days_in_planning,
                day_number_in_planning=day_number_in_planning,
                length_planning=length_planning,
                current_available=current_available,
                solar_produced=solar_produced,
                current_used=current_used,
                algorithm=planning.algorithm,
                household_planning=household_planning,
                appliance_time=appliance_time,
            )

            results = write_results(
                date=date,
                day_iterator=day_iterator,
                day_number_in_planning=day_number_in_planning,
                results=results,
                energyflow=planning.energyflow,
                twinworld=planning.twinworld,
                costmodel=planning.costmodel,
                appliance_time=appliance_time,
                energyflow_day_sim=energyflow_day_sim,
                household_planning=household_planning,
            )

        # If the researcher didn't select the greedy or simulated
        # annealing algorithm, evaluate the algorithm of the researcher
        if (
            planning.algorithm.name != "Greedy planning"
            and planning.algorithm.name != "Simulated Annealing"
        ):
            algo = planning.algorithm.algorithm
            try:
                exec(algo, global_vars, local_vars)
                run = local_vars.get("run", None)
                run()
            except Exception as e:
                Logger.exception(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Error in algorithm: {e}",
                )

    start_day = (start_date - total_start_date) // SECONDS_IN_DAY + 1

    time_daily = [
        el
        for el in appliance_time
        if el.day >= start_day and el.day < start_day + days_in_chunk
    ]

    return SelectedModelsOutput(
        results=results,
        timedaily=time_daily,
        days_in_planning=days_in_planning,
        start_date=total_start_date,
        end_date=end_date,
    )
