import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase

load_dotenv()

db_engine = create_engine(os.getenv("DB_URL"), echo=True)


class BaseModel(DeclarativeBase):
    pass
