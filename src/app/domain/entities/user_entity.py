from dataclasses import dataclass


@dataclass(slots=True)
class UserDM: # DM - Domain model
    uuid: str 
    email: str 
    password: str 
    is_active: bool 
    is_superuser: bool