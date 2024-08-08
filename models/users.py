from typing import Any, Optional
from typing_extensions import Self

from pydantic import BaseModel, root_validator, model_validator, PrivateAttr, Field

id_counter = 0


def id_generator():
    global id_counter
    id_counter += 1
    return id_counter


class User(BaseModel):
    id: int = Field(default_factory=id_generator)
    name: str
    password: str


class UserUpdate(BaseModel):
    name: Optional[str | None] = None
    password: Optional[str | None] = None


class UserProtected(BaseModel):
    id: int
    name: str


users = [
    User(name="admin", password="123"),
    User(name="user", password="123"),
]


def get_user_by_id(user_id: int) -> Optional[User]:
    for user in users:
        if user.id == user_id:
            return user
    return None


def update(user_id: int, new: UserUpdate) -> Optional[User]:
    update_data = new.model_dump(exclude_unset=True)
    stored = get_user_by_id(user_id)
    if stored is None:
        return stored
    stored.__dict__.update(**update_data)
    return stored
