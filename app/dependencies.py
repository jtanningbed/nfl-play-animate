from app.config import SessionLocal
from sqlalchemy.orm import Session
from collections.abc import Generator


# Dependency to get the database session
def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
