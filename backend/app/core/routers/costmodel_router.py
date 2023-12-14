from typing import Sequence

from fastapi import APIRouter, Depends, HTTPException, status

from sqlmodel import Session

from app.utils import get_session

from app.core.crud.costmodel_crud import costmodel_crud
from app.core.schemas import costmodel_schema
from app.core.models import costmodel_model

router = APIRouter()


@router.get("/", response_model=list[costmodel_schema.CostModelRead])
async def get_costmodels(
    *, session: Session = Depends(get_session)
) -> Sequence[costmodel_model.CostModel]:
    return costmodel_crud.get_multi(session=session)


@router.get("/{id}/", response_model=costmodel_schema.CostModelRead)
async def get_costmodel(
    *, id: int, session: Session = Depends(get_session)
) -> costmodel_model.CostModel:
    costmodel = costmodel_crud.get(session=session, id=id)

    if not costmodel:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"costmodel with id: {id} not found.",
        )

    return costmodel


@router.post("/", status_code=status.HTTP_201_CREATED)
async def post_costmodel(
    *,
    form_data: costmodel_schema.CostModelCreate,
    session: Session = Depends(get_session),
) -> None:
    check_costmodel = costmodel_crud.get_by_name(
        session=session, name=form_data.name
    )

    if check_costmodel:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"costmodel with name: {form_data.name} already exists.",
        )

    costmodel_crud.create(session=session, obj_in=form_data)
