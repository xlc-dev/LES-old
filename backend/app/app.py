import os
import time
import logging
from pathlib import Path

from fastapi import FastAPI, Request, Depends

# from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.gzip import GZipMiddleware

from app.config import settings
from app.utils import create_db_and_tables, set_sec_headers

from app.core.routers import (
    seeder_router,
    simulation_router,
    twinworld_router,
    costmodel_router,
)


def create_app() -> FastAPI:
    """Application factory for API.

    This factory does the following:
        - Enable CORS
        - Setup Logging
        - Include routers
        - Startup Events
        - Setup documentation
    """

    tags_metadata = [
        {
            "name": "Simulate",
            "description": "Simulate the twinworld",
        },
        {
            "name": "Twinworld",
            "description": "Twinworld API",
        },
        {
            "name": "Costmodel",
            "description": "Costmodel API",
        },
        {
            "name": "Seed",
            "description": "Seed the database with data",
        },
    ]

    app = FastAPI(
        title=settings.project_name,
        description=f"API for the {settings.project_name} app",
        version="0.1",
        openapi_tags=tags_metadata,
        openapi_url=settings.openapi_url if settings.development else None,
        redoc_url=None,
        swagger_ui_parameters={"docExpansion": "none"},
        dependencies=[Depends(set_sec_headers)],
    )

    # TODO: CORS
    if settings.development:
        app.add_middleware(TrustedHostMiddleware, allowed_hosts=["localhost"])
    else:
        app.add_middleware(TrustedHostMiddleware, allowed_hosts=["localhost"])

    origins = [settings.server_host]

    # app.add_middleware(HTTPSRedirectMiddleware)
    app.add_middleware(GZipMiddleware)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PATCH", "DELETE"],
        allow_headers=[
            "Access-Control-Allow-Headers",
            "Accept-Encoding",
            "Content-Type",
            "Authorization",
            "Access-Control-Allow-Origin",
        ],
        expose_headers=[],
    )

    if settings.development:

        @app.middleware("http")
        async def add_process_time_header(request: Request, call_next):
            start_time = time.time()
            response = await call_next(request)
            process_time = time.time() - start_time
            response.headers["X-Process-Time"] = str(process_time)
            return response

    folder = os.path.join(Path().resolve(), "data/logs")
    if not os.path.exists(folder):
        os.makedirs(folder)

    if settings.development:
        logging.basicConfig(
            filename=f"{folder}/FastAPI.log", level=logging.DEBUG
        )
    else:
        logging.basicConfig(
            filename=f"{folder}/FastAPI.log", level=logging.WARNING
        )

    app.include_router(
        simulation_router.router,
        prefix=f"{settings.api_prefix}/simulate",
        tags=["Simulate"],
    )

    app.include_router(
        twinworld_router.router,
        prefix=f"{settings.api_prefix}/twinworld",
        tags=["Twinworld"],
    )

    app.include_router(
        costmodel_router.router,
        prefix=f"{settings.api_prefix}/costmodel",
        tags=["Costmodel"],
    )

    if settings.development:
        app.include_router(
            seeder_router.router,
            prefix=f"{settings.api_prefix}/seed",
            tags=["Seed"],
        )

    @app.on_event("startup")
    def on_startup():
        "Create DB and tables on startup"
        create_db_and_tables()

    return app
