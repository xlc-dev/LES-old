"""Entrypoint for the application.

This is the file that needs to be run to start the application.

This file does the following:
    - Create the app factory
    - Print all available API routes
    - Run the app through Uvicorn

example: `python run.py`
"""

from os import system

from uvicorn import run

from app.app import create_app
import app.config as config  # `as` is needed for printing the docstring

# App factory
app = create_app()

# Make ANSI get processed everywhere properly
# to get pretty colors in the terminal
system("")


if __name__ == "__main__":
    print(config.__doc__)
    reload = False

    if config.settings.development:
        reload = True
        urls = [
            {"path": route.path, "name": route.name} for route in app.routes
        ]

        print("\033[1mAll routes:\033[0m\n")

        for url in urls:
            print(url)

        print(
            "\nDEVELOPMENT IS SET TO \033[1;31mTRUE.\033[0m "
            + "MAKE SURE THIS IS \033[1;31mNOT\033[0m IN PRODUCTION"
        )

    print(
        "\n======================================================="
        + "========================"
    )

    run(
        "run:app",
        reload=reload,
        host=config.settings.server_host,
        port=config.settings.port,
        use_colors=config.settings.uvcorn_colors,
        workers=config.settings.workers,
    )
