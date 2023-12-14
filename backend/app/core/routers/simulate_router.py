from fastapi import APIRouter, Depends

from sqlmodel import Session

from app.utils import get_session

from app.core.schemas import simulation_schema

from app.core.routers.twinworld_router import get_twinworlds
from app.core.routers.costmodel_router import get_costmodels

router = APIRouter()


@router.get("/load-data", response_model=simulation_schema.SimulationData)
async def get_data(*, session: Session = Depends(get_session)):
    twinworlds = await get_twinworlds(session=session)
    costmodels = await get_costmodels(session=session)

    return simulation_schema.SimulationData(
        twin_world=twinworlds, cost_model=costmodels
    )


@router.post("/start")
async def start(*, session: Session = Depends(get_session)):
    return {"message": "Simulation started"}


@router.post("/stop")
def stop():
    return {"message": "Simulation ended"}
