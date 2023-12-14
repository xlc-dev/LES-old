"""\033[1mApp settings:\033[0m

===============================================================================
\033[1mPossible environment variables:\033[0m
===============================================================================
\033[1m
  Option:           Type: Description:                                 Default:

\033[1m* Uvcorn:\033[0m
 - port:            Int:  Set port of server.                              8000
 - development:     Bool: Enables Development environment.                False
 - uvcorn_colors:   Bool: Allows Uvicorn to use colors or not.             True
 - workers:         Int:  Number of workers.                                  1
\033[1m* App:\033[0m
 - project_name:    Str:  The name of the application.                      LES
 - server_host:     Str:  The url of the server.                        0.0.0.0
 - api_prefix:      Str:  The prefix for every API route.                  /api
 - openapi_url:     Str:  The url to the JSON file for the docs.  /openapi.json
\033[1m* Database:\033[0m
 - database_url:    Str:  The database URL.               sqlite:///data/app.db
 - db_echo:         Bool: Enables printing of SQL statements.             False
===============================================================================
"""

from pydantic_settings import BaseSettings
from sqlmodel import create_engine


class Settings(BaseSettings):
    port: int = 8000
    development: bool = False
    uvcorn_colors: bool = True
    workers: int = 2

    project_name: str = "LES"
    server_host: str = "0.0.0.0"
    api_prefix: str = "/api"
    openapi_url: str = "/openapi.json"

    database_url: str = "sqlite:///data/app.db"
    db_echo: bool = False

    class Config:
        "Configuration for the setting class"
        # `.env.prod` takes priority over `.env`
        env_file = ".env", ".env.prod"
        env_file_encoding = "utf-8"


settings = Settings()  # type: ignore

connect_args = {"check_same_thread": False}
engine = create_engine(
    settings.database_url, echo=settings.db_echo, connect_args=connect_args
)
