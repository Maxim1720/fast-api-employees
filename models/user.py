from typing import Optional, Type

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Session

from api.dto.users import UserForCreate, UserUpdate
from models.base import BaseModel, db_engine


class User(BaseModel):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)


BaseModel.metadata.create_all(db_engine)

__session = Session(autoflush=True, bind=db_engine)


def get_by_id(user_id: int) -> Optional[User]:
    with __session as db:
        return db.get(User, user_id)


def create(user: User) -> User:
    with __session as db:
        u = user
        db.add(u)
        db.commit()
        db.refresh(u)
        return u


def update_or_create(user_id: int, user: UserForCreate) -> User:
    with __session as db:
        u = db.get(User, user_id)
        if u is None:
            u = create(User(**user.__dict__))
        else:
            u = update_by_id(user_id, UserUpdate(**user.__dict__))
        return u


def update_by_id(user_id: int, user: UserUpdate) -> Optional[User]:
    with __session as db:
        u = db.get(User, user_id)
        for k, v in user.model_dump(exclude_unset=True).items():
            setattr(u, k, v)
        db.commit()
        db.refresh(u)
        return u


def get_all() -> list[Type[User]]:
    with __session as db:
        return db.query(User).all()


def get_by_name(name: str) -> Optional[User]:
    with __session as db:
        return db.query(User).filter(User.name == name).first()


def delete_by_id(user_id: int) -> Optional[Type[User]]:
    with __session as db:
        u = db.get(User, user_id)
        if u is not None:
            db.delete(u)
            db.commit()
        return u
