

from pydantic import BaseModel, EmailStr


class UserRequestDTO(BaseModel):
    email: EmailStr
    password: str
