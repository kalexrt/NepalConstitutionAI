from typing import Generator
from sqlalchemy.orm.session import Session
from .db import create_db_session

def get_session() -> Generator: 
    db: Session | None = None
    try:
        db = create_db_session()
        yield db
    except Exception as e:
        raise e
    finally:
        if db:
            db.close()