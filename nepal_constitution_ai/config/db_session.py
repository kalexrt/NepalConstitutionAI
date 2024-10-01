from typing import Generator
from loguru import logger
from sqlalchemy.orm.session import Session
from contextlib import contextmanager
from .db import create_db_session

@contextmanager
def get_session() -> Generator: 
    db: Session | None = None
    try:
        db = create_db_session()
        yield db
    except Exception as e:
        logger.error(f"An error occurred while creating db session: {str(e)}")
        raise e
    finally:
        if db:
            db.close()