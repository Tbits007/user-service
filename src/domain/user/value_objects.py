from src.domain.common.value_objects import DomainValueObject
from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class UserId(DomainValueObject):
    value: UUID


@dataclass(frozen=True)
class Username(DomainValueObject):
    value: str


@dataclass(frozen=True)
class UserPasswordHash(DomainValueObject):
    value: bytes

        

        