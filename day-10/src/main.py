from fastapi import FastAPI, Depends, status, HTTPException
from sqlalchemy.orm import Session
import models
import auth
from auth import get_current_user
from database import engine, SessionLocal
from typing import Annotated

# initialize FastAPI
app = FastAPI()
app.include_router(auth.router)


# binds my models to the engine and creates tables in the database from my model
models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# short for creating database session (for query/commit) to DB.
db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[Session, Depends(get_current_user)]


@app.get('/', status_code=status.HTTP_200_OK)
async def user(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication Failed")
    return {"User": user}
