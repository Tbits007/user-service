from datetime import timedelta, datetime, timezone
from typing import Self
import uuid

from jose import JWTError, jwt

from app.application.interfaces.jwt_interface import JwtTokenInterface
from app.config import Config
from app.domain.entities.user_entity import UserDM


class JwtTokenService(JwtTokenInterface):
    SUB = "sub"
    EXP = "exp"
    IAT = "iat"
    JTI = "jti"

    def __init__(self):
        self.config = Config()

    def encode_access_token(
        self,
        user: UserDM,
        minutes: int | None = None
        ) -> str:
        
        payload = {self.SUB: str(user.uuid), self.JTI: str(uuid.uuid4()), self.IAT: datetime.now(timezone.utc)}

        expire = datetime.now(timezone.utc) + timedelta(
            minutes=minutes or self.config.JWT_Config.ACCESS_TOKEN_EXPIRES_MINUTES
        )
        payload[self.EXP] = expire


        token = jwt.encode(payload, self.config.JWT_Config.SECRET_KEY, algorithm=self.config.JWT_Config.ALGORITHM),

        return token
    

    def decode_access_token(self, token: str) -> dict[str, str]:
        try:
            payload = jwt.decode(
                token, 
                self.config.JWT_Config.SECRET_KEY, 
                algorithms=[self.config.JWT_Config.ALGORITHM]
                )
            return payload
        except JWTError:
            raise Exception("Invalid token")



