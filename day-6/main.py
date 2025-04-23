"""
Creating AuthMiddleWare User API
"""

# pylint:disable=E0401, R0903, C0115
from uuid import uuid4, UUID
from typing import List, Optional

from passlib.context import CryptContext
from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.params import Query
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel, EmailStr
from starlette.middleware.base import BaseHTTPMiddleware

# --- Setup ---
app = FastAPI()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBasic()

PUBLIC_PATHS = {"/docs", "/openapi.json", "/redoc", "/user", "/users", "/favicon.ico"}


# In-memory users DB with hashed passwords
USERS_DB: List[dict] = [
    {
        "id": uuid4(),
        "name": "alice",
        "email": "alice@example.com",
        "hashed_password": pwd_context.hash("alicepass"),
    },
    {
        "id": uuid4(),
        "name": "bob",
        "email": "bob@example.com",
        "hashed_password": pwd_context.hash("bobpass"),
    },
]


# --- Pydantic Models ---
class UserResponseModel(BaseModel):
    id: UUID
    name: str
    email: EmailStr


class UserCreateModel(BaseModel):
    name: str
    password: str
    email: EmailStr


class ListUsersModel(BaseModel):
    response: List[UserResponseModel]
    page_count: int
    total_count: int


# --- Utility Functions ---
def get_user_by_email(email: str) -> Optional[dict]:
    """Retrieve a user dict from USERS_DB by email."""
    # return next((u for u in USERS_DB if u["email"] == email), None)
    for u in USERS_DB:
        print("Checking user:", u)  # Debug
        if u["email"] == email:
            return u
    return None


# --- Auth Middleware ---
class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        # Skip authentication for public endpoints
        if request.url.path in PUBLIC_PATHS:
            return await call_next(request)

        # HTTP Basic credentials
        credentials: HTTPBasicCredentials = await security(request)
        user = get_user_by_email(credentials.username)
        print(f"User: {user}")
        print(f"password: {credentials.password}")
        if not user:
            raise HTTPException(status_code=401, detail="Invalid credentials")

        # Attach user info to request.state for downstream
        request.state.current_user = user.get("name")
        print(f"user {user.get('name')}")
        return await call_next(request)


# Register middleware
app.add_middleware(AuthMiddleware)


# --- Endpoints ---
@app.post("/user", response_model=UserResponseModel)
async def create_user(user: UserCreateModel):
    if get_user_by_email(user.email):
        raise HTTPException(status_code=400, detail="Email already registered")
    new_user = {
        "id": uuid4(),
        "name": user.name,
        "email": user.email,
        "hashed_password": pwd_context.hash(user.password),
    }
    USERS_DB.append(new_user)
    return UserResponseModel(**new_user)


@app.get("/users", response_model=ListUsersModel)
async def list_users(skip: int = Query(0, ge=0), limit: int = Query(10, ge=1, le=50)):
    sliced = USERS_DB[skip : skip + limit]
    # Exclude password from response
    response = [{k: u[k] for k in ("id", "name", "email")} for u in sliced]
    return {
        "response": response,
        "page_count": len(response),
        "total_count": len(USERS_DB),
    }


@app.get("/hello")
async def hello_world(request: Request):
    # print(f'request: {list(request.state)}')
    user = request.state.current_user
    return {"message": f"Hello, ['{user}']!"}
