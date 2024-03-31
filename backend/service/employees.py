from typing import Any
from service.database import getDBConnection, getDBCursor, close_connection
from sqlite3 import Error

class Employee:
    def __init__(self, id=None, name=None, phone=None, ssn=None, address=None, work_perc=None, cash_perc=None, salary=None) -> None:
        self.emp_id = id
        self.emp_name = name
        self.emp_phone = phone
        self.emp_ssn = ssn
        self.emp_address = address
        self.emp_work_percentage = work_perc
        self.emp_cash_percentage = cash_perc
        self.emp_salary = salary

# Implement all 4 CRUD operations on employees
def row_to_employee(row: list[Any]):
    return Employee(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7])

# GET all employees
def select_all_employees() -> list[Employee]:
    cursor = getDBCursor()
    cursor.execute("SELECT * FROM employees")
    output = cursor.fetchall()

    all_emp_list: list[Employee] = []
    for row in output:
        all_emp_list.append(row_to_employee(row))
    
    close_connection()
    return all_emp_list

# GET Employee by ID
def select_employee_id(id: int) -> Employee:
    cursor = getDBCursor()
    cursor.execute(f"SELECT * FROM employees WHERE id = {id}")
    output = cursor.fetchone()

    close_connection()
    return row_to_employee(output) if output else Employee()

# POST new Employee
def create_new_employee(new_emp: Employee) -> Employee:
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
    
    cursor.execute("SELECT last_insert_rowid()")
    new_emp.emp_id = cursor.fetchone()[0]

    close_connection()
    return new_emp

# PUT existing Employee
def update_existing_employee(exist_emp: Employee) -> Employee:
    conn = getDBConnection()
    cursor = conn.cursor()

    try:
        cursor.execute("UPDATE employees SET emp_name=?, emp_phone=?, emp_ssn=?, emp_address=?, emp_work_percentage=?, emp_cash_percentage=?, emp_salary=?",
                       (exist_emp.emp_name, exist_emp.emp_phone, exist_emp.emp_ssn, exist_emp.emp_address, exist_emp.emp_work_percentage, exist_emp.emp_cash_percentage, exist_emp.emp_salary))
        conn.commit()
    except Error as e:
        print(e)
        conn.rollback()
        close_connection()
        return Employee()
    
    close_connection()
    return exist_emp

# DELETE existing employee by ID
def delete_existing_employee(exist_emp_id: int) -> Employee:
    conn = getDBConnection()
    cursor = conn.cursor()

    try:
        found_emp = select_employee_id(exist_emp_id)
        if found_emp.emp_id:
            cursor.execute("DELETE employees WHERE emp_id=?", (found_emp.emp_id,))
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