from http import HTTPStatus

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.containers import AppContainer
from app.dependencies import db_session_dependency
from app.schemas.auth import SignUpSchema, LogInSchema
from app.services.auth import AuthService
from app.utils.db_session_decorator import managed_db_session

router = APIRouter(tags=['auth'])


@router.post('/sign-up/', name='auth:sign-up', status_code=HTTPStatus.CREATED)
@managed_db_session
@inject
async def sign_up(
    data: SignUpSchema,
    db_session: AsyncSession = Depends(db_session_dependency),
    auth_service: AuthService = Depends(Provide[AppContainer.auth_service]),
):
    return await auth_service.sign_up(db_session, data)


@router.post('/login/', name='auth:login')
@managed_db_session
@inject
async def login(
    data: LogInSchema,
    db_session: AsyncSession = Depends(db_session_dependency),
    auth_service: AuthService = Depends(Provide[AppContainer.auth_service]),
):
    return await auth_service.login(db_session, data)
