from hashlib import sha256

from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession

from app.repos.users import UserRepo
from app.schemas.auth import SignUpSchema
from app.schemas.users import UserCreateSchema, UserResponseSchema


class UserService:
    def __init__(self, repo: UserRepo):
        self.repo = repo

    async def get(self, session: AsyncSession, email: EmailStr):
        result = await self.repo.get(session, email)
        return result.scalar_one_or_none()

    async def create(self, session: AsyncSession, data: SignUpSchema):
        hashed_password = sha256(data.password).digest()
        user_data = UserCreateSchema(email=data.email, password=hashed_password)
        return UserResponseSchema.model_validate(await self.repo.create(session, user_data.dict()))
