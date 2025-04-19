"""
Creating Response model for User API
"""

# pylint:disable=E0401, R0903, C0115
from uuid import uuid4, UUID
from typing import List

from passlib.context import CryptContext
from fastapi import FastAPI, HTTPException
from fastapi.params import Query
from pydantic import BaseModel, EmailStr

app = FastAPI()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


USERS_DB: List[dict] = [
    {
        "id": "0074015e-4572-48f1-abeb-464d7ec93d3d",
        "name": "string",
        "email": "use68@example.com",
    },
    {
        "id": "0074015e-4572-48f1-abeb-464d7ec93d3d",
        "name": "string",
        "email": "use1@example.com",
    },
    {
        "id": "0074015e-4572-48f1-abeb-464d7ec93d3d",
        "name": "string",
        "email": "use2@example.com",
    },
    {
        "id": "0074015e-4572-48f1-abeb-464d7ec93d3d",
        "name": "string",
        "email": "13@example.com",
    },
    {
        "id": "0074015e-4572-48f1-abeb-464d7ec93d3d",
        "name": "string",
        "email": "134@example.com",
    },
    {
        "id": "0074015e-4572-48f1-abeb-464d7ec93d3d",
        "name": "string",
        "email": "1313@example.com",
    },
    {
        "id": "0074015e-4572-48f1-abeb-464d7ec93d3d",
        "name": "string",
        "email": "424@example.com",
    },
    {
        "id": "0074015e-4572-48f1-abeb-464d7ec93d3d",
        "name": "string",
        "email": "2524@example.com",
    },
    {
        "id": "0074015e-4572-48f1-abeb-464d7ec93d3d",
        "name": "string",
        "email": "5354@example.com",
    },
    {
        "id": "0074015e-4572-48f1-abeb-464d7ec93d3d",
        "name": "string",
        "email": "534@example.com",
    },
    {
        "id": "0074015e-4572-48f1-abeb-464d7ec93d3d",
        "name": "string",
        "email": "90@example.com",
    },
    {
        "id": "0074015e-4572-48f1-abeb-464d7ec93d3d",
        "name": "string",
        "email": "2849@example.com",
    },
    {
        "id": "0074015e-4572-48f1-abeb-464d7ec93d3d",
        "name": "string",
        "email": "218904u@example.com",
    },
    {
        "id": "0074015e-4572-48f1-abeb-464d7ec93d3d",
        "name": "string",
        "email": "1093@example.com",
    },
]


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
    page_count: int
    total_count: int


@app.get("/users", response_model=ListUsersModel)
def get_user(skip: int = Query(0, ge=0), limit: int = Query(10, ge=1, le=10)):
    """Fetch all Users"""
    return {
        "response": USERS_DB[skip : skip + limit],
        "page_count": len(USERS_DB[skip : skip + limit]),
        "total_count": len(USERS_DB),
    }


@app.post("/user", response_model=UserResponseModel)
def add_user(user: UserCreateModel):
    """

    :param user: UserModel for creating new user
    :return: UserResponseModel
    """
    # email checking
    email_present = check_if_email_present(user.email)

    if email_present:
        raise HTTPException(status_code=400, detail="User already present!")

    hashed_pwd = pwd_context.hash(str(user.password))
    new_user = {
        "id": uuid4(),
        "name": user.name,
        "password": hashed_pwd,
        "email": user.email,
    }
    USERS_DB.append(new_user)
    return UserResponseModel(**{k: new_user[k] for k in ["id", "name", "email"]})


def check_if_email_present(email: str) -> bool:
    """Checks if email is present in the users_db"""
    email_present = any(each_user["email"] == email for each_user in USERS_DB)
    return email_present
