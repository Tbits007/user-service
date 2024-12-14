from dishka import Provider, Scope, provide

from app.application.interactors.auth_interactors import (
    RegisterInteractor,
    VerifyInteractor,
    LoginInteractor,
    PasswordResetInteractor,
    PasswordResetConfirmInteractor,   
)
from app.application.interfaces import password_hasher_interface
from app.infrastructure.adapters.jwt_processor_impl import JwtTokenProcessor
from app.infrastructure.adapters.password_hasher_impl import PasswordHasherImpl 
from app.application.interfaces import jwt_processor_interface


class AuthProvider(Provider):

    register_interactor = provide(RegisterInteractor, scope=Scope.REQUEST)
    verify_interactor = provide(VerifyInteractor, scope=Scope.REQUEST)
    login_interactor = provide(LoginInteractor, scope=Scope.REQUEST)
    password_reset_interactor = provide(PasswordResetInteractor, scope=Scope.REQUEST)
    password_reset_confirm_interactor = provide(PasswordResetConfirmInteractor, scope=Scope.REQUEST)

    password_hasher = provide(
        PasswordHasherImpl,
        scope=Scope.REQUEST,
        provides=password_hasher_interface.PasswordHasherInterface
    )

    jwt_token_processor = provide(
        JwtTokenProcessor,
        scope=Scope.REQUEST,
        provides=jwt_processor_interface.JwtProcessorInterface
    )
