import platform
from os import system

from uvicorn import run

from app.app import create_app
import app.config as config

# App factory
app = create_app()

# Make ANSI get processed everywhere properly
system("")


def get_all_urls():
    url_list = [
        {"path": route.path, "name": route.name} for route in app.routes
    ]
    return url_list


if __name__ == "__main__":
    print(config.__doc__)
    reload = False

    if config.settings.development:
        reload = True
        print(
            "DEVELOPMENT IS SET TO \033[1;31mTRUE.\033[0m "
            + "MAKE SURE THIS IS \033[1;31mNOT\033[0m IN PRODUCTION"
        )

    urls = get_all_urls()

    print("\nAll routes:\n")

    for url in urls:
        print(url)

    print(
        "\n======================================================="
        + "========================"
    )

    # Check if the OS is Linux or macOS and enable uvloop if true
    if platform.system() in ["Linux", "Darwin"]:
        loop = "uvloop"
    else:
        loop = None

    run(
        "run:app",
        reload=reload,
        loop=loop,
        host=config.settings.server_host,
        port=config.settings.port,
        use_colors=config.settings.uvcorn_colors,
        workers=config.settings.workers,
    )
