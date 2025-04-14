"""
Main file as entry
"""

# pylint:disable=E0401

from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


# pylint:disable=R0903
class Item(BaseModel):
    """
    Item Model for database classification
    """

    name: str
    price: float
    is_offer: Union[bool, None] = None


@app.get("/")
def read_root():
    """
    Returns hello world!
    :return: str
    """
    return {"Hello": "World"}


# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: Union[str, None] = None):
#     """
#     :param item_id:
#     :param q:
#     :return:
#     """
#     return {"item_id": item_id, "q": q}
#
#
# @app.put("/items/{item_id}")
# def update_item(item_id: int, item: Item):
#     return {"item_name": item.name, "item_id": item_id}
