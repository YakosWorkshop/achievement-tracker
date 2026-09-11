from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from achievement_tracker.database.base import Base

PROJECT_ROOT = Path(__file__).resolve().parent[3]
DATABASE_PATH = PROJECT_ROOT / "data" / "achievements.db"

DATABASE_URL = f"sqlite:///{DATABASE_PATH}"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(bind=engine)

def initialize_database() -> None:
    Base.metadata.create_all(engine)