import asyncio

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from api import router as root_router
from core.models import init as init_database
from settings import config_parameters


def create_app() -> FastAPI:
    if config_parameters.IS_PROD:
        app = FastAPI(
            title="X10-Backend",
            debug=not config_parameters.IS_PROD,
            docs_url=None,
            redoc_url=None,
            openapi_url=None,
        )
    else:
        app = FastAPI(
            title="X10-Backend",
            debug=not config_parameters.IS_PROD,
        )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["*"],
    )
    return app


try:
    import uvloop

    uvloop.install()
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
except Exception:
    pass
server = create_app()
server.include_router(root_router, prefix="/api")
init_database(server)
