# pylint:disable=E0401, R0903, C0115

from pydantic import BaseModel


class Blog(BaseModel):
    title: str
    desc: str


class BlogView(BaseModel):
    id: int
    title: str
    desc: str
