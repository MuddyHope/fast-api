"""
Using query and parameters to make a calculator
"""

# pylint:disable=E0401

from typing import Union
from enum import Enum

from fastapi import FastAPI, Query, HTTPException


# instantiation of FastApi
app = FastAPI()


class OperationEnum(Enum):
    """
    What all operations are allowed in the calculator
    """

    ADD = "+"
    SUB = "-"
    MULT = "*"
    DIVIDE = "/"


@app.get("/")
def read_root():
    """
    Returns hello world!
    :return: str
    """
    return {"Hello": "World"}


@app.get("/calculator")
def calculator(
    operation: OperationEnum = Query(
        ..., description="Choose an operation: +, -, *, /"
    ),
    num1: Union[int, float] = Query(..., description="First number"),
    num2: Union[int, float] = Query(..., description="Second number"),
) -> Union[dict]:
    """
    :param operation: string of which operation
    :param num1: First Number
    :param num2: Second Number
    :return: Response of the operation
    """
    _res = None
    if operation == OperationEnum.ADD:
        _res = num1 + num2
    elif operation == OperationEnum.SUB:
        _res = num1 - num2
    elif operation == OperationEnum.DIVIDE:
        if num2 == 0:
            raise HTTPException(
                status_code=400, detail="Division by zero is not possible"
            )
        _res = num1 / num2
    elif operation == OperationEnum.MULT:
        _res = num1 * num2
    return {"result": _res}
