from dataclasses import dataclass


@dataclass(slots=True)  
class CreateUserDTO:  
    email: str 
    username: str
    password: str 
    is_active: bool = True
    is_verified: bool = False
    is_superuser: bool = False


@dataclass(slots=True)  
class LoginUserDTO:  
    email: str 
    username: str