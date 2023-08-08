from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from decouple import config

USER = config("POSTGRES_USER")
PASSWORD = config("POSTGRES_PASSWORD")
DB = config("POSTGRES_DATABASE")
HOST = config("POSTGRES_HOST")

SQLALCHEMY_DATABASE_URL = f'postgresql://{USER}:{PASSWORD}@{HOST}/{DB}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ALL THESE FROM FASTAPI SQLALCHEMY DOCUMENTATION