import os
from aiohttp.web import run_app

from app.web.app import setup_app


if __name__ == "__main__":
    run_app(
        setup_app(
            config_path=os.path.join(
                os.path.dirname(__file__),
                "config.yml",
            )
        ),
    )
