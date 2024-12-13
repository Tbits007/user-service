from app.application.interfaces import user_interface
from app.domain.entities.user_entity import UserDM


class GetUserInteractor:  
    def __init__(  
            self,  
            user_gateway: user_interface.UserReader,  
    ) -> None:  
        self._user_gateway = user_gateway  
  
    async def __call__(self, email: str) -> UserDM | None:  
        return await self._user_gateway.read_by_email(email)  


class UpdateUserInteractor:  
    def __init__(  
            self,  
            user_gateway: user_interface.UserUpdater,  
    ) -> None:  
        self._user_gateway = user_gateway  

    async def __call__(self, email: str, update_data: dict) -> None:
        return await self._user_gateway.update(email, update_data)

# class NewUserInteractor:  
#     def __init__(  
#             self,  
#             db_session: db_interface.DBSession,  
#             user_gateway: user_interface.UserSaver,
#             uuid_generator: uuid_generator_interfaces.UUIDGenerator,  
#     ) -> None:  
#         self._db_session = db_session  
#         self._user_gateway = user_gateway  
#         self._uuid_generator = uuid_generator

#     async def __call__(self, dto: NewUserDTO) -> None:
#         uuid = str(self._uuid_generator())  
#         user = user.UserDM(
#             uuid=uuid,  
#             email=dto.email,
#             password=dto.password,
#             is_active=dto.is_active,
#             is_superuser=dto.is_superuser
#         )  
  
#         await self._user_gateway.save(user)  
#         await self._db_session.commit()  
