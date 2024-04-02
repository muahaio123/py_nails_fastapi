from service.database import create_connection
from typing import Union
from fastapi import FastAPI, Request
from service.employees import *
import json
from types import SimpleNamespace

# run the program with this command: py -m uvicorn main:app --reload

create_connection()
app = FastAPI()

# APIs for Employees
@app.get("/employees")
def get_all_employees():
    return select_all_employees()

@app.get("/employees/{emp_id}")
def get_employee_id(emp_id: int):
    return select_employee_id(emp_id)

@app.post("/employees")
async def post_employee(request: Request):
    # get request's body data as python's dictionary
    data = await request.json()
    # convert json data to Employee object (by mapping data and value to corresponding attribute in dataclass)
    new_emp = Employee(**data)

    return create_new_employee(new_emp)

@app.put("/employees")
async def put_employee(request: Request):
    # get request's body data as python's dictionary
    data = await request.json()
    # convert json data to Employee object (by mapping data and value to corresponding attribute in dataclass)
    exist_emp = Employee(**data)

    return update_existing_employee(exist_emp)    

@app.delete("/employees/{emp_id}")
async def delete_employees(emp_id: int):
    return delete_existing_employee(emp_id)