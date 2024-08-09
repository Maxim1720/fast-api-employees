from fastapi import FastAPI, HTTPException

from app.api.dto.users import UserUpdate, UserProtected, UserForCreate
from app.models.user import get_by_id, create, User as UserDB, get_by_name, update_by_id
from app.models.user import get_all, delete_by_id

app = FastAPI()


@app.get("/", response_model=list[UserProtected])
async def all():
    return get_all()


@app.post("/", response_model=UserProtected)
async def add(user: UserForCreate):
    if get_by_name(user.name) is not None:
        raise HTTPException(status_code=400, detail="User with this name already exists")
    return create(UserDB(**user.__dict__))


@app.put("/{user_id}", response_model=UserProtected)
async def put(user_id: int, user: UserForCreate):
    from app.models.user import update_or_create
    return update_or_create(user_id, user)


@app.patch("/{user_id}", response_model=UserProtected)
async def partial_update(user_id: int, user: UserUpdate):
    new = update_by_id(user_id, user)
    if new is None:
        raise HTTPException(status_code=404, detail="User not found")
    return new


@app.get("/{user_id}", response_model=UserProtected)
async def get(user_id: int):
    user = get_by_id(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.delete("/{user_id}", response_model=UserProtected)
async def delete(user_id: int):
    deleted = delete_by_id(user_id)
    if deleted is None:
        raise HTTPException(status_code=404, detail="User not found")
    return deleted
