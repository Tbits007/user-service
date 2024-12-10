from dishka.integrations.fastapi import (
    FromDishka,
    inject,
)
from fastapi import APIRouter, HTTPException
from app.application.dtos.user_dtos import NewUserDTO
from app.application.interactors.user_interactors import GetUserByEmailInteractor, NewUserInteractor
from app.controllers.user_controllers.user_schemas import UserRegisterSchema, UserLoginSchema
from app.infrastructure.oauth.hash import get_password_hash

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.post("/register/")
@inject
async def register(
    data: UserRegisterSchema,
    create_user_interactor: FromDishka[NewUserInteractor],
    get_user_interactor: FromDishka[GetUserByEmailInteractor],
    ) -> None:

    # check by email if exists
    user = await get_user_interactor(data.email)
    if user:
        raise HTTPException(status_code=400, detail="Email has already registered")
 
    # hashing password
    hashed_password = get_password_hash(data.password)

    # save user to db
    dto = NewUserDTO(
        email=data.email,
        password=hashed_password,
        is_active=data.is_active,
        is_superuser=data.is_superuser,
    )
    await create_user_interactor(dto)

    # send verify email 
    # ...



# @router.post("/login/")
# @inject
# async def login(
#     data: UserLoginSchema,
#     interactor: FromDishka[GetUserInteractor]
#     ) -> None:

#     #get user data
#     dto = GetUserDTO(
#         uuid=data.uuid
#     )
#     user_data = await interactor(dto)

#     #verify