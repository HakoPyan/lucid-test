from uuid import uuid4

import sqlalchemy as sa
from sqlalchemy.dialects.mysql import BINARY
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    __abstract__ = True

    id = sa.Column(BINARY(16), primary_key=True, default=lambda: uuid4().bytes)
