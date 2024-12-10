from pydantic import BaseModel


class UserRegisterSchema(BaseModel):
    email: str 
    password: str 
    is_active: bool 
    is_superuser: bool 


class UserLoginSchema(BaseModel):
    email: str 
    password: str 



