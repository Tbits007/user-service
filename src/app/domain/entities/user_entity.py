from dataclasses import dataclass


@dataclass(slots=True)
class UserDM: # DM - Domain model
    id_: str 
    email: str 
    password: str 
    is_active: bool 
    is_superuser: bool