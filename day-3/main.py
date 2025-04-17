"""
Create User registration
"""

# pylint:disable=E0401, R0903, C0115
from typing import List
from uuid import uuid4, UUID

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
from passlib.context import CryptContext

# instantiate FastAPI
app = FastAPI()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

users_db = []


class UserCreateModel(BaseModel):
    name: str
    email: EmailStr
    password: str


class UserResponseModel(BaseModel):
    id: UUID
    name: str
    email: EmailStr


class UsersListModel(BaseModel):
    result: List[UserResponseModel]
    count: int


@app.get("/users", response_model=UsersListModel)
def get_users():
    """
    :return: Result of users are there and also count
    """
    return {"result": users_db, "count": len(users_db)}


@app.post("/users", response_model=UserResponseModel)
def add_user(user: UserCreateModel):
    """
    Register a new user with hashed password
    :param user: UserCreateModel
    :return: UserResponseModel
    """
    if any(u["email"] == user.email for u in users_db):
        raise HTTPException(status_code=400, detail="User Already exists")
    hashed_pwd = pwd_context.hash(user.password)
    new_user = {
        "id": uuid4(),
        "name": user.name,
        "email": user.email,
        "password": hashed_pwd,
    }
    users_db.append(new_user)
    return UserResponseModel(**{k: new_user[k] for k in ("id", "name", "email")})
