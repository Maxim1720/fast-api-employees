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


class UserForCreate(BaseModel):
    name: str
    password: str
