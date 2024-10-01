from uuid import UUID
from sqlalchemy.orm import Session

from nepal_constitution_ai.user import schemas
from nepal_constitution_ai.user.model import User

async def get_user(user_id: UUID, db: Session):
    user = db.query(User).filter(User.user_id == user_id).first()
    return user

async def get_all_users(db: Session):
    users = db.query(User).all()
    return users

async def authenticate_user(db: Session, user_id: UUID):
    user = db.query(User).filter(User.user_id == user_id).first()
    if user:
        return user
    new_user = await user_create(user_id=user_id, db=db)
    return new_user

async def user_create(user_id: UUID, db: Session):
    user = User(user_id=user_id)

    db.add(user)
    db.commit()
    db.refresh(user)

    return user