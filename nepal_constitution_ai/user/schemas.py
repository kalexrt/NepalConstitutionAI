from uuid import UUID
from typing import Optional
from pydantic import BaseModel

class User(BaseModel):
    user_id: Optional[UUID] = None
class UserCreate(BaseModel):
    user_id: UUID

class UserResponse(BaseModel):
    user_id: Optional[UUID] = None