from typing import AsyncIterable
from uuid import uuid4

from dishka import Provider, Scope, provide, AnyOf, from_context
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.application.interfaces import (
    user_interfaces,
    db_interfaces
)
from app.application.interactors.user_interactors import (
    DeleteUserInteractor,
    GetUserByEmailInteractor,
    GetUserByUuidInteractor,
    NewUserInteractor,
    UpdateUserInteractor
)
from app.application.interfaces.uuid_generator_interfaces import UUIDGenerator
from app.config import Config
from app.infrastructure.database import new_session_maker
from app.infrastructure.adapters.user_gateway import UserGateway


class AppProvider(Provider):
    config = from_context(provides=Config, scope=Scope.APP)

    @provide(scope=Scope.APP)
    def get_uuid_generator(self) -> UUIDGenerator:
        return uuid4

    @provide(scope=Scope.APP)
    def get_session_maker(self, config: Config) -> async_sessionmaker[AsyncSession]:
        return new_session_maker(config.postgres)

    @provide(scope=Scope.REQUEST)
    async def get_session(self, session_maker: async_sessionmaker[AsyncSession]) -> AsyncIterable[AnyOf[
        AsyncSession,
        db_interfaces.DBSession,
    ]]:
        async with session_maker() as session:
            yield session

    user_gateway = provide(
        UserGateway,
        scope=Scope.REQUEST,
        provides=AnyOf[
            user_interfaces.UserReader,
            user_interfaces.UserSaver,
            user_interfaces.UserUpdater,
            user_interfaces.UserDeleter
            ]
    )

    create_new_user_interactor = provide(NewUserInteractor, scope=Scope.REQUEST)
    get_user_by_uuid_interactor = provide(GetUserByUuidInteractor, scope=Scope.REQUEST)
    get_user_by_email_interactor = provide(GetUserByEmailInteractor, scope=Scope.REQUEST)
    update_user_interactor = provide(UpdateUserInteractor, scope=Scope.REQUEST)
    delete_user_interactor = provide(DeleteUserInteractor, scope=Scope.REQUEST)