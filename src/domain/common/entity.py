from typing import TypeVar, Generic
from dataclasses import dataclass
from src.domain.common.value_objects import DomainValueObject

# Задаём обобщённый тип EntityId, ограниченный классом DomainValueObject
EntityId = TypeVar("EntityId", bound="DomainValueObject")


@dataclass
class DomainEntity(Generic[EntityId]):
    id_: EntityId
