from abc import abstractmethod
from typing import Protocol


class DBSession(Protocol):
    @abstractmethod
    async def commit(self) -> None:
        """Закоммитить текущую транзакцию."""
        ...

    @abstractmethod
    async def flush(self) -> None:
        """Отправить изменения в базу данных без коммита."""
        ...