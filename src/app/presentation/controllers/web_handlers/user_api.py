from dishka.integrations.fastapi import (
    FromDishka,
    inject,
)
from fastapi import APIRouter, HTTPException, Request, Response
from app.application.dtos.user_dtos import NewUserDTO
from app.application.interactors.user_interactors import GetUserByEmailInteractor, GetUserByUuidInteractor, NewUserInteractor
from app.application.interfaces.jwt_interface import JwtTokenInterface
from app.application.interfaces.password_hasher_interface import PasswordHasherInterface
from app.presentation.schemas.user_schemas import UserReadSchema, UserRegisterSchema, UserLoginSchema
from app.infrastructure.adapters.auth.utils import AddAccessTokenCookie, Authenticate, GetCurrentUser, GetToken

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
    password_hash: FromDishka[PasswordHasherInterface]
    ) -> None: 

    # check by email if exists
    user = await get_user_interactor(data.email)
    if user:
        raise HTTPException(status_code=400, detail="Email has already registered")
 
    # hashing password
    hashed_password = password_hash.get_password_hash(data.password)

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



@router.post("/login/")
@inject
async def login(
    data: UserLoginSchema,
    jwt_service: FromDishka[JwtTokenInterface],
    get_by_email_interactor: FromDishka[GetUserByEmailInteractor],
    password_hasher: FromDishka[PasswordHasherInterface],
    response: Response
    ) -> dict[str, str]:

    user = await Authenticate(get_by_email_interactor, password_hasher)(email=data.email, password=data.password)
    if not user:
        raise HTTPException(status_code=400)
  
    access_token = jwt_service.encode_access_token(user=user)[0]
    #add access token cookie
    await AddAccessTokenCookie()(response, access_token)
    return {"token": access_token}


@router.post("/me/")
@inject
async def get_user_data(
    request: Request,
    get_user_interactor: FromDishka[GetUserByUuidInteractor],
    jwt_service: FromDishka[JwtTokenInterface]
    ) -> UserReadSchema:

    token = await GetToken()(request)
    current_user = await GetCurrentUser(get_user_interactor, jwt_service)(token)
    return current_user