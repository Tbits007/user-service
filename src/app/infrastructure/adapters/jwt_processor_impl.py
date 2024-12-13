from datetime import timedelta, datetime, timezone
from jose import jwt, JWTError

from app.domain.exceptions.access import AuthenticationError
from app.application.interfaces.jwt_processor_interface import JwtProcessorInterface, Algorithm, TokenType


class JwtTokenProcessor(JwtProcessorInterface):
    def __init__(
            self,
            secret: str,
            access_token_expires: timedelta,
            refresh_token_expires: timedelta,
            algorithm: Algorithm
    ) -> None:
        self.secret = secret
        self.access_token_expires = access_token_expires
        self.refresh_token_expires = refresh_token_expires
        self.algorithm = algorithm

    def create_access_token(self, user_email: str) -> str:
        issued_at = datetime.now(timezone.utc)
        expires = issued_at + self.access_token_expires
        to_encode = {
            "exp": expires,
            "iat": issued_at,
            "sub": user_email,
            "type": TokenType.ACCESS.value,
        }
        return jwt.encode(
            to_encode, self.secret, algorithm=self.algorithm,
        )

    def create_password_reset_token(self, user_email: str) -> str:
        issued_at = datetime.now(timezone.utc)
        expires = issued_at + self.access_token_expires
        to_encode = {
            "exp": expires,
            "iat": issued_at,
            "sub": user_email,
            "type": TokenType.PASSWORD_RESET.value,
        }
        return jwt.encode(
            to_encode, self.secret, algorithm=self.algorithm,
        )

    def create_refresh_token(self, user_email: str) -> str:
        issued_at = datetime.now(timezone.utc)
        expires = issued_at + self.refresh_token_expires
        to_encode = {
            "exp": expires,
            "iat": issued_at,
            "sub": user_email,
            "type": TokenType.REFRESH.value,
        }
        return jwt.encode(
            to_encode, self.secret, algorithm=self.algorithm,
        )

    def verify_token(self, token: str, token_type: TokenType | None = None) -> str | None:
        try:
            payload = jwt.decode(
                token, self.secret, algorithms=[self.algorithm],
            )
            if token_type and payload.get("type") != token_type.value:
                raise AuthenticationError("Invalid token type")
            return payload["sub"]
        except JWTError:
            raise AuthenticationError



