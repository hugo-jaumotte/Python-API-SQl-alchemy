import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from typing import Generator
from dotenv import load_dotenv

load_dotenv()

# Create SQLAlchemy engine
# pool_pre_ping=True: checks connection before using it (avoids stale connections)
engine = create_engine(os.getenv("DATABASE_URL"), echo=False, pool_pre_ping=True)

# Session factory
# autoflush=False: disables automatic flush before queries
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base class for all ORM models
Base = declarative_base()

def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()