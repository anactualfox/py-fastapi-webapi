from http.client import HTTPException
from typing import List
from fastapi import FastAPI, status
from uuid import UUID
from fastapi.responses import HTMLResponse
from models import User

app = FastAPI()

db: List[User] = [
    User(
        first_name="John",
        last_name="Ed"
    ),
    User(
        first_name="Emily",
        last_name="Ane"
    ),
]


@app.get("/", response_class=HTMLResponse)
async def root():
    return '''
    <html>
        <a>
            <b>Hello!</b>
        </a>
    </html>
    '''


@app.get("/api/v1/users")
async def get_users_async():
    return db


@app.post("/api/v1/users", status_code=status.HTTP_201_CREATED)
async def create_user_async(user: User):
    db.append(user)
    return {"id": user.id}


@app.get("/api/v1/users/{id}")
async def get_user_async(id: UUID):
    for user in db:
        if user.id == id:
            return user

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@app.put("api/v1/users/", status_code=status.HTTP_204_NO_CONTENT)
async def update_user_async(user: User):
    for db_user in db:
        if db_user == user.id:
            db.remove(db_user)
            db.append(user)

    raise HTTPException(status_code=status.HTTP_409_CONFLICT)


@app.delete("/api/v1/users/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_async(id: UUID):
    for user in db:
        if user.id == id:
            db.remove(user)
            return

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)