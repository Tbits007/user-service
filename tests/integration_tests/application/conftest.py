import pytest
from unittest.mock import AsyncMock
from app.application.interfaces import (
    user_interface,
    email_sender_interface,
    jwt_processor_interface,
    password_hasher_interface
)


@pytest.fixture
def mock_user_saver():
    return AsyncMock(user_interface.UserSaver)


@pytest.fixture
def mock_user_reader():
    return AsyncMock(user_interface.UserReader)


@pytest.fixture
def mock_user_updater():
    return AsyncMock(user_interface.UserUpdater)


@pytest.fixture
def mock_email_sender():
    return AsyncMock(email_sender_interface.EmailSender)


@pytest.fixture
def mock_jwt_processor():
    return AsyncMock(jwt_processor_interface.JwtProcessorInterface)


@pytest.fixture
def mock_password_hasher():
    return AsyncMock(password_hasher_interface.PasswordHasherInterface)
