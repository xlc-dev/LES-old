from typing import Sequence

from fastapi import APIRouter, Depends, HTTPException, status

from sqlmodel import Session

from app.utils import get_session

from app.core.crud.twinworld_crud import twinworld_crud
from app.core.crud.household_crud import household_crud
from app.core.models import twinworld_model, household_model

router = APIRouter()


@router.get("/", response_model=list[twinworld_model.TwinWorldRead])
async def get_twinworlds(
    *, session: Session = Depends(get_session)
) -> Sequence[twinworld_model.TwinWorld]:
    return twinworld_crud.get_multi(session=session)


@router.get("/{id}/", response_model=twinworld_model.TwinWorldRead)
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
    form_data: twinworld_model.TwinWorldCreate,
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


@router.delete("/{id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_twinworld(
    *,
    id: int,
    session: Session = Depends(get_session),
) -> None:
    twinworld = twinworld_crud.get(session=session, id=id)

    if not twinworld:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Twinworld with ID: {id} not found",
        )

    if twinworld.id == 1 or twinworld.id == 2:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Twinworld with ID: {id} is not allowed to be deleted.",
        )

    twinworld_crud.remove(session=session, id=id)


@router.post("/{twinworld_id}/households/", response_model=household_model.HouseholdRead)
async def create_household_for_twinworld(twinworld_id: int, household_data: household_model.HouseholdCreate,
                                         session: Session = Depends(get_session)):
    twinworld = twinworld_crud.get(session=session, id=twinworld_id)
    if not twinworld:
        raise HTTPException(status_code=404, detail="Twinworld not found")
    household = household_crud.create_with_twinworld(session=session, obj_in=household_data, twinworld_id=twinworld_id)
    return household


@router.put("/{twinworld_id}/households/{household_id}", response_model=household_model.HouseholdRead)
async def update_household_for_twinworld(twinworld_id: int, household_id: int,
                                         household_data: household_model.HouseholdUpdate,
                                         session: Session = Depends(get_session)):
    twinworld = twinworld_crud.get(session=session, id=twinworld_id)
    if not twinworld:
        raise HTTPException(status_code=404, detail="Twinworld not found")
    household = household_crud.get(session=session, id=household_id)
    if not household or household.twinworld_id != twinworld_id:
        raise HTTPException(status_code=404, detail="Household not found in this twinworld")
    household = household_crud.update(session=session, db_obj=household, obj_in=household_data)
    return household


@router.delete("/{twinworld_id}/households/{household_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_household_for_twinworld(twinworld_id: int, household_id: int, session: Session = Depends(get_session)):
    twinworld = twinworld_crud.get(session=session, id=twinworld_id)
    if not twinworld:
        raise HTTPException(status_code=404, detail="Twinworld not found")
    household = household_crud.get(session=session, id=household_id)
    if not household or household.twinworld_id != twinworld_id:
        raise HTTPException(status_code=404, detail="Household not found in this twinworld")
    household_crud.remove(session=session, id=household_id)
    return None
