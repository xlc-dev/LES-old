from uvicorn import run
from os import system

import app.config as config
from app.app import create_app

# App factory
app = create_app()

# Make ASNI get processed everywhere properly
system("")


def get_all_urls():
    url_list = [{"path": route.path, "name": route.name} for route in app.routes]
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

    # urls = get_all_urls()

    # print('\nAll routes:\n')

    # for url in urls:
    #     print(url)

    print(
        "\n======================================================="
        + "========================"
    )

    run(
        "run:app",
        host=config.settings.server_host,
        port=config.settings.port,
        use_colors=config.settings.uvcorn_colors,
        reload=reload,
        # loop="uvloop",
        workers=2,
    )
