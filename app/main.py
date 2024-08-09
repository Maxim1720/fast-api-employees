from fastapi import FastAPI
from app.api.users import app as users_app

app = FastAPI()
app.mount("/users", users_app)


@app.get("/")
async def root():
    return {"message": "Welcome to 'Employee' REST API application!"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
