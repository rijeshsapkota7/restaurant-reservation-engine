from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import create_engine
from security.env_loader import SQLITEURL

engine = create_engine(SQLITEURL, connect_args={"check_same_thread" : False})

Base = declarative_base()

LocalSession = sessionmaker(bind=engine)

def get_db():
    db = LocalSession()
    try:
        yield db
    finally:
        db.close()