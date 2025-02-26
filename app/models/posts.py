import sqlalchemy as sa
from sqlalchemy.dialects.mysql import BINARY
from sqlalchemy.orm import relationship

from app.models import Base


class Post(Base):
    __tablename__ = 'posts'

    text = sa.Column(sa.Text, nullable=False)
    user_id = sa.Column(BINARY(16), sa.ForeignKey('users.id'), nullable=False)

    user = relationship('User', back_populates='posts')
