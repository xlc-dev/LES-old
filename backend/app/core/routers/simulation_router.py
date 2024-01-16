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

from sqlmodel import Session, SQLModel

from app.utils import Logger, get_session

from app.core.models.costmodel_model import CostModelRead
from app.core.models.twinworld_model import TwinWorldRead
from app.core.models.algorithm_model import AlgorithmRead
from app.core.models.household_model import HouseholdRead

from app.core.crud.costmodel_crud import costmodel_crud
from app.core.crud.twinworld_crud import twinworld_crud
from app.core.crud.algorithm_crud import algorithm_crud
from app.core.crud.household_crud import household_crud

router = APIRouter()


class SimulationData(SQLModel):
    twin_world: list[TwinWorldRead]
    cost_model: list[CostModelRead]
    algorithm: list[AlgorithmRead]


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

    results = household_crud.get_by_twinworld(session=session, id=twinworld_id)

    if not results:
        Logger.exception(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No results found for twinworld with id: {twinworld_id}",
        )

    return results


@router.post("/stop")
async def stop(*, session: Session = Depends(get_session)):
    return {"message": "Simulation ended"}
