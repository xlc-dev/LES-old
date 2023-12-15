from fastapi import APIRouter, Depends, HTTPException, Body, status
from pydantic import BaseModel

from sqlmodel import Session, SQLModel

from app.utils import get_session
from typing import List

from app.core.models.algorithm_model import Algorithm, AlgorithmCreate
from app.core.models.costmodel_model import CostModel, CostModelCreate
from app.core.models.twinworld_model import TwinWorld, TwinWorldCreate

from app.core.models.costmodel_model import CostModelRead
from app.core.models.twinworld_model import TwinWorldRead
from app.core.models.algorithm_model import AlgorithmRead
from app.core.models.household_model import HouseholdRead

from app.core.crud.costmodel_crud import costmodel_crud
from app.core.crud.twinworld_crud import twinworld_crud
from app.core.crud.algorithm_crud import algorithm_crud
from app.core.crud.household_crud import household_crud

from app.utils import get_session

router = APIRouter()


class SaveSelectionRequest(BaseModel):
    algorithms: List[AlgorithmCreate]
    pricingModels: List[CostModelCreate]
    twinWorlds: List[TwinWorldCreate]


class SimulationData(SQLModel):
    twin_world: list[TwinWorldRead]
    cost_model: list[CostModelRead]
    algorithm: list[AlgorithmRead]


@router.get("/load-data", response_model=SimulationData)
async def get_data(*, session: Session = Depends(get_session)):
    twinworlds = twinworld_crud.get_multi(session=session)
    costmodels = costmodel_crud.get_multi(session=session)
    algorithms = algorithm_crud.get_multi(session=session)

    return SimulationData(
        twin_world=twinworlds, cost_model=costmodels, algorithm=algorithms
    )


# @router.post("/save")
# def save_selection(request_data: SaveSelectionRequest, session: Session = Depends(get_session)):
#     print("Received data:", request_data)
#     for algorithm_data in request_data.algorithms:
#         algorithm_crud.create(obj_in=algorithm_data, session=session)
#
#     for pricing_model_data in request_data.pricingModels:
#         costmodel_crud.create(obj_in=pricing_model_data, session=session)
#
#     for twin_world_data in request_data.twinWorlds:
#         twinworld_crud.create(obj_in=twin_world_data, session=session)
#
#     return {"message": "Data saved successfully"}


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

    results = household_crud.get_by_twinworld(session=session, id=twinworld.id)

    if not results:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No results found for twinworld with id: {twinworld_id}",
        )

    return results


@router.post("/stop")
async def stop(*, session: Session = Depends(get_session)):
    return {"message": "Simulation ended"}
