"""
Blog API
"""

from typing import List

# pylint:disable=E0401, R0903, C0115

from fastapi import FastAPI

from models import Blog, BlogView
from middleware import LoggingMiddleWare


app = FastAPI()
app.add_middleware(LoggingMiddleWare)

BLOG_ID = 0

database = {}


@app.get("/")
async def main():
    """
    Main function
    :return:
    """
    return {"Hello": "User"}


@app.post("/blog", response_model=BlogView)
async def create_blog(blog_details: Blog):
    """Create blogs"""
    # pylint: disable=W0603
    global BLOG_ID
    database[BLOG_ID] = {}
    database[BLOG_ID]["title"] = blog_details.title
    database[BLOG_ID]["desc"] = blog_details.desc
    new_blog = {"id": BLOG_ID, "title": blog_details.title, "desc": blog_details.desc}
    BLOG_ID += 1
    return BlogView(**new_blog)


@app.get("/blog", response_model=List[BlogView])
async def get_all_blogs():
    """List all blogs in database"""
    return [BlogView(id=_id, **blog) for _id, blog in database.items()]
