import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Database URL default to SQLite local file (or /tmp on read-only serverless runtimes like Vercel)
_default_db_url = (
    "sqlite:////tmp/amicare.db"
    if os.getenv("VERCEL")
    else "sqlite:///./amicare.db"
)
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", _default_db_url)

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
