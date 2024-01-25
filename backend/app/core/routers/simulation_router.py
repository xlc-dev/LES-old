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

from fastapi import APIRouter, Depends, Body, status

from sqlmodel import Session

from app.utils import Logger, get_session, SECONDS_IN_DAY

from app.core.crud.costmodel_crud import costmodel_crud
from app.core.crud.twinworld_crud import twinworld_crud
from app.core.crud.algorithm_crud import algorithm_crud
from app.core.crud.household_crud import household_crud

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
                        date=date,
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
            twinworld=planning.twinworld,
        )

        results = write_results(
            date=date,
            day_iterator=day_iterator,
            day_number_in_planning=day_number_in_planning,
            results=results,
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
            eval(planning.algorithm.algorithm)

    start_day = (start_date - total_start_date) // SECONDS_IN_DAY + 1

    time_daily = [
        el
        for el in appliance_time
        if el.day >= start_day and el.day < start_day + days_in_chunk
    ]

    return SelectedModelsOutput(
        results=results,
        timedaily=time_daily,
        start_date=total_start_date,
        end_date=end_date,
    )
