from fastapi import FastAPI, Query, HTTPException, status
from service import employees, works, payments, emp_work_detail
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# run the program with this command: py -m uvicorn main:app --reload
app = FastAPI(
    title="Nails Salon API",
    description="API for managing salon employees, works, payments, and work details",
    version="1.0.0"
)

##### APIs for Employees #####
@app.get("/employees/all_employees", tags=["Employees"])
def get_all_employees() -> list[employees.Employee]:
    try:
        return employees.select_all_employees()
    except Exception as e:
        logger.error(f"Error fetching employees: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error fetching employees")

@app.get("/employees/by-id/{emp_id}", tags=["Employees"])
def get_employee_id(emp_id: int) -> employees.Employee:
    emp = employees.select_employee_id(emp_id)
    if emp.emp_id == -1:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Employee {emp_id} not found")
    return emp

@app.post("/employees/new_employee", status_code=status.HTTP_201_CREATED, tags=["Employees"])
def post_employee(new_emp: employees.Employee) -> employees.Employee:
    try:
        return employees.create_new_employee(new_emp)
    except Exception as e:
        logger.error(f"Error creating employee: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error creating employee")

@app.put("/employees/update_employee", tags=["Employees"])
def put_employee(exist_emp: employees.Employee) -> employees.Employee:
    try:
        result = employees.update_existing_employee(exist_emp)
        if result.emp_id == -1:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Employee {exist_emp.emp_id} not found")
        return result
    except Exception as e:
        logger.error(f"Error updating employee: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error updating employee")

@app.delete("/employees/delete_employee/{emp_id}", status_code=status.HTTP_200_OK, tags=["Employees"])
def delete_employee(emp_id: int) -> employees.Employee:
    try:
        result = employees.delete_existing_employee(emp_id)
        if result.emp_id == -1:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Employee {emp_id} not found")
        return result
    except Exception as e:
        logger.error(f"Error deleting employee: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error deleting employee")
##### APIs for Employees #####

##### APIs for Works #####
@app.get("/works/all_works", tags=["Works"])
def get_all_works() -> list[works.Works]:
    try:
        return works.select_all_works()
    except Exception as e:
        logger.error(f"Error fetching works: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error fetching works")

@app.get("/works/by-id/{work_id}", tags=["Works"])
def get_work_id(work_id: int) -> works.Works:
    work = works.select_work_id(work_id)
    if work.work_id == -1:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Work {work_id} not found")
    return work
    
# GET works between 2 datetime
@app.get("/works/between-dates/{from_datetime}/{to_datetime}", tags=["Works"])
def get_works_date(from_datetime: str, to_datetime: str) -> list[works.Works]:
    try:
        return works.select_works_between_dates(from_datetime, to_datetime)
    except Exception as e:
        logger.error(f"Error fetching works between dates: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error fetching works")

# POST new work
@app.post("/works/new_work", status_code=status.HTTP_201_CREATED, tags=["Works"])
def post_work(new_work: works.Works) -> works.Works:
    try:
        return works.create_new_work(new_work)
    except Exception as e:
        logger.error(f"Error creating work: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error creating work")

# Update existing work
@app.put("/works/update_work", tags=["Works"])
def put_work(exist_work: works.Works) -> works.Works:
    try:
        result = works.update_existing_work(exist_work)
        if result.work_id == -1:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Work {exist_work.work_id} not found")
        return result
    except Exception as e:
        logger.error(f"Error updating work: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error updating work")

@app.delete("/works/delete_work/{work_id}", status_code=status.HTTP_200_OK, tags=["Works"])
def delete_work(work_id: int) -> works.Works:
    try:
        result = works.delete_existing_work(work_id)
        if result.work_id == -1:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Work {work_id} not found")
        return result
    except Exception as e:
        logger.error(f"Error deleting work: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error deleting work")
##### APIs for Works #####

##### APIs for Employee Work Details #####
@app.get("/details/all_details", tags=["Employee Work Details"])
def get_all_details() -> list[emp_work_detail.Detail]:
    return emp_work_detail.select_all_detail()

@app.get("/details/by-id/{work_id}", tags=["Employee Work Details"])
def get_detail_id(work_id: int) -> emp_work_detail.Detail:
    return emp_work_detail.select_detail_id(work_id)

# GET detail by list of work_ids
@app.get("/details/by-workids", tags=["Employee Work Details"])
def get_details_workid_list(work_ids: str = Query(None)) -> list[emp_work_detail.Detail]:
    return emp_work_detail.select_detail_workdids(work_ids)

# GET details by emp_id and list of work_ids
@app.get("/details/by-empid/{emp_id}", tags=["Employee Work Details"])
def get_detail_empid_workids(emp_id: int, work_ids: str = Query(None)) -> list[emp_work_detail.Detail]:
    return emp_work_detail.select_detail_empid_workids(emp_id, work_ids)

@app.post("/details/new_detail", tags=["Employee Work Details"])
def post_detail(new_detail: emp_work_detail.Detail) -> emp_work_detail.Detail:
    return emp_work_detail.create_new_detail(new_detail)
    
@app.put("/details/update_detail", tags=["Employee Work Details"])
def put_detail(exist_detail: emp_work_detail.Detail) -> emp_work_detail.Detail:
    return emp_work_detail.update_existing_detail(exist_detail)    

@app.delete("/details/delete_detail/{detail_id}", tags=["Employee Work Details"])
def delete_detail(detail_id: int) -> emp_work_detail.Detail:
    return emp_work_detail.delete_existing_detail(detail_id)
##### APIs for Employee Work Details #####

##### APIs for Payments #####
@app.get("/payments/all_payments", tags=["Payments"])
def get_all_payments() -> list[payments.Payments]:
    return payments.select_all_payments()

@app.get("/payments/by-id/{pmt_id}", tags=["Payments"])
def get_payment_id(pmt_id: int) -> payments.Payments:
    return payments.select_payment_id(pmt_id)

# GET detail by list of work_ids (1-2-3-4-5-etc.)
@app.get("/payments/by-pmtids/{pmt_ids}", tags=["Payments"])
def get_payments_workid_list(pmt_ids: str) -> list[payments.Payments]:
    return payments.select_payment_pmtids(pmt_ids)

# Create new payment
@app.post("/payments/new_payment", tags=["Payments"])
def post_payment(new_detail: payments.Payments) -> payments.Payments:
    return payments.create_new_payment(new_detail)

# Update existing payment
@app.put("/payments/update_payment", tags=["Payments"])
def put_payment(exist_detail: payments.Payments) -> payments.Payments:
    return payments.update_existing_payment(exist_detail)    

# Delete existing payment
@app.delete("/payments/delete_payment/{pmt_id}", tags=["Payments"])
def delete_payments(pmt_id: int) -> payments.Payments:
    return payments.delete_existing_payment(pmt_id)
##### APIs for Payments #####
