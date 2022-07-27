from typing import List
from fastapi import FastAPI, HTTPException, status
from uuid import UUID, uuid4
from fastapi.responses import HTMLResponse
from models.models import User


app = FastAPI()

db: List[User] = [
    User(
        id="2f260067-b225-4dd3-830d-d8f27c794e3a",
        first_name="John",
        last_name="Ed"
    ),
    User(
        id="2d77d74b-fbad-4f30-a302-782c05799f9a",
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

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="User not found")


@app.put("/api/v1/users/", status_code=status.HTTP_204_NO_CONTENT)
async def update_user_async(user: User):
    for db_user in db:
        if db_user.id == user.id:
            db.remove(db_user)
            db.append(user)
            return

    raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                        detail="User does not exist")


@app.delete("/api/v1/users/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_async(id: UUID):
    for user in db:
        if user.id == id:
            db.remove(user)
            return

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="User not found")
