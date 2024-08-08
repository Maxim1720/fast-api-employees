from fastapi import FastAPI, HTTPException

from models.users import User, UserUpdate, UserProtected, get_user_by_id, update
from models.users import users as users_db

app = FastAPI()


@app.get("/", response_model=list[UserProtected])
async def all():
    return users_db


@app.post("/", response_model=UserProtected)
async def add(user: User):
    users_db.append(user)
    return user


@app.put("/{user_id}", response_model=UserProtected)
async def put(user_id: int, user: User):
    user_from_db = get_user_by_id(user_id)
    if user_from_db is None:
        users_db.append(User(**user.__dict__))
        return users_db[-1]
    return update(user_id, UserUpdate(**user.__dict__))


@app.patch("/{user_id}", response_model=UserProtected)
async def partial_update(user_id: int, user: UserUpdate):
    new = update(user_id, user)
    if new is None:
        raise HTTPException(status_code=404, detail="User not found")
    return new


@app.get("/{user_id}", response_model=UserProtected)
async def get(user_id: int):
    user = get_user_by_id(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user
