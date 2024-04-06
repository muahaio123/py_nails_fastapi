from dataclasses import dataclass
from typing import Any
from service.database import pool
from sqlite3 import Error
from pydantic import BaseModel

@dataclass
class Employee(BaseModel):
    emp_id: int = -1
    emp_name: str = ""
    emp_phone: str = ""
    emp_ssn: str = ""
    emp_address: str = ""
    emp_work_percentage: int = 0
    emp_cash_percentage: int = 0
    emp_salary: int = 0

def getDefultEmployee():
    return Employee(emp_id=-1, emp_name="", emp_phone="", emp_ssn="", emp_address="", emp_work_percentage=0, emp_cash_percentage=0, emp_salary=0)

# Implement all 4 CRUD operations on employees
async def row_to_employee(row: list[Any]):
    return Employee(emp_id=row[0], emp_name=row[1], emp_phone=row[2], emp_ssn=row[3], emp_address=row[4], emp_work_percentage=row[5], emp_cash_percentage=row[6], emp_salary=row[7])

async def list_to_employess(rows: list[Any]):
    return [await row_to_employee(row) for row in rows]

# GET all employees
async def select_all_employees() -> list[Employee]:
    with pool.connection() as conn:
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM employees")
        output = cursor.fetchall()
    
    return await list_to_employess(output)

# GET Employee by ID
async def select_employee_id(id: int) -> Employee:
    with pool.connection() as conn:
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM employees WHERE emp_id = ?", (id,))
        output = cursor.fetchone()

    return await row_to_employee(output) if output else getDefultEmployee()

# POST new Employee
async def create_new_employee(new_emp: Employee) -> Employee:
    with pool.connection() as conn:
        cursor = conn.cursor()

        try:
            cursor.execute("INSERT INTO employees(emp_name, emp_phone, emp_ssn, emp_address, emp_work_percentage, emp_cash_percentage, emp_salary) VALUES(?, ?, ?, ?, ?, ?, ?)",
                        (new_emp.emp_name, new_emp.emp_phone, new_emp.emp_ssn, new_emp.emp_address, new_emp.emp_work_percentage, new_emp.emp_cash_percentage, new_emp.emp_salary))
            cursor.execute("SELECT emp_id FROM employees ORDER BY emp_id DESC LIMIT 1")
            new_emp.emp_id = cursor.fetchone()[0]
            conn.commit()
        except Error as e:
            print(e)
            conn.rollback()
            return getDefultEmployee()

    return new_emp

# PUT existing Employee
async def update_existing_employee(exist_emp: Employee) -> Employee:
    with pool.connection() as conn:
        cursor = conn.cursor()

        try:
            found_emp = await select_employee_id(exist_emp.emp_id)
            if found_emp.emp_id != -1:
                cursor.execute("UPDATE employees SET emp_name=?, emp_phone=?, emp_ssn=?, emp_address=?, emp_work_percentage=?, emp_cash_percentage=?, emp_salary=? WHERE emp_id=?",
                            (exist_emp.emp_name, exist_emp.emp_phone, exist_emp.emp_ssn, exist_emp.emp_address, exist_emp.emp_work_percentage, exist_emp.emp_cash_percentage, exist_emp.emp_salary, exist_emp.emp_id))
                conn.commit()
            else:
                raise Error(f"emp_id={found_emp.emp_id} cannot be found in table:employees")
        except Error as e:
            print(e)
            conn.rollback()
            return getDefultEmployee()
    
    return exist_emp

# DELETE existing employee by ID
async def delete_existing_employee(exist_emp_id: int) -> Employee:
    with pool.connection() as conn:
        cursor = conn.cursor()

        try:
            found_emp = await select_employee_id(exist_emp_id)
            if found_emp.emp_id != -1:
                cursor.execute("DELETE FROM employees WHERE emp_id=?", (exist_emp_id,))
                conn.commit()
            else:
                raise Error(f"emp_id={found_emp.emp_id} cannot be found in table:employees")
        except Error as e:
            print(e)
            conn.rollback()
            return getDefultEmployee()
    
    return found_emp