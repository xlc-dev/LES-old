from typing import Sequence

from fastapi import APIRouter, Depends, HTTPException, status

from sqlmodel import Session

from app.utils import get_session

from app.core.crud.twinworld_crud import twinworld_crud
from app.core.schemas import twinworld_schema
from app.core.models import twinworld_model

router = APIRouter()


@router.get("/", response_model=list[twinworld_schema.TwinWorldRead])
async def get_twinworlds(
    *, session: Session = Depends(get_session)
) -> Sequence[twinworld_model.TwinWorld]:
    return twinworld_crud.get_multi(session=session)


@router.get("/{id}/", response_model=twinworld_schema.TwinWorldRead)
async def get_twinworld(
    *, id: int, session: Session = Depends(get_session)
) -> twinworld_model.TwinWorld:
    twinworld = twinworld_crud.get(session=session, id=id)

    if not twinworld:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Twinworld with id: {id} not found.",
        )

    return twinworld


@router.post("/", status_code=status.HTTP_201_CREATED)
async def post_twinworld(
    *,
    form_data: twinworld_schema.TwinWorldCreate,
    session: Session = Depends(get_session),
) -> None:
    check_twinworld = twinworld_crud.get_by_name(
        session=session, name=form_data.name
    )

    if check_twinworld:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Twinworld with name: {form_data.name} already exists.",
        )

    twinworld_crud.create(session=session, obj_in=form_data)
