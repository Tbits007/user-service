from typing import AsyncGenerator

from dishka import Provider, Scope, provide, from_context
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.application.interfaces.email_sender_interface import EmailSender
from app.infrastructure.adapters.email_sender_impl import EmailSenderImpl
from app.infrastructure.database.database import new_session_maker
from app.main.config import Config


class RootProvider(Provider):
    config = from_context(provides=Config, scope=Scope.APP)

    @provide(scope=Scope.APP)
    def get_session_maker(self, config: Config) -> async_sessionmaker[AsyncSession]:
        return new_session_maker(config.postgres)

    @provide(scope=Scope.REQUEST)
    async def get_session(self, session_maker: async_sessionmaker[AsyncSession]) -> AsyncGenerator[AsyncSession, None]:
        async with session_maker() as session:
            yield session

    email_sender = provide(EmailSenderImpl, scope=Scope.REQUEST, provides=EmailSender)