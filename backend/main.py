from fastapi import FastAPI, Request
from service import employees, works, payments, emp_work_detail

# run the program with this command: py -m uvicorn main:app --reload
app = FastAPI()

##### APIs for Employees #####
@app.get("/employees")
async def get_all_employees():
    return await employees.select_all_employees()

@app.get("/employees/{emp_id}")
async def get_employee_id(emp_id: int):
    return await employees.select_employee_id(emp_id)

@app.post("/employees")
async def post_employee(request: Request):
    # get request's body data as python's dictionary
    data = await request.json()
    # convert json data to Employee object (by mapping data and value to corresponding attribute in dataclass)
    new_emp = employees.Employee(**data)

    return await employees.create_new_employee(new_emp)

@app.put("/employees")
async def put_employee(request: Request):
    # get request's body data as python's dictionary
    data = await request.json()
    # convert json data to Employee object (by mapping data and value to corresponding attribute in dataclass)
    exist_emp = employees.Employee(**data)

    return await employees.update_existing_employee(exist_emp)    

@app.delete("/employees/{emp_id}")
async def delete_employee(emp_id: int):
    return await employees.delete_existing_employee(emp_id)
##### APIs for Employees #####

##### APIs for Works #####
@app.get("/works")
async def get_all_works():
    return await works.select_all_works()

@app.get("/works/{work_id}")
async def get_work_id(work_id: int):
    return await works.select_work_id(work_id)

# GET works between 2 datetime
@app.get("/works/{from_datetime}/{to_datetime}")
async def get_works_date(from_datetime: str, to_datetime: str):
    return await works.select_works_between_dates(from_datetime, to_datetime)

@app.post("/works")
async def post_work(request: Request):
    # get request's body data as python's dictionary
    data = await request.json()
    # convert json data to Employee object (by mapping data and value to corresponding attribute in dataclass)
    new_emp = works.Works(**data)

    return await works.create_new_work(new_emp)

@app.put("/works")
async def put_work(request: Request):
    # get request's body data as python's dictionary
    data = await request.json()
    # convert json data to Employee object (by mapping data and value to corresponding attribute in dataclass)
    exist_emp = works.Works(**data)

    return await works.update_existing_work(exist_emp)    

@app.delete("/works/{work_id}")
async def delete_work(work_id: int):
    return await works.delete_existing_work(work_id)
##### APIs for Works #####
