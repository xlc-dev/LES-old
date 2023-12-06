import logging
import traceback
from typing import Generator

from fastapi import HTTPException, Response

from sqlmodel import SQLModel, Session

from app.config import engine


def set_sec_headers(*, response: Response):
    "Set security headers headers of the response"

    response.headers[
        "Strict-Transport-Security"
    ] = "max-age=31536000; includeSubDomains"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1"
    response.headers["Referrer-Policy"] = "no-referrer, same-origin"

    return response


def create_db_and_tables() -> None:
    "Create SQL DB and create tables and columns"

    SQLModel.metadata.create_all(engine)


def delete_db_and_tables() -> None:
    "Delete SQL DB and create tables and columns"

    SQLModel.metadata.drop_all(engine)


def get_session() -> Generator:
    "Create session and get the engine as db"

    with Session(engine) as session:
        yield session


class Logger(logging.Formatter):
    "Logging class to format logs with color"

    grey = "\x1b[38;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    format: str = (
        "%(asctime)s - %(name)s - %(levelname)s"  # type: ignore
        "- %(message)s (%(filename)s:%(lineno)d)"
    )

    FORMATS = {
        logging.DEBUG: grey + format + reset,
        logging.INFO: grey + format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + format + reset,
        logging.CRITICAL: bold_red + format + reset,
    }

    def format(self, record):  # type: ignore
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)

    @staticmethod
    def debug(value: str) -> None:
        logging.debug(value)

    @staticmethod
    def info(value: str) -> None:
        logging.info(value)

    @staticmethod
    def warning(value: str) -> None:
        logging.warning(value)

    @staticmethod
    def error(value: str) -> None:
        logging.error(value)

    @staticmethod
    def exception(*, status_code: int, detail: str, headers=None) -> HTTPException:
        logging.error(detail + "\n" + traceback.format_exc())
        raise HTTPException(status_code=status_code, detail=detail, headers=headers)
