from dataclasses import dataclass  


@dataclass(slots=True)  
class NewUserDTO:  
    email: str 
    password: str 
    is_active: bool 
    is_superuser: bool 