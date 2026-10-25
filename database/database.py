from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import create_engine
from security.env_loader import DATABASE_URL

if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
else:
    engine = create_engine(DATABASE_URL)
Base = declarative_base()

LocalSession = sessionmaker(bind=engine)

def get_db():
    db = LocalSession()
    try:
        yield db
    finally:
        db.close()