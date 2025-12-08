from typing import Any
from service.database import pool
from sqlite3 import Error
from pydantic import BaseModel, field_validator
import logging

logger = logging.getLogger(__name__)

class Employee(BaseModel):
    emp_id: int = -1
    emp_name: str = ""
    emp_phone: str = ""
    emp_ssn: str = ""
    emp_address: str = ""
    emp_work_percentage: int = 0
    emp_cash_percentage: int = 0
    emp_salary: int = 0
    
    @field_validator('emp_work_percentage', 'emp_cash_percentage')
    @classmethod
    def validate_percentages(cls, v):
        if not 0 <= v <= 100:
            raise ValueError('Percentages must be between 0 and 100')
        return v
    
    @field_validator('emp_salary')
    @classmethod
    def validate_salary(cls, v):
        if v < 0:
            raise ValueError('Salary cannot be negative')
        return v

def getDefaultEmployee():
    return Employee(emp_id=-1, emp_name="", emp_phone="", emp_ssn="", emp_address="", emp_work_percentage=0, emp_cash_percentage=0, emp_salary=0)

# Implement all 4 CRUD operations on employees
def row_to_employee(row: list[Any]):
    return Employee(emp_id=row[0], emp_name=row[1], emp_phone=row[2], emp_ssn=row[3], emp_address=row[4], emp_work_percentage=row[5], emp_cash_percentage=row[6], emp_salary=row[7])

def list_to_employees(rows: list[Any]):
    return [row_to_employee(row) for row in rows]

# GET all employees
def select_all_employees() -> list[Employee]:
    with pool.connection() as conn:
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM employees")
        output = cursor.fetchall()
    
    return list_to_employees(output)

# GET Employee by ID
def select_employee_id(id: int) -> Employee:
    with pool.connection() as conn:
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM employees WHERE emp_id = ?", (id,))
        output = cursor.fetchone()

    return row_to_employee(output) if output else getDefaultEmployee()

# POST new Employee
def create_new_employee(new_emp: Employee) -> Employee:
    with pool.connection() as conn:
        cursor = conn.cursor()

        try:
            cursor.execute("INSERT INTO employees(emp_name, emp_phone, emp_ssn, emp_address, emp_work_percentage, emp_cash_percentage, emp_salary) VALUES(?, ?, ?, ?, ?, ?, ?)",
                        (new_emp.emp_name, new_emp.emp_phone, new_emp.emp_ssn, new_emp.emp_address, new_emp.emp_work_percentage, new_emp.emp_cash_percentage, new_emp.emp_salary))
            cursor.execute("SELECT emp_id FROM employees ORDER BY emp_id DESC LIMIT 1")
            new_emp.emp_id = cursor.fetchone()[0]
            conn.commit()
            logger.info(f"Employee created: {new_emp.emp_id} - {new_emp.emp_name}")
        except Error as e:
            logger.error(f"Database error creating employee: {e}")
            conn.rollback()
            new_emp = getDefaultEmployee()

    return new_emp

# PUT existing Employee
def update_existing_employee(exist_emp: Employee) -> Employee:
    with pool.connection() as conn:
        cursor = conn.cursor()

        try:
            found_emp = select_employee_id(exist_emp.emp_id)
            if found_emp.emp_id != -1:
                cursor.execute("UPDATE employees SET emp_name=?, emp_phone=?, emp_ssn=?, emp_address=?, emp_work_percentage=?, emp_cash_percentage=?, emp_salary=? WHERE emp_id=?",
                            (exist_emp.emp_name, exist_emp.emp_phone, exist_emp.emp_ssn, exist_emp.emp_address, exist_emp.emp_work_percentage, exist_emp.emp_cash_percentage, exist_emp.emp_salary, exist_emp.emp_id))
                conn.commit()
                logger.info(f"Employee updated: {exist_emp.emp_id}")
            else:
                raise Error(f"emp_id={found_emp.emp_id} cannot be found in table:employees")
        except Error as e:
            logger.error(f"Database error updating employee {exist_emp.emp_id}: {e}")
            conn.rollback()
            return getDefaultEmployee()
    
    return exist_emp

# DELETE existing employee by ID
def delete_existing_employee(exist_emp_id: int) -> Employee:
    with pool.connection() as conn:
        cursor = conn.cursor()

        try:
            found_emp = select_employee_id(exist_emp_id)
            if found_emp.emp_id != -1:
                cursor.execute("DELETE FROM employees WHERE emp_id=?", (exist_emp_id,))
                conn.commit()
                logger.info(f"Employee deleted: {exist_emp_id}")
            else:
                raise Error(f"emp_id={found_emp.emp_id} cannot be found in table:employees")
        except Error as e:
            logger.error(f"Database error deleting employee {exist_emp_id}: {e}")
            conn.rollback()
            return getDefaultEmployee()
    
    return found_emp