from dishka.integrations.fastapi import (
    FromDishka,
    inject,
)
from fastapi import APIRouter
from app.application.dtos.user_dtos import NewUserDTO
from app.application.interactors.user_interactors import NewUserInteractor
from app.controllers.user_controllers.user_schemas import UserCreateSchema

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.post("/create_user/")
@inject
async def create_user(
    data: UserCreateSchema,
    interactor: FromDishka[NewUserInteractor]
    ):

    dto = NewUserDTO(
        email=data.email,
        password=data.password,
        is_active=data.is_active,
        is_superuser=data.is_superuser,
    )
    await interactor(dto)
    return {"msg": "bebra"}
