from dataclasses import dataclass
from typing import Any
from service.database import getDBConnection, getDBCursor, close_connection
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
async def row_to_employee(row: list[Any]):
    return Employee(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7])

# GET all employees
async def select_all_employees() -> list[Employee]:
    cursor = getDBCursor()
    cursor.execute("SELECT * FROM employees")
    output = cursor.fetchall()

    all_emp_list: list[Employee] = []
    for row in output:
        all_emp_list.append(await row_to_employee(row))
    
    close_connection()
    return all_emp_list

# GET Employee by ID
async def select_employee_id(id: int) -> Employee:
    cursor = getDBCursor()
    cursor.execute("SELECT * FROM employees WHERE emp_id = ?", (id,))
    output = cursor.fetchone()

    close_connection()
    return await row_to_employee(output) if output else Employee()

# POST new Employee
async def create_new_employee(new_emp: Employee) -> Employee:
    conn = getDBConnection()
    cursor = conn.cursor()

    try:
        cursor.execute("INSERT INTO employees(emp_name, emp_phone, emp_ssn, emp_address, emp_work_percentage, emp_cash_percentage, emp_salary) VALUES(?, ?, ?, ?, ?, ?, ?)",
                       (new_emp.emp_name, new_emp.emp_phone, new_emp.emp_ssn, new_emp.emp_address, new_emp.emp_work_percentage, new_emp.emp_cash_percentage, new_emp.emp_salary))
        conn.commit()
    except Error as e:
        print(e)
        conn.rollback()
        close_connection()
        return Employee()
    
    cursor.execute("SELECT emp_id FROM employees ORDER BY emp_id DESC LIMIT 1")
    new_emp.emp_id = cursor.fetchone()[0]

    close_connection()
    return new_emp

# PUT existing Employee
async def update_existing_employee(exist_emp: Employee) -> Employee:
    conn = getDBConnection()
    cursor = conn.cursor()

    try:
        cursor.execute("UPDATE employees SET emp_name=?, emp_phone=?, emp_ssn=?, emp_address=?, emp_work_percentage=?, emp_cash_percentage=?, emp_salary=? WHERE emp_id=?",
                       (exist_emp.emp_name, exist_emp.emp_phone, exist_emp.emp_ssn, exist_emp.emp_address, exist_emp.emp_work_percentage, exist_emp.emp_cash_percentage, exist_emp.emp_salary, exist_emp.emp_id))
        conn.commit()
    except Error as e:
        print(e)
        conn.rollback()
        close_connection()
        return Employee()
    
    close_connection()
    return exist_emp

# DELETE existing employee by ID
async def delete_existing_employee(exist_emp_id: int) -> Employee:
    conn = getDBConnection()
    cursor = conn.cursor()

    try:
        found_emp = await select_employee_id(exist_emp_id)
        if found_emp.emp_id != -1:
            cursor.execute("DELETE FROM employees WHERE emp_id=?", (exist_emp_id,))
            conn.commit()
        else:
            raise Error
    except Error as e:
        print(e)
        conn.rollback()
        close_connection()
        return Employee()
    
    close_connection()
    return found_emp