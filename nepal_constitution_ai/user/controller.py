from uuid import UUID

from sqlalchemy.orm import Session

import nepal_constitution_ai.user.services as user_services

from . import schemas

def create_user(user: schemas.UserCreate, db: Session):
    new_user = user_services.user_create(user=user, db=db)
    return new_user

async def get_all_users(db: Session):
    users = await user_services.get_all_users(db=db)
    return users