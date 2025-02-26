from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.repos.posts import PostRepo
from app.schemas.posts import PostCreateRequestSchema, PostReadResponseSchema, MultiplePostResponseSchema


class PostService:
    def __init__(self, repo: PostRepo):
        self.repo = repo

    async def list(self, session: AsyncSession, user_id: UUID):
        posts = await self.repo.list(session, user_id)
        return MultiplePostResponseSchema(results=[PostReadResponseSchema.model_validate(p) for p in posts])

    async def create(self, session: AsyncSession, data: PostCreateRequestSchema, user_id: UUID):
        post = await self.repo.create(session, {**data.dict(), 'user_id': user_id.bytes})
        return PostReadResponseSchema.model_validate(post)

    async def delete(self, session: AsyncSession, user_id: UUID, post_id: UUID):
        return await self.repo.delete(session, user_id.bytes, post_id.bytes)
