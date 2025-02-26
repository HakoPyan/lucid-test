from http import HTTPStatus
from uuid import UUID

from cachetools import TTLCache
from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.auth import retrieve_user_id_from_token
from app.core.containers import AppContainer
from app.dependencies import db_session_dependency
from app.schemas.posts import PostCreateRequestSchema
from app.services.posts import PostService
from app.utils.db_session_decorator import managed_db_session

router = APIRouter(tags=['posts'])

cache = TTLCache(maxsize=1000, ttl=300)


@router.get('/', name='posts:list')
@managed_db_session
@inject
async def list_posts(
    user_id: UUID = Depends(retrieve_user_id_from_token),
    db_session: AsyncSession = Depends(db_session_dependency),
    post_service: PostService = Depends(Provide[AppContainer.post_service]),
):
    """Endpoint for listing user posts."""
    if user_id in cache:
        return cache[user_id]

    response = await post_service.list(db_session, user_id)
    cache[user_id] = response
    return response


@router.post('/', name='posts:create', status_code=HTTPStatus.CREATED)
@managed_db_session
@inject
async def create(
    data: PostCreateRequestSchema,
    user_id: UUID = Depends(retrieve_user_id_from_token),
    db_session: AsyncSession = Depends(db_session_dependency),
    post_service: PostService = Depends(Provide[AppContainer.post_service]),
):
    """Endpoint for creating user posts."""
    cache.pop(user_id, None)
    return await post_service.create(db_session, data, user_id)


@router.delete('/{post_id:uuid}/', name='posts:delete', status_code=HTTPStatus.NO_CONTENT)
@managed_db_session
@inject
async def delete(
    post_id: UUID,
    user_id: UUID = Depends(retrieve_user_id_from_token),
    db_session: AsyncSession = Depends(db_session_dependency),
    post_service: PostService = Depends(Provide[AppContainer.post_service]),
):
    """Endpoint for deleting user posts."""
    return await post_service.delete(db_session, user_id, post_id)
