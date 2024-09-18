from datetime import datetime
from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.orm import Session

from nepal_constitution_ai.user import schemas
from nepal_constitution_ai.user.model import User

async def get_all_users(db: Session):
    users = db.query(User).all()
    return users

def authenticate_user(db: Session, user_id: UUID, password: str):
    user = db.query(User).filter(User.user_id == user_id).first()
    if user:
        return user
    return False

def user_create(user: schemas.UserCreate, db: Session):
    user_exists = db.query(User).filter_by(user_id=user.user_id).first()
    if user_exists:
        raise HTTPException(status_code=400, detail="User Exists Already")

    user = User()

    db.add(user)
    db.commit()
    db.refresh(user)

    return {"User created successfully"}