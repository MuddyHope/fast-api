from fastapi import FastAPI, Depends, Query, Body, Path, HTTPException
from sqlalchemy.orm import Session
from models import Blog
from typing import List, Optional
from middleware.logging import LoggingMiddleWare
from database import Base, engine, SessionLocal
from api_model import DescriptionBody, BlogViewModel

app = FastAPI()

app.add_middleware(LoggingMiddleWare)


Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/blog/", response_model=BlogViewModel)
async def create_post(title: str = Query(), description: DescriptionBody = Body(), db: Session = Depends(get_db)):
    blog = Blog(title=title, description=description.description)
    db.add(blog)
    db.commit()
    db.refresh(blog)
    return blog


@app.get("/blogs/", response_model=List[BlogViewModel])
async def read_posts(db: Session = Depends(get_db)):
    return db.query(Blog).all()


@app.get("/blog/{blog_id}", response_model=BlogViewModel)
async def read_each_blog(blog_id: int = Path(), db: Session = Depends(get_db)):
    return db.query(Blog).get(blog_id)


@app.put("/blog/{blog_id}", response_model=BlogViewModel)
async def update_each_blog(blog_id: int = Path(), title: Optional[str] = Query(None),
                           description: Optional[DescriptionBody] = Body(None), db: Session = Depends(get_db)):
    blog = db.query(Blog).filter(Blog.id == blog_id).first()
    # print("blog_title", blog.title)
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")

    if title is not None:
        blog.title = title

    if description is not None and description.description is not None:
        blog.description = description.description

    db.commit()
    db.refresh(blog)
    return BlogViewModel(**blog.__dict__)


@app.delete("/blog/{blog_id}")
async def delete_each_blog(blog_id: int = Path(), db: Session = Depends(get_db)):
    try:
        blog = db.query(Blog).filter(Blog.id == blog_id).delete()
        db.commit()
    except:
        raise HTTPException(404, detail=f"Blog Id {blog_id} Not found")
    return {f"BlogId {blog_id} Deleted": "success"}


