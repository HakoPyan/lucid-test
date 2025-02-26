from typing import Annotated
from uuid import UUID

import jwt
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from app.core.config import env_secrets
from app.utils.exceptions import UnauthorizedError

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='auth/login/')


async def retrieve_user_id_from_token(token: Annotated[str, Depends(oauth2_scheme)]) -> UUID:
    try:
        payload = jwt.decode(token, env_secrets.JWT_SECRET_KEY, algorithms=env_secrets.JWT_ALGORITHMS)
    except Exception:
        raise UnauthorizedError()
    return UUID(payload.get('sub'))
