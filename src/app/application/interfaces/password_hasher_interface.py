from typing import Protocol
from abc import abstractmethod


class PasswordHasherInterface(Protocol):
    @abstractmethod
    def get_password_hash(self, password: str) -> str:
        ...
    
    @abstractmethod
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        ...
