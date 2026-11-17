from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config import settings

from pathlib import Path

DATABASE_URL = "sqlite:///" + str(Path(__file__).resolve().parent.parent / "taskflow.db")

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)





