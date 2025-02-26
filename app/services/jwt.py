import logging
import sys
from datetime import datetime, timedelta
from typing import Any
from uuid import UUID

import jwt
from fastapi.security import HTTPBearer

from app.core.config import env_secrets

log = logging.getLogger(__name__)


bearer_security_scheme = HTTPBearer(auto_error=False)


if not env_secrets.JWT_SECRET_KEY:  # pragma: no cover
    log.error('JWT_SECRET_KEY environment variable must be set. Exiting.')
    sys.exit(1)


class JWTService:
    def __init__(
        self,
        jwt_issuer: str,
        jwt_algorithms: list[str],
        access_token_exp_delta: timedelta,
    ):
        self.jwt_issuer = jwt_issuer
        self.jwt_algorithms = jwt_algorithms
        self.access_token_exp_delta = access_token_exp_delta

    def generate_access_token(self, user_id: bytes):
        when = datetime.utcnow()
        return self.encode_token({
            'sub': str(UUID(bytes=user_id)),
            'iss': self.jwt_issuer,
            'iat': when,
            'exp': when + self.access_token_exp_delta,
        })

    @staticmethod
    def encode_token(payload: dict[str, Any]) -> str:
        return jwt.encode(payload=payload, key=env_secrets.JWT_SECRET_KEY, algorithm=env_secrets.JWT_ALGORITHMS[0])

    def decode_token(self, token: str) -> dict[str, Any]:
        return jwt.decode(jwt=token, key=env_secrets.JWT_SECRET_KEY, algorithms=self.jwt_algorithms)
