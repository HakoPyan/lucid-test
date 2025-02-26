from hashlib import sha256

from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.auth import SignUpSchema, LogInSchema
from app.services.jwt import JWTService
from app.services.users import UserService
from app.utils.exceptions import AlreadyExistsError, UnauthorizedError


class AuthService:
    def __init__(self, jwt_service: JWTService, user_service: UserService):
        self.jwt_service = jwt_service
        self.user_service = user_service

    async def login(self, db_session: AsyncSession, data: LogInSchema):
        existing_user = await self.user_service.get(db_session, data.email)
        if not existing_user:
            raise UnauthorizedError()

        if sha256(data.password).digest() == existing_user.password:
            return self.jwt_service.generate_access_token(user_id=existing_user.id)

        raise UnauthorizedError()

    async def sign_up(self, db_session: AsyncSession, data: SignUpSchema):
        existing_user = await self.user_service.get(db_session, data.email)
        if existing_user:
            raise AlreadyExistsError('User already exists', 'user_already_exists')
        user = await self.user_service.create(db_session, data)
        return self.jwt_service.generate_access_token(user_id=user.id)
