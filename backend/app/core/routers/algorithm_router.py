from typing import Sequence

from fastapi import APIRouter, Depends, HTTPException, status

from sqlmodel import Session

from app.utils import get_session

from app.core.crud.algorithm_crud import algorithm_crud
from app.core.models import algorithm_model

router = APIRouter()


@router.get("/", response_model=list[algorithm_model.AlgorithmRead])
async def get_algorithms(
    *, session: Session = Depends(get_session)
) -> Sequence[algorithm_model.Algorithm]:
    return algorithm_crud.get_multi(session=session)


@router.get("/{id}/", response_model=algorithm_model.AlgorithmRead)
async def get_algorithm(
    *, id: int, session: Session = Depends(get_session)
) -> algorithm_model.Algorithm:
    algorithm = algorithm_crud.get(session=session, id=id)

    if not algorithm:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"algorithm with id: {id} not found.",
        )

    return algorithm


@router.post("/", status_code=status.HTTP_201_CREATED)
async def post_algorithm(
    *,
    form_data: algorithm_model.AlgorithmCreate,
    session: Session = Depends(get_session),
) -> None:
    check_algorithm = algorithm_crud.get_by_name(
        session=session, name=form_data.name
    )

    if check_algorithm:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"algorithm with name: {form_data.name} already exists.",
        )

    algorithm_crud.create(session=session, obj_in=form_data)


@router.delete("/{id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_algorithm(
    *,
    id: int,
    session: Session = Depends(get_session),
) -> None:
    algorithm = algorithm_crud.get(session=session, id=id)

    if not algorithm:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"algorithm with ID: {id} not found",
        )

    if algorithm.id == 1 or algorithm.id == 2:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"algorithm with ID: {id} is not allowed to be deleted.",
        )

    algorithm_crud.remove(session=session, id=id)
