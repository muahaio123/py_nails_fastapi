from re import I
from fastapi import FastAPI, Query, Request
from service import employees, works, payments, emp_work_detail

# run the program with this command: py -m uvicorn main:app --reload
app = FastAPI()

##### APIs for Employees #####
@app.get("/employees")
async def get_all_employees() -> list[employees.Employee]:
    return await employees.select_all_employees()

@app.get("/employees/{emp_id}")
async def get_employee_id(emp_id: int) -> employees.Employee:
    return await employees.select_employee_id(emp_id)

@app.post("/employees")
async def post_employee(new_emp: employees.Employee) -> employees.Employee:
    return await employees.create_new_employee(new_emp)

@app.put("/employees")
async def put_employee(exist_emp: employees.Employee) -> employees.Employee:
    return await employees.update_existing_employee(exist_emp)    

@app.delete("/employees/{emp_id}")
async def delete_employee(emp_id: int) -> employees.Employee:
    return await employees.delete_existing_employee(emp_id)
##### APIs for Employees #####

##### APIs for Works #####
@app.get("/works")
async def get_all_works() -> list[works.Works]:
    return await works.select_all_works()

@app.get("/works/{work_id}")
async def get_work_id(work_id: int) -> works.Works:
    return await works.select_work_id(work_id)

# GET works between 2 datetime
@app.get("/works/{from_datetime}/{to_datetime}")
async def get_works_date(from_datetime: str, to_datetime: str) -> list[works.Works]:
    return await works.select_works_between_dates(from_datetime, to_datetime)

@app.post("/works")
async def post_work(new_work: works.Works) -> works.Works:
    return await works.create_new_work(new_work)

@app.put("/works")
async def put_work(exist_work: works.Works) -> works.Works:
    return await works.update_existing_work(exist_work)    

@app.delete("/works/{work_id}")
async def delete_work(work_id: int) -> works.Works:
    return await works.delete_existing_work(work_id)
##### APIs for Works #####

##### APIs for Emp_Work_Detail #####
@app.get("/details")
async def get_all_details() -> list[emp_work_detail.Detail]:
    return await emp_work_detail.select_all_detail()

@app.get("/details/{work_id}")
async def get_detail_id(work_id: int) -> emp_work_detail.Detail:
    return await emp_work_detail.select_detail_id(work_id)

# GET detail by list of work_ids
@app.get("/details")
async def get_details_workid_list(work_ids: str = Query(None)) -> list[emp_work_detail.Detail]:
    return await emp_work_detail.select_detail_workdids([int(id) for id in work_ids.split('-')])

# GET details by emp_id and list of work_ids
@app.get("/details/{emp_id}")
async def get_detail_empid_workids(emp_id: int, work_ids: str = Query(None)) -> list[emp_work_detail.Detail]:
    return await emp_work_detail.select_detail_empid_workids(emp_id, [int(id) for id in work_ids.split('-')])

@app.post("/details")
async def post_detail(new_detail: emp_work_detail.Detail) -> emp_work_detail.Detail:
    return await emp_work_detail.create_new_detail(new_detail)

@app.put("/details")
async def put_detail(exist_detail: emp_work_detail.Detail) -> emp_work_detail.Detail:
    return await emp_work_detail.update_existing_detail(exist_detail)    

@app.delete("/details/{detail_id}")
async def delete_detail(detail_id: int) -> emp_work_detail.Detail:
    return await emp_work_detail.delete_existing_detail(detail_id)
##### APIs for Emp_Work_Detail #####

##### APIs for Payments #####
@app.get("/payments")
async def get_all_payments() -> list[payments.Payments]:
    return await payments.select_all_payments()

@app.get("/payments/{pmt_id}")
async def get_payment_id(pmt_id: int) -> payments.Payments:
    return await payments.select_payment_id(pmt_id)

# GET detail by list of work_ids
@app.get("/payments")
async def get_payments_workid_list(pmt_ids: str = Query(None)) -> list[payments.Payments]:
    return await payments.select_payment_workdids([int(id) for id in pmt_ids.split('-')])

@app.post("/payments")
async def post_payment(new_detail: payments.Payments) -> payments.Payments:
    return await payments.create_new_payment(new_detail)

@app.put("/payments")
async def put_payment(exist_detail: payments.Payments) -> payments.Payments:
    return await payments.update_existing_payment(exist_detail)    

@app.delete("/payments/{pmt_id}")
async def delete_payments(pmt_id: int) -> payments.Payments:
    return await payments.delete_existing_payment(pmt_id)
##### APIs for Payments #####
