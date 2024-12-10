from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import text

from app.application.interfaces.user_interfaces import UserReader, UserSaver, UserUpdater, UserDeleter
from app.domain.entities.user_entity import UserDM


class UserGateway(
    UserReader,
    UserSaver,
    UserUpdater,
    UserDeleter,
):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def read_by_uuid(self, uuid: str) -> UserDM | None:
        query = text("SELECT * FROM users WHERE uuid = :uuid")
        result = await self._session.execute(
            statement=query,
            params={"uuid": uuid},
        )
        row = result.fetchone()
        if not row:
            return None
        return UserDM(
            uuid=row.uuid,
            email=row.email,
            password=row.password,
            is_active=row.is_active,
            is_superuser=row.is_superuser
        )

    async def read_by_email(self, email: str) -> UserDM | None:
        query = text("SELECT * FROM users WHERE email = :email")
        result = await self._session.execute(
            statement=query,
            params={"email": email},
        )
        row = result.fetchone()
        if not row:
            return None
        return UserDM(
            uuid=row.uuid,
            email=row.email,
            password=row.password,
            is_active=row.is_active,
            is_superuser=row.is_superuser
        )

    async def save(self, user: UserDM) -> None:
        query = text(
            """
            INSERT INTO users (uuid, email, password, is_active, is_superuser)
            VALUES (:uuid, :email, :password, :is_active, :is_superuser)"""
            )
        await self._session.execute(
            statement=query,
            params={
                "uuid": user.uuid,
                "email": user.email,
                "password": user.password,
                "is_active": user.is_active,
                "is_superuser": user.is_superuser
            },
        )

    async def update(self, uuid: str, user: UserDM) -> UserDM | None:
        # Начальная часть запроса
        base_query = "UPDATE users SET "
        query_parts = []
        params = {"uuid": uuid}  # Параметры для SQL-запроса

        # Добавляем только те поля, которые не None
        if user.email is not None:
            query_parts.append("email = :email")
            params["email"] = user.email

        if user.password is not None:
            query_parts.append("password = :password")
            params["password"] = user.password

        if user.is_active is not None:
            query_parts.append("is_active = :is_active")
            params["is_active"] = user.is_active

        if user.is_superuser is not None:
            query_parts.append("is_superuser = :is_superuser")
            params["is_superuser"] = user.is_superuser

        # Если нечего обновлять, возвращаем None
        if not query_parts:
            return None

        # Формируем полный SQL-запрос
        query = text(
            base_query + ", ".join(query_parts) + " WHERE uuid = :uuid RETURNING uuid, email, password, is_active, is_superuser"
        )

        # Выполняем запрос
        result = await self._session.execute(
            statement=query,
            params=params,
        )

        # Получаем обновлённую строку
        row = result.fetchone()
        if not row:
            return None

        # Возвращаем обновлённый объект UserDM
        return UserDM(
            uuid=row.uuid,
            email=row.email,
            password=row.password,
            is_active=row.is_active,
            is_superuser=row.is_superuser
        )

    async def delete(self, uuid: str) -> None:
        # Формируем SQL-запрос на удаление
        query = text("DELETE FROM users WHERE uuid = :uuid")

        # Выполняем запрос
        await self._session.execute(
            statement=query,
            params={"uuid": uuid},
        )