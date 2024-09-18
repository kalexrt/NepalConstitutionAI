from uuid import UUID

from pydantic import BaseModel

class UserCreate(BaseModel):
    user_id: UUID

class UserResponse(BaseModel):
    user_id: UUID