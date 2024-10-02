from datetime import datetime
from uuid import uuid4
from pydantic.types  import UUID4
from sqlalchemy import JSON, Column, DateTime, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from nepal_constitution_ai.config.db import Base

class ChatSessionModel(Base):
    """DB model for chat_session"""
    __tablename__ = "chat_session"
    chat_session_id: Mapped[UUID4] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    chat_date = Column(DateTime, default=datetime.now())
    modified_at = Column(DateTime, default=datetime.now())
    created_by = Column(UUID(as_uuid=True), ForeignKey('users.user_id'), nullable=False)

class ChatMessageModel(Base):
    """ DB model for chat_message"""
    __tablename__ = "chat_message"
    chat_message_id: Mapped[UUID4] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    message_by = Column(Text)
    content = Column(Text)
    message_time = Column(DateTime, default=datetime.now())
    chat_session_id: Mapped[UUID4] = mapped_column(UUID(as_uuid=True))