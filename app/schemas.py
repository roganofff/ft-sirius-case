from pydantic import BaseModel, EmailStr, constr, validator
from typing import Optional

class UserCreate(BaseModel):
    email: EmailStr
    password: constr(min_length=8, max_length=128)
    full_name: Optional[constr(strip_whitespace=True, min_length=2, max_length=50)] = None

    @validator("password")
    def password_complexity(cls, v):
        if not any(c.isdigit() for c in v):
            raise ValueError("Пароль должен содержать хотя бы одну цифру")
        if not any(c.isalpha() for c in v):
            raise ValueError("Пароль должен содержать хотя бы одну букву")
        return v
