from abc import ABC
from dataclasses import dataclass


@dataclass(frozen=True)
class DomainValueObject(ABC):
    
    def validate(self) -> None:
        pass

    def __post_init__(self) -> None:
        self.validate()
