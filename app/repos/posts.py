from uuid import UUID

from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession


class PostRepo:
    def __init__(self, model):
        self.model = model

    async def list(self, session: AsyncSession, user_id: UUID):
        query = select(self.model).where(self.model.user_id == user_id.bytes)
        results = await session.execute(query)
        return results.scalars()

    async def create(self, session, data):
        instance = self.model(**data)
        session.add(instance)
        await session.flush()
        await session.refresh(instance)
        return instance

    async def delete(self, session: AsyncSession, user_id: bytes, post_id: bytes):
        query = delete(self.model).where(self.model.id == post_id, self.model.user_id == user_id)
        return await session.execute(query)
