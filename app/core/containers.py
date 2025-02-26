from operator import attrgetter

from dependency_injector import containers, providers
from fastapi import FastAPI
from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker, create_async_engine
from starlette.middleware import Middleware

from app import models
from app.core.config import config, env_secrets
from app.core.middleware import DBSessionMiddleware
from app.repos.posts import PostRepo
from app.repos.users import UserRepo
from app.services.posts import PostService
from app.services.users import UserService
from app.utils.exc_handlers import handle_already_exists_error, handler_unauthorized_error
from app.utils.exceptions import AlreadyExistsError, UnauthorizedError
from app.services.auth import AuthService
from app.services.jwt import JWTService


class AppContainer(containers.DeclarativeContainer):
    config = providers.Configuration(strict=True)
    env = providers.Configuration(strict=True, pydantic_settings=[env_secrets])

    db_engine: AsyncEngine = providers.Singleton(
        create_async_engine,
        url=env.DB_DSN,
        echo=False,
    )

    session_factory: async_sessionmaker = providers.Singleton(
        async_sessionmaker,
        db_engine,
        expire_on_commit=False,
        autoflush=True,
    )

    middlewares = providers.List(
        providers.Factory(
            Middleware,
            cls=DBSessionMiddleware,
            session_factory=session_factory,
        ),
    )

    app_factory: FastAPI = providers.Factory(
        FastAPI,
        root_path=env.API_ROOT_PATH,
        title=config.app.title,
        debug=config.app.debug,
        version=env.VERSION,
        openapi_url=config.docs.openapi_url,
        docs_url=config.docs.docs_url,
        redoc_url=config.docs.redoc_url,
        description=config.docs.description,
        middleware=middlewares,
        servers=config.app.servers,
        openapi_tags=config.app.openapi_tags,
        contact=config.app.contact,
        generate_unique_id_function=attrgetter('name'),
        exception_handlers={
            UnauthorizedError: handler_unauthorized_error,
            AlreadyExistsError: handle_already_exists_error,
        },
    )

    jwt_service = providers.Factory(
        JWTService,
        jwt_issuer=config.app.title,
        jwt_algorithms=config.jwt.algorithms,
        access_token_exp_delta=config.jwt.access_token_exp_delta,
    )

    user_repo = providers.Factory(
        UserRepo,
        model=models.User,
    )

    user_service = providers.Factory(
        UserService,
        repo=user_repo,
    )

    post_repo = providers.Factory(
        PostRepo,
        model=models.Post,
    )

    post_service = providers.Factory(
        PostService,
        repo=post_repo,
    )

    auth_service = providers.Factory(
        AuthService,
        jwt_service=jwt_service,
        user_service=user_service,
    )


app_container = AppContainer()
app_container.config.from_pydantic(config)
