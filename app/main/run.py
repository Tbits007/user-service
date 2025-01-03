from contextlib import asynccontextmanager

from dishka import make_async_container
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI
from faststream.kafka.fastapi import KafkaBroker

from app.main.config import Config
from app.main.ioc.providers.auth import AuthProvider
from app.main.ioc.providers.root import RootProvider
from app.main.ioc.providers.user import UserProvider
from app.presentation.controllers.http.auth.router import auth_router
from app.presentation.controllers.http.user.router import user_router

# uvicorn --factory app.main.run:create_production_app --reload
# black src/app


def create_production_app() -> FastAPI:
    config = Config()
    broker = KafkaBroker(config.kafka_.uri())
    include_broker_routers(broker)
    _app = create_app()
    container = make_async_container(
        RootProvider(),
        AuthProvider(),
        UserProvider(),
        context={Config: config, KafkaBroker: broker},
    )
    setup_dishka(container, _app)
    return _app


@asynccontextmanager
async def lifespan(_app: FastAPI):
    yield


def create_app() -> FastAPI:
    _app = FastAPI(lifespan=lifespan)
    include_fastapi_routers(_app)
    return _app


def include_broker_routers(broker: KafkaBroker):
    broker.include_router(auth_router)


def include_fastapi_routers(_app: FastAPI) -> None:
    _app.include_router(
        auth_router,
        prefix="/auth",
        tags=[
            "auth",
        ],
    )
    _app.include_router(
        user_router,
        prefix="/user",
        tags=[
            "user",
        ],
    )
