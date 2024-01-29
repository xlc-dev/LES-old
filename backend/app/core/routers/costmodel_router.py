from typing import Sequence

from fastapi import APIRouter, Depends, status

from sqlmodel import Session

from app.utils import Logger, get_session

from app.core.models import costmodel_model

from app.core.crud.costmodel_crud import costmodel_crud

router = APIRouter()


@router.get("/", response_model=list[costmodel_model.CostModelRead])
async def get_costmodels(
    *, session: Session = Depends(get_session)
) -> Sequence[costmodel_model.CostModel]:
    return costmodel_crud.get_multi(session=session)


@router.get("/{id}", response_model=costmodel_model.CostModelRead)
async def get_costmodel(
    *, id: int, session: Session = Depends(get_session)
) -> costmodel_model.CostModel:
    costmodel = costmodel_crud.get(session=session, id=id)

    if not costmodel:
        Logger.exception(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"costmodel with id: {id} not found",
        )

    return costmodel


@router.post("/", status_code=status.HTTP_201_CREATED)
async def post_costmodel(
    *,
    form_data: costmodel_model.CostModelCreate,
    session: Session = Depends(get_session),
) -> None:
    check_costmodel = costmodel_crud.get_by_name(
        session=session, name=form_data.name
    )

    if check_costmodel:
        Logger.exception(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"costmodel with name: {form_data.name} already exists",
        )

    costmodel_crud.create(session=session, obj_in=form_data)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_costmodel(
    *,
    id: int,
    session: Session = Depends(get_session),
) -> None:
    # Don't allow the user to delete the default costmodels
    if id == 1 or id == 2:
        Logger.exception(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"costmodel with ID: {id} is not allowed to be deleted",
        )

    costmodel = costmodel_crud.get(session=session, id=id)

    if not costmodel:
        Logger.exception(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"costmodel with ID: {id} not found",
        )

    costmodel_crud.remove(session=session, id=id)
