from typing import Sequence

from fastapi import APIRouter, Depends, status

from sqlmodel import Session

from app.utils import Logger, get_session

from app.core.models import household_model

from app.core.crud.household_crud import household_crud

router = APIRouter()


@router.get("/", response_model=list[household_model.HouseholdRead])
async def get_households(
    *, session: Session = Depends(get_session)
) -> Sequence[household_model.Household]:
    return household_crud.get_multi(session=session)


@router.get("/{id}", response_model=household_model.HouseholdRead)
async def get_household(
    *, id: int, session: Session = Depends(get_session)
) -> household_model.Household:
    household = household_crud.get(session=session, id=id)

    if not household:
        Logger.exception(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"household with id: {id} not found",
        )

    return household


@router.get(
    "/twinworld/{twinworld_id}",
    response_model=list[household_model.HouseholdRead],
)
async def get_households_by_twinworld(
    *, twinworld_id: int, session: Session = Depends(get_session)
) -> Sequence[household_model.Household]:
    household = household_crud.get(session=session, id=twinworld_id)

    if not household:
        Logger.exception(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"twinworld with id: {household} not found",
        )

    return household_crud.get_by_twinworld(session=session, id=twinworld_id)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def post_household(
    *,
    form_data: household_model.HouseholdCreate,
    session: Session = Depends(get_session),
) -> None:
    check_household = household_crud.get_by_name(
        session=session, name=form_data.name
    )

    if check_household:
        Logger.exception(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"household with name: {form_data.name} already exists",
        )

    household_crud.create(session=session, obj_in=form_data)


@router.patch("/{id}", response_model=household_model.HouseholdUpdate)
async def update_household(
    *,
    id: int,
    household: household_model.HouseholdUpdate,
    session: Session = Depends(get_session),
) -> household_model.HouseholdUpdate:
    current_household = household_crud.get(session=session, id=id)

    if not current_household:
        Logger.exception(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Household with ID: {id} not found",
        )

    household_crud.update(
        session=session,
        db_obj=current_household,
        obj_in=household,
    )

    return household


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_household(
    *,
    id: int,
    session: Session = Depends(get_session),
) -> None:
    household = household_crud.get(session=session, id=id)

    if not household:
        Logger.exception(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"household with ID: {id} not found",
        )

    if household.twinworld_id == 1 or household.twinworld_id == 2:
        Logger.exception(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"household with twinworld id: {id} is not allowed to be deleted",  # noqa: E501
        )

    household_crud.remove(session=session, id=id)
