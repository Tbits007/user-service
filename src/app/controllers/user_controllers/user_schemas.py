from pydantic import BaseModel


class UserReadSchema(BaseModel):
    email: str 
    password: str 
    is_active: bool 
    is_superuser: bool 


class UserCreateSchema(BaseModel):
    email: str 
    password: str 
    is_active: bool 
    is_superuser: bool 