from dataclasses import dataclass


@dataclass(frozen=True)
class DomainValueObject:
    def validate(self) -> None:
        pass

    def __post_init__(self) -> None:
        self.validate()
