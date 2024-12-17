import pytest
from datetime import datetime, timedelta, timezone
from unittest.mock import patch
from app.domain.exceptions.access import AuthenticationError
from app.application.interfaces.jwt_processor_interface import TokenType
from app.infrastructure.adapters.jwt_processor_impl import JwtTokenProcessor


@pytest.fixture
def jwt_processor():
    return JwtTokenProcessor()


@pytest.fixture
def user_email():
    return "testuser@example.com"


@pytest.fixture
def mock_config():
    with patch('app.main.config.JWTConfig') as mock:
        mock.SECRET_KEY = "secret_key"
        mock.ACCESS_TOKEN_EXPIRES_MINUTES = 15
        mock.REFRESH_TOKEN_EXPIRES_MINUTES = 30
        mock.ALGORITHM = "HS256"
        yield mock


def test_create_access_token(jwt_processor, user_email):
    token = jwt_processor.create_access_token(user_email)
    assert isinstance(token, str)
    assert len(token) > 0


def test_create_password_reset_token(jwt_processor, user_email):
    token = jwt_processor.create_password_reset_token(user_email)
    assert isinstance(token, str)
    assert len(token) > 0


def test_create_refresh_token(jwt_processor, user_email):
    token = jwt_processor.create_refresh_token(user_email)
    assert isinstance(token, str)
    assert len(token) > 0


def test_verify_token_success(jwt_processor, user_email):
    # Create valid access token
    token = jwt_processor.create_access_token(user_email)
    
    # Verify the token
    payload = jwt_processor.verify_token(token, token_type=TokenType.ACCESS)
    
    assert payload == user_email


def test_verify_token_invalid_type(jwt_processor, user_email):
    # Create access token
    token = jwt_processor.create_access_token(user_email)
    
    # Verify the token with incorrect type
    with pytest.raises(AuthenticationError):
        jwt_processor.verify_token(token, token_type=TokenType.PASSWORD_RESET)


def test_verify_token_invalid_token(jwt_processor):
    # Test with invalid token
    invalid_token = "invalid_token"
    with pytest.raises(AuthenticationError):
        jwt_processor.verify_token(invalid_token)


def test_token_expiration(jwt_processor, user_email, mock_config):
    # Create an access token
    token = jwt_processor.create_access_token(user_email)
    
    # Simulate token expiration by altering the current time
    with patch('datetime.datetime') as mock_datetime:
        mock_datetime.now.return_value = datetime.now(timezone.utc) + timedelta(minutes=16)
        
        with pytest.raises(AuthenticationError):
            jwt_processor.verify_token(token)
