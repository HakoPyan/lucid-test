import sqlalchemy as sa
from sqlalchemy.dialects.mysql import BINARY
from sqlalchemy.orm import relationship

from app.models import Base


class User(Base):
    __tablename__ = 'users'

    email = sa.Column(sa.String(255), unique=True, nullable=False)
    password = sa.Column(BINARY(32), nullable=False)

    posts = relationship('Post', back_populates='user')
