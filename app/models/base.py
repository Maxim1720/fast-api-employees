from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase
from app.config.settings import env

db_engine = create_engine(env("DB_URL"), echo=True)


class BaseModel(DeclarativeBase):
    pass
