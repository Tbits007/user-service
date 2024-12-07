from abc import abstractmethod
from typing import Protocol

from app.domain.entities.user_entity import UserDM


class UserSaver(Protocol):
    @abstractmethod
    async def save(self, user: UserDM) -> None:
        ...


class UserReader(Protocol):
    @abstractmethod
    async def read_by_uuid(self, uuid: str) -> UserDM | None:
        ...


class DBSession(Protocol):
    @abstractmethod
    async def commit(self) -> None:
        """Закоммитить текущую транзакцию."""
        ...

    @abstractmethod
    async def flush(self) -> None:
        """Отправить изменения в базу данных без коммита."""
        ...