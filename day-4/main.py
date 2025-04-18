"""
Creating Response model for User API
"""

# pylint:disable=E0401, R0903, C0115
from uuid import uuid4, UUID
from typing import List
from passlib.context import CryptContext
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr

app = FastAPI()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserResponseModel(BaseModel):
    """
    User Response Model once user has successfully registered
    """

    id: UUID
    name: str
    email: EmailStr


class UserCreateModel(BaseModel):
    """
    User create model
    """

    name: str
    password: str
    email: EmailStr


class ListUsersModel(BaseModel):
    """
    User show model
    """

    response: List[UserResponseModel]
    count: int


users_db = []


@app.get("/users", response_model=ListUsersModel)
def get_user():
    """Fetch all Users"""
    return {"response": users_db, "count": len(users_db)}


@app.post("/user", response_model=UserResponseModel)
def add_user(user: UserCreateModel):
    """

    :param user: UserModel for creating new user
    :return: UserResponseModel
    """
    # email checking
    email_present = any(each_user["email"] == user.email for each_user in users_db)

    if email_present:
        raise HTTPException(status_code=400, detail="User already present!")

    hashed_pwd = pwd_context.hash(str(user.password))
    new_user = {
        "id": uuid4(),
        "name": user.name,
        "password": hashed_pwd,
        "email": user.email,
    }
    users_db.append(new_user)
    return UserResponseModel(**{k: new_user[k] for k in ["id", "name", "email"]})
