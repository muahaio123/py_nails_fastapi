from service.database import create_connection
from typing import Union
from fastapi import FastAPI, Request
from service.employees import *
import json
from types import SimpleNamespace

# run the program with this command: python -m uvicorn main:app --reload

create_connection()
app = FastAPI()

# APIs for Employees
@app.get("/employees")
async def get_all_employees():
    return json.dumps(select_all_employees().__dict__)

@app.get("/employees/{emp_id}")
async def get_all_employees(emp_id: int):
    return json.dumps(select_employee_id(emp_id).__dict__)

@app.post("/employees")
async def post_employees(request: Request):
    data = await request.json()
    new_emp = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))
    new_emp = create_new_employee(new_emp)
    return json.dumps(new_emp.__dict__)

@app.delete("/employees/{emp_id}")
async def delete_employees(emp_id: int):
    return json.dumps(delete_existing_employee(emp_id).__dict__)