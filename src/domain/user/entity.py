from typing import Self
from src.domain.user.value_objects import UserId, UserPasswordHash, Username
from src.domain.common.entity import DomainEntity
from domain.user.enums import UserRoleEnum
from dataclasses import dataclass
from uuid import UUID


@dataclass(kw_only=True)
class User(DomainEntity[UserId]):
    username: Username
    password_hash: UserPasswordHash
    roles: set[UserRoleEnum]
    is_active: bool

    @classmethod
    def create(cls, *, user_id: UUID, username: str, password_hash: bytes) -> Self:
        return cls(
            id_=UserId(user_id),
            username=Username(username),
            password_hash=UserPasswordHash(password_hash),
            roles={UserRoleEnum.USER},
            is_active=True,
        )

    def activate(self) -> None:
        self.is_active = True

    def inactivate(self) -> None:
        self.is_active = False

    def grant_admin(self) -> None:
        self.roles.add(UserRoleEnum.ADMIN)

    def revoke_admin(self) -> None:
        self.roles.discard(UserRoleEnum.ADMIN)