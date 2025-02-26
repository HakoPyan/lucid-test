from http import HTTPStatus

from fastapi import Request
from fastapi.responses import JSONResponse

from app.utils.exceptions import AlreadyExistsError, UnauthorizedError


async def handle_already_exists_error(request: Request, exc: AlreadyExistsError) -> JSONResponse:
    return JSONResponse(status_code=HTTPStatus.CONFLICT, content={'detail': exc.args[0]})


def handler_unauthorized_error(request: Request, exc: UnauthorizedError) -> JSONResponse:
    return JSONResponse(status_code=HTTPStatus.UNAUTHORIZED, content={'detail': exc.args[0]})
