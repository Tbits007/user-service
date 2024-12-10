from dataclasses import dataclass


@dataclass(slots=True)  
class NewUserDTO:  
    email: str 
    password: str 
    is_active: bool 
    is_superuser: bool 


@dataclass(slots=True)  
class UpdateUserDTO:
    email: str | None = None
    password: str | None = None
    is_active: bool | None = None
    is_superuser: bool | None = None


@dataclass(slots=True)
class GetUserByUuidDTO:
    uuid: str


@dataclass(slots=True)
class GetUserByEmailDTO:
    email: str