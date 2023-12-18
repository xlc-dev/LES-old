from typing import Sequence

from fastapi import APIRouter, Depends, HTTPException, status

from sqlmodel import Session

from app.utils import get_session

from app.core.crud.energyflow_crud import energyflow_crud
from app.core.models import energyflow_model

router = APIRouter()


@router.get("/", response_model=list[energyflow_model.EnergyFlowRead])
async def get_energyflows(
    *, session: Session = Depends(get_session)
) -> Sequence[energyflow_model.EnergyFlow]:
    return energyflow_crud.get_multi(session=session)


@router.get("/{id}/", response_model=energyflow_model.EnergyFlowRead)
async def get_energyflow(
    *, id: int, session: Session = Depends(get_session)
) -> energyflow_model.EnergyFlow:
    energyflow = energyflow_crud.get(session=session, id=id)

    if not energyflow:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"energyflow with id: {id} not found.",
        )

    return energyflow


@router.post("/", status_code=status.HTTP_201_CREATED)
async def post_energyflow(
    *,
    form_data: energyflow_model.EnergyFlowCreate,
    session: Session = Depends(get_session),
) -> None:
    check_energyflow = energyflow_crud.get_by_name(
        session=session, name=form_data.name
    )

    if check_energyflow:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"energyflow with name: {form_data.name} already exists.",
        )

    energyflow_crud.create(session=session, obj_in=form_data)
