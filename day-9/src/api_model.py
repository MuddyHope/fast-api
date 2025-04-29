from typing import Optional

from pydantic import BaseModel


class DescriptionBody(BaseModel):
    description: str

class BlogViewModel(BaseModel):
    id: int
    title: str
    description: Optional[str]
