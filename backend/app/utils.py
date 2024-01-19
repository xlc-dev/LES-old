"""All global utility functions.

This module contains all the global utility functions
that are used throughout the application.
"""

import logging
import traceback
from typing import Generator, NoReturn

from fastapi import HTTPException, Response

from sqlmodel import SQLModel, Session

from app.config import engine


SECONDS_IN_DAY = 86400
HOURS_IN_WEEK = 168


def timestamp_to_unix(timestamp: float) -> int:
    "Convert excel timestamp to unix timestamp"
    return round((timestamp - 25569) * SECONDS_IN_DAY)


def unix_to_hour(unix: int) -> int:
    "Convert unix timestamp to hour"
    return unix // 3600 % 24


def unix_to_timestamp(unix: int) -> float:
    "Convert unix timestamp to excel timestamp"
    return unix / SECONDS_IN_DAY + 25569


def set_sec_headers(*, response: Response):
    "Set security headers in the response"

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
    """Custom logger class that formats the log messages with colors.

    This class inherits from logging.Formatter and overrides the
    format method to add colors to the log messages. It also
    provides static methods to log messages with different
    log levels.

    It also provides a static method to raise an HTTPException
    from FastAPI and log the exception with the traceback.
    """

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
    def exception(*, status_code: int, detail: str, headers=None) -> NoReturn:
        logging.error(detail + "\n" + traceback.format_exc())
        raise HTTPException(
            status_code=status_code, detail=detail, headers=headers
        )
