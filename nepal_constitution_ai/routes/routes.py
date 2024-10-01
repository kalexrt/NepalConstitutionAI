from fastapi import APIRouter, Depends

from nepal_constitution_ai.chat.routes import router as chat_routes
from nepal_constitution_ai.user.services import  authenticate_user


router = APIRouter()

router.include_router(chat_routes)

