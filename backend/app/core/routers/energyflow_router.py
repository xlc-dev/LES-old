from typing import Sequence

from fastapi import APIRouter, Depends, status

from sqlmodel import Session

from app.utils import Logger, get_session

from app.core.crud.energyflow_crud import energyflow_crud
from app.core.models import energyflow_model

router = APIRouter()


@router.get("/", response_model=list[energyflow_model.EnergyFlowRead])
async def get_energyflows(
    *, session: Session = Depends(get_session)
) -> Sequence[energyflow_model.EnergyFlow]:
    return energyflow_crud.get_multi(session=session)


@router.get("/{id}", response_model=energyflow_model.EnergyFlowRead)
async def get_energyflow(
    *, id: int, session: Session = Depends(get_session)
) -> energyflow_model.EnergyFlow:
    energyflow = energyflow_crud.get(session=session, id=id)

    if not energyflow:
        Logger.exception(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Energyflow with id {id} not found",
        )

    return energyflow


@router.post("/", status_code=status.HTTP_201_CREATED)
async def post_energyflow(
    *,
    form_data: energyflow_model.EnergyFlowCreate,
    session: Session = Depends(get_session),
) -> None:
    check_energyflow = energyflow_crud.get_by_timestamp(
        session=session, timestamp=form_data.timestamp
    )

    if check_energyflow:
        Logger.exception(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Energyflow with timestamp {form_data.timestamp} already exists",  # noqa: E501
        )

    energyflow_crud.create(session=session, obj_in=form_data)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_energyflow(
    *,
    id: int,
    session: Session = Depends(get_session),
) -> None:
    # Don't allow the user to delete the default energyflow
    if id == 1:
        Logger.exception(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Energyflow with id {id} is not allowed to be deleted",
        )

    eneryflow = energyflow_crud.get(session=session, id=id)

    if not eneryflow:
        Logger.exception(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Energyflow with id {id} not found",
        )

    energyflow_crud.remove(session=session, id=id)
