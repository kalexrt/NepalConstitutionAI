from typing import List
from uuid import UUID, uuid4

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from loguru import logger

import nepal_constitution_ai.chat.controller as chat_controller
from nepal_constitution_ai.config.db_session import get_session
import nepal_constitution_ai.user.services as user_services
from nepal_constitution_ai.user.schemas import User

from . import schemas

router = APIRouter()



@router.post("/chat_session", response_model=schemas.ChatSession)
async def create_chat_session(
    user: User,
    db: Session = Depends(get_session),
):
    user = await user_services.get_user(user_id=user.user_id, db=db)
    if user is None:
        new_user_id = uuid4()
        new_user = await user_services.user_create(user_id=new_user_id, db=db)
        user = new_user
    new_chat_session = await chat_controller.create_chat_session(
        db=db, created_by=user.user_id
    )
    return new_chat_session


@router.patch("/chat_session/{session_id}")
async def update_chat_session(
    session_id: UUID,
    request: schemas.ChatSessionRequest,
    user_id: UUID,
    db: Session = Depends(get_session),
):
    user = await user_services.get_user(user_id=user_id, db=db)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    chat_session = await chat_controller.update_chat_session(
        user_id=user.user_id, session_id=session_id, request=request, db=db
    )

    return chat_session


@router.get("/chat-sessions")
async def get_chat_sessions(
    user_id: UUID,
    db: Session = Depends(get_session),
):
    user = await user_services.get_user(user_id=user_id, db=db)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    chat_session = await chat_controller.get_chat_session(
        user_id=user.user_id, db=db
    )

    return chat_session


@router.post("/generate_response", response_model=schemas.ChatResponse)
async def generate_response_with_session(
    request: schemas.RetrieverInput,
    user_id: UUID,
    db: Session = Depends(get_session),
    
):
    user = await user_services.get_user(user_id=user_id, db=db)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    try:
        query = request.query
        chat_session_id = request.chat_session_id

        logger.info(f"Retrieving for chat session: {chat_session_id}")

        if not query:
            raise HTTPException(status_code=400, detail="Missing required parameters")
        response = chat_controller.user_input(
            db=db,
            user=user,
            query=query,
            chat_session_id=chat_session_id,
        )  # Call user_input with the database session
        return response
    except HTTPException as e:
        logger.error(f"HTTP error occurred: {str(e)}")
        raise HTTPException(
            detail=f"An error occurred while processing your query: {str(e)}",
        )
    except Exception as e:
        logger.error(f"An unexpected error occurred: {str(e)}")
        raise e




@router.get(
    "/chat-history/{session_id}", response_model=List[schemas.ChatHistoryResponse]
)
async def get_chat_history(session_id: UUID, db: Session = Depends(get_session)):
    chat_messages = chat_controller.get_chat_history_by_session_id(
        session_id=session_id, db=db
    )

    if chat_messages is None:
        raise HTTPException(status_code=404, detail="Chat history not found")

    return chat_messages

