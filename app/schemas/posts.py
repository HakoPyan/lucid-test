from uuid import UUID

from pydantic import BaseModel, constr

MAX_PAYLOAD_SIZE = 1024 * 1024


class PostCreateRequestSchema(BaseModel):
    text: constr(max_length=MAX_PAYLOAD_SIZE)


class PostReadResponseSchema(PostCreateRequestSchema):
    id: UUID
    user_id: UUID

    class Config:
        from_attributes = True


class MultiplePostResponseSchema(BaseModel):
    results: list[PostReadResponseSchema]
