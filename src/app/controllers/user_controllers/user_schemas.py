from pydantic import BaseModel


class UserCreateSchema(BaseModel):
    email: str 
    password: str 
    is_active: bool 
    is_superuser: bool 