from pydantic import EmailStr
from sqlalchemy import select


class UserRepo:
    def __init__(self, model):
        self.model = model

    async def get(self, session, email: EmailStr):
        query = select(self.model).where(self.model.email == email)
        return await session.execute(query)

    async def create(self, session, data):
        instance = self.model(**data)
        session.add(instance)
        await session.flush()
        await session.refresh(instance)
        return instance
