from typing import cast

from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession


def db_session_dependency(request: Request) -> AsyncSession:
    return cast(AsyncSession, request.scope['db_session'])
