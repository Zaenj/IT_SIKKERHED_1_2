from fastapi import FastAPI, HTTPException
from src.models import User
from src.flat_file_loader import load_users, save_users

app = FastAPI()


@app.get("/")
def root():
    return {"message": "REST API is running"}


@app.post("/users")
def create_user(user: User):
    users = load_users()

    # Check if user already exists
    if any(u["person_id"] == user.person_id for u in users):
        raise HTTPException(status_code=400, detail="User already exists")

    users.append(user.dict())
    save_users(users)

    return user


@app.get("/users/{person_id}")
def get_user(person_id: int):
    users = load_users()

    for user in users:
        if user["person_id"] == person_id:
            return user

    raise HTTPException(status_code=404, detail="User not found")


@app.put("/users/{person_id}")
def update_user(person_id: int, updated_user: User):
    users = load_users()

    for index, user in enumerate(users):
        if user["person_id"] == person_id:
            users[index] = updated_user.dict()
            save_users(users)
            return updated_user

    raise HTTPException(status_code=404, detail="User not found")

@app.delete("/users/{person_id}")
def delete_user(person_id: int):
    users = load_users()

    for index, user in enumerate(users):
        if user["person_id"] == person_id:
            deleted_user = users.pop(index)
            save_users(users)
            return {"message": "User deleted", "user": deleted_user}

    raise HTTPException(status_code=404, detail="User not found")


@app.get("/users")
def list_users():
    return load_users()