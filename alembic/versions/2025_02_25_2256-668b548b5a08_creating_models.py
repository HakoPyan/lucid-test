"""Creating models

Revision ID: 668b548b5a08
Revises: 
Create Date: 2025-02-25 22:56:23.465069

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '668b548b5a08'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('email', sa.String(length=255), nullable=False),
    sa.Column('password', sa.BINARY(length=32), nullable=False),
    sa.Column('id', sa.BINARY(length=16), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('posts',
    sa.Column('text', sa.Text(), nullable=False),
    sa.Column('user_id', sa.BINARY(length=16), nullable=False),
    sa.Column('id', sa.BINARY(length=16), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('posts')
    op.drop_table('users')
    # ### end Alembic commands ###
