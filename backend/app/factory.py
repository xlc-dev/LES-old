# from dataclasses import dataclass

from fastapi import APIRouter, Depends, status

from sqlmodel import Session

# from polyfactory.factories import DataclassFactory

from app.utils import (
    Logger,
    get_session,
    create_db_and_tables,
    delete_db_and_tables,
)


router = APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED)
def factory(session: Session = Depends(get_session)):
    delete_db_and_tables()
    create_db_and_tables()

    try:
        session.commit()
    except Exception:
        session.rollback()

        Logger.exception(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not add factory data",
        )
