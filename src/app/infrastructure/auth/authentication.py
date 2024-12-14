from fastapi import Request, HTTPException, Depends

from app.domain.exceptions.access import AuthenticationError
from app.infrastructure.adapters.jwt_processor_impl import JwtTokenProcessor, TokenType
from app.main.config import JWTConfig


class JwtTokenAuthentication:
    def __init__(self, config: JWTConfig):
        self.jwt_token_processor = JwtTokenProcessor(
            secret=config.SECRET_KEY,
            access_token_expires=config.ACCESS_TOKEN_EXPIRES_MINUTES,
            refresh_token_expires=config.REFRESH_TOKEN_EXPIRES_MINUTES,
            algorithm=config.ALGORITHM,
        )

    async def __call__(self, request: Request) -> str:
        authorization = request.headers.get("Authorization")
        if not authorization or not authorization.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Unauthorized")
        try:
            email = self.jwt_token_processor.verify_token(
                token=authorization.split("Bearer ")[1],
                token_type=TokenType.ACCESS,
            )
            return email
        except AuthenticationError:
            raise HTTPException(status_code=401, detail="Unauthorized")


def get_user_email(
        email: str = Depends(JwtTokenAuthentication(JWTConfig()))
) -> str:
    return email
