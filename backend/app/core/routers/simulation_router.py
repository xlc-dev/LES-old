from fastapi import APIRouter, Depends, HTTPException, Body, status

from sqlmodel import Session, SQLModel

from random import random

from app.utils import get_session
from app.simulation import plan_new

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


@router.post("/plan")
async def plan(
    *, planning: list[HouseholdRead], session: Session = Depends(get_session)
):
    if planning[0].appliances[0].appliance_windows[0].bitmap_plan is None:
        for household in planning:
            for appliance in household.appliances:
                for timewindow in appliance.appliance_windows:
                    print(timewindow.day, timewindow.bitmap_window, household.name, appliance.name, appliance.daily_usage)
                    usage = appliance.daily_usage
                    while usage < random.random():
                        starttime = max
                        plan_new(appliance.name, starttime, appliance.duration)
        # plan_new (appliance=planning[0].appliances[0].name[0])
    return


# , response_model=list[HouseholdRead]
