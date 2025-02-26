from uuid import UUID

from pydantic import BaseModel, EmailStr


class UserCreateSchema(BaseModel):
    email: EmailStr
    password: bytes


class UserResponseSchema(UserCreateSchema):
    id: UUID

    class Config:
        from_attributes = True
