from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.types import ASGIApp
from starlette.types import Receive
from starlette.types import Scope
from starlette.types import Send


class DBSessionMiddleware:
    def __init__(self, app: ASGIApp, session_factory: async_sessionmaker[AsyncSession]):
        self.app = app
        self.session_factory = session_factory

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope['type'] == 'http':
            scope['db_session'] = self.session_factory()
            try:
                await self.app(scope, receive, send)
            finally:
                db_session = scope.pop('db_session', None)
                if db_session is not None:
                    await db_session.close()
            return
        await self.app(scope, receive, send)
