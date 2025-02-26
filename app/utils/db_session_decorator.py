import logging
from collections.abc import Callable, Coroutine
from functools import wraps
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

log = logging.getLogger(__name__)


def managed_db_session(
    func: Callable[..., Any],
) -> Callable[[tuple[Any, ...], dict[str, Any]], Coroutine[Any, Any, Any]]:
    @wraps(func)
    async def wrapper(*args, **kwargs) -> Any:  # type: ignore
        db_session: AsyncSession = kwargs.get('db_session')  # type: ignore
        try:
            async with db_session.begin():
                result = await func(*args, **kwargs)
            log.debug('Got successful result. Commit DB changes.: %s', result)
            await db_session.commit()
            return result
        except Exception as exc:
            log.warning('Exception caught. Roll DB changes back.: %s', exc)
            await db_session.rollback()
            raise

    return wrapper
