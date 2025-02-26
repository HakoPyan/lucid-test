from datetime import datetime
from uuid import UUID

from pydantic import EmailStr, BaseModel


class SignUpSchema(BaseModel):
    email: EmailStr
    password: bytes


class LogInSchema(SignUpSchema):
    ...
