# from datetime import datetime, timedelta, timezone
# from fastapi import Request, Response
# from app.application.interactors.user_interactors import GetUserByEmailInteractor, GetUserByUuidInteractor
# from app.application.interfaces.jwt_processor_interface import JwtTokenInterface
# from app.application.interfaces.password_hasher_interface import PasswordHasherInterface
# from app.config import Config
# from app.domain.entities import user_entity


# # Класс для аутентификации пользователя
# class Authenticate:
#     def __init__(
#             self,
#             get_by_email_interactor: GetUserByEmailInteractor,
#             password_hasher: PasswordHasherInterface
#         ) -> None:
#         self.get_by_email_interactor = get_by_email_interactor
#         self.password_haser = password_hasher

#     async def __call__(self, email: str, password: str) -> user_entity.UserDM | None:
#         user = await self.get_by_email_interactor(email=email)
#         if not user or not self.password_haser.verify_password(password, user.password):
#             return None
#         return user


# # Класс для получения токена из cookies
# class GetToken:
#     def __init__(self, token_name: str = "access_token"):
#         self.token_name = token_name

#     async def __call__(self, request: Request) -> str:
#         token = request.cookies.get(self.token_name)
#         if not token:
#             raise Exception
#         return token


# # Класс для получения текущего пользователя
# class  GetCurrentUser:
#     def __init__(
#             self,
#             get_user_interactor: GetUserByUuidInteractor,
#             jwt_service: JwtTokenInterface
#         ) -> None:
#         self.get_user_interactor = get_user_interactor
#         self.jwt_service = jwt_service


#     async def __call__(self, token: str) -> user_entity.UserDM:
#         payload = self.jwt_service.decode_access_token(token)

#         expire: str = payload.get("exp")
#         if not expire or int(expire) < int(datetime.now(timezone.utc).timestamp()):
#             raise Exception
        
#         user_uuid: str = payload.get("sub")
#         if not user_uuid:
#             raise Exception
        
#         user = await self.get_user_interactor(uuid=user_uuid)
#         if not user:
#             raise Exception
        
#         return user


# # Класс для добавления Cookie в браузер
# class AddAccessTokenCookie:
#     def __init__(self):
#         self.config = Config()

        
#     async def __call__(self, response: Response, token: str):
#         exp = datetime.now(timezone.utc) + timedelta(minutes=self.config.JWT_Config.ACCESS_TOKEN_EXPIRES_MINUTES)
#         exp = exp.replace(tzinfo=timezone.utc)

#         response.set_cookie(
#             key="access_token",
#             value=token,
#             expires=int(exp.timestamp()),
#             httponly=True,
#         )

