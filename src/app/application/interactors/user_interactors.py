from app.application.interfaces import user_interfaces, db_interfaces 
from app.application.dtos.user_dtos import NewUserDTO, UpdateUserDTO  
from app.domain.entities import user_entity
  
  
class GetUserInteractor:  
    def __init__(  
            self,  
            user_gateway: user_interfaces.UserReader,  
    ) -> None:  
        self._user_gateway = user_gateway  
  
    async def __call__(self, uuid: str) -> user_entity.UserDM | None:  
        return await self._user_gateway.read_by_uuid(uuid)  
  
  
class NewUserInteractor:  
    def __init__(  
            self,  
            db_session: db_interfaces.DBSession,  
            user_gateway: user_interfaces.UserSaver,  
    ) -> None:  
        self._db_session = db_session  
        self._user_gateway = user_gateway  

    async def __call__(self, dto: NewUserDTO) -> None:  
        user = user_entity.UserDM(  
            email=dto.email,
            password=dto.password,
            is_active=dto.is_active,
            is_superuser=dto.is_superuser
        )  
  
        await self._user_gateway.save(user)  
        await self._db_session.commit()  


class UpdateUserInteractor:  
    def __init__(  
            self,  
            db_session: db_interfaces.DBSession,  
            user_gateway: user_interfaces.UserUpdater,  
    ) -> None:  
        self._db_session = db_session  
        self._user_gateway = user_gateway  

    async def __call__(self, uuid: str, dto: UpdateUserDTO) -> None:
        user = user_entity.UserDM(  
            email=dto.email,
            password=dto.password,
            is_active=dto.is_active,
            is_superuser=dto.is_superuser
        )  
        await self._user_gateway.update(uuid, user)
        await self._db_session.commit()  

class DeleteUserInteractor:
    def __init__(
            self,
            db_session: db_interfaces.DBSession,
            user_gateway: user_interfaces.UserDeleter,
    ) -> None:
        self._db_session = db_session
        self._user_gateway = user_gateway

    async def __call__(self, uuid: str) -> None:
        await self._user_gateway.delete(uuid)
        await self._db_session.commit()
