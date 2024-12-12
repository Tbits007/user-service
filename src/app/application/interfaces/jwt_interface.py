from typing import Self, Protocol
from abc import abstractmethod
from app.domain.entities.user_entity import UserDM


class JwtTokenInterface(Protocol):
    @abstractmethod
    def encode_access_token(self, user: UserDM, minutes: int | None = None) -> str:
        ...
    
    @abstractmethod
    def decode_access_token(self, token: str) -> dict[str]:
        ...
