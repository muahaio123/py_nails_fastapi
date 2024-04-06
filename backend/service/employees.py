from dataclasses import dataclass
from typing import Any
from service.database import pool
from sqlite3 import Error

@dataclass
class Employee:
    emp_id: int = -1
    emp_name: str = ""
    emp_phone: str = ""
    emp_ssn: str = ""
    emp_address: str = ""
    emp_work_percentage: int = 0
    emp_cash_percentage: int = 0
    emp_salary: int = 0

# Implement all 4 CRUD operations on employees
def row_to_employee(row: list[Any]):
    return Employee(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7])

# GET all employees
async def select_all_employees() -> list[Employee]:
    with pool.connection() as conn:
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM employees")
        output = cursor.fetchall()

        all_emp_list: list[Employee] = []
        for row in output:
            all_emp_list.append(row_to_employee(row))
    
    return all_emp_list

# GET Employee by ID
async def select_employee_id(id: int) -> Employee:
    with pool.connection() as conn:
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM employees WHERE emp_id = ?", (id,))
        output = cursor.fetchone()

    return row_to_employee(output) if output else Employee()

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
            return Employee()

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
            return Employee()
    
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
            return Employee()
    
    return found_emp