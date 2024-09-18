from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .config import settings

def get_conn_url():
    user =  settings.POSTGRES_USER
    password = settings.POSTGRES_PASSWORD
    server = settings.POSTGRES_SERVER
    port = settings.POSTGRES_PORT
    db = settings.POSTGRES_DB
    
    conn_base_url = f"postgresql://{user}:{password}@{server}:{port}/{db}"
    return conn_base_url

def create_db_session():
    conn = get_conn_url( user=settings.POSTGRES_USER, 
    password=settings.POSTGRES_PASSWORD,
    server=settings.POSTGRES_SERVER, port=settings.POSTGRES_PORT, db=settings.POSTGRES_DB,
    port=settings.POSTGRES_PORT,
    db=settings.POSTGRES_DB)

    engine = create_engine(conn)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return SessionLocal()

Base = declarative_base()
__all__ = ['Base', 'create_db_session']
