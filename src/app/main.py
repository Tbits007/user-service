from dishka import make_async_container
from dishka.integrations import fastapi as fastapi_integration
from fastapi import FastAPI

from app.config import Config
from app.ioc import AppProvider
from app.controllers.user_controllers.user_api import router as user_router


config = Config()
container = make_async_container(AppProvider(), context={Config: config})


routers = (
    user_router, 
)


def get_fastapi_app() -> FastAPI:
    fastapi_app = FastAPI()

    for router in routers:
        fastapi_app.include_router(router)

    fastapi_integration.setup_dishka(container, fastapi_app)
    
    return fastapi_app


def get_app():
    fastapi_app = get_fastapi_app()
    
    return fastapi_app

# $env:PYTHONPATH="C:\\PythonProjects\\FastAPIprojects\\user-service\\src"
# uvicorn --factory app.main:get_app --reload