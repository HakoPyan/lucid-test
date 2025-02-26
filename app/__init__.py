from fastapi import APIRouter, FastAPI

from app.core.config import config
from app.core.containers import app_container
from app.views.auth import router as auth_router
from app.views.posts import router as posts_router

api_wire = ['app.views.auth', 'app.views.posts']


def get_router() -> APIRouter:
    router = APIRouter()
    router.include_router(auth_router, prefix='/auth')
    router.include_router(posts_router, prefix='/posts')
    return router


def create_app() -> FastAPI:
    app_container.wire(packages=api_wire)
    app = app_container.app_factory()
    router = get_router()
    app.include_router(router)
    return app
