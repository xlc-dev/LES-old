import pandas
import numpy
import math
import random
import scipy
import ast

from typing import Sequence

from fastapi import APIRouter, Depends, status

from sqlmodel import Session

from app.utils import Logger, get_session

from app.core.models import algorithm_model

from app.core.crud.algorithm_crud import algorithm_crud

router = APIRouter()


@router.get("/", response_model=list[algorithm_model.AlgorithmRead])
async def get_algorithms(
    *, session: Session = Depends(get_session)
) -> Sequence[algorithm_model.Algorithm]:
    return algorithm_crud.get_multi(session=session)


@router.get("/{id}", response_model=algorithm_model.AlgorithmRead)
async def get_algorithm(
    *, id: int, session: Session = Depends(get_session)
) -> algorithm_model.Algorithm:
    algorithm = algorithm_crud.get(session=session, id=id)

    if not algorithm:
        Logger.exception(
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
        Logger.exception(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"algorithm with name: {form_data.name} already exists.",
        )

    # Create a restricted globals dictionary
    restricted_globals = {
        "pandas": pandas,
        "numpy": numpy,
        "scipy": scipy,
        "math": math,
        "random": random,
    }

    # Simple check if the code is valid Python syntax, it is bypassable.
    # TODO: make this more comprehensive.
    try:
        compile(form_data.algorithm, "<string>", "exec")
    except SyntaxError as e:
        Logger.exception(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid syntax in the provided code: {str(e)}",
        )

    imports = set()

    # Walk through the tree and find all imports
    for node in ast.walk(ast.parse(form_data.algorithm)):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.add(alias.name)
        elif isinstance(node, ast.ImportFrom):
            imports.add(node.module)

    # Check if any imported module is not in restricted_globals
    invalid_imports = [imp for imp in imports if imp not in restricted_globals]

    if invalid_imports:
        Logger.exception(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid imports: {', '.join(invalid_imports)}",
        )

    algorithm_crud.create(session=session, obj_in=form_data)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_algorithm(
    *,
    id: int,
    session: Session = Depends(get_session),
) -> None:
    # Don't allow the user to delete the default algorithms
    if id == 1 or id == 2:
        Logger.exception(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"algorithm with ID: {id} is not allowed to be deleted.",
        )

    algorithm = algorithm_crud.get(session=session, id=id)

    if not algorithm:
        Logger.exception(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"algorithm with ID: {id} not found",
        )

    algorithm_crud.remove(session=session, id=id)
