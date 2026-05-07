from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

from .config import settings


SQLALCHEMY_DATABASE_URL =( 
        f"postgresql://{settings.database_username}:"
        f"{settings.database_password}@"
        f"{settings.database_hostname}:"
        f"{settings.database_port}/"
        f"{settings.database_name}"
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)

class Base(DeclarativeBase):
    pass


SessionLocal = sessionmaker(
    autocommit=False, 
    autoflush=False, 
    bind=engine
    )


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()