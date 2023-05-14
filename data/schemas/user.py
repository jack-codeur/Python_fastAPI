from pydantic import BaseModel, Field,EmailStr
from typing import Optional

class UserBase(BaseModel):
    first_name: str
    last_name: str
    phone: str
    password:str
    email: EmailStr
    def validate_email(cls, v):
        if r'^[\w\.-]+@[\w\.-]+\.\w{2,}$' not in v:
            raise ValueError('l\'adresse email n\'est pas valide')
        return v
    def json(self, *args, **kwargs):
        return self.dict(*args, **kwargs)

class UserCreate(UserBase):
    id: Optional[str] = Field(None)

class UserUpdate(UserBase):
    id:str
    password: Optional[str] = Field(None)
    email: Optional[str] = Field(None)
    phone: Optional[str] = Field(None)

class LoginData(BaseModel):
    login: str
    password: str

class UserDelete(UserBase):
    id:str

class User(UserBase):
    id:str
