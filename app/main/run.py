from dishka import make_async_container
from dishka.integrations.faststream import setup_dishka
from faststream import FastStream

from app.main.config import Config
from app.main.ioc.providers.root import RootProvider
from app.main.ioc.providers.action import ActionProvider
from app.presentation.controllers.handlers import actions

# $env:PYTHONPATH="C:\\PythonProjects\\FastAPIprojects\\tracking-service\\src"
# faststream run --factory app.main.run:create_app


def create_production_app() -> FastStream:
    config = Config()
    _app = create_app()
    container = make_async_container(
        RootProvider(),
        ActionProvider(),
        context={Config: config},
    )
    setup_dishka(container, _app)
    return _app


def create_app() -> FastStream:   
    _app = FastStream()
    set_brokers(_app)
    return _app


def set_brokers(_app: FastStream) -> None:
    _app.set_broker(actions)