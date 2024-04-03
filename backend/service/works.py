from dataclasses import dataclass
from service.database import getDBConnection, getDBCursor, close_connection
from typing import Any
from sqlite3 import Error


@dataclass
class Works:
    work_id: int = -1
    work_datetime: str = ""
    work_amount: float = 0
    work_tip: float = 0
    work_discount: float = 0
    work_grandtotal: float = 0
    work_notes: str = ""

    # Implement all 4 CRUD operations on works table
def row_to_works(row: list[Any]):
    return Works(row[0], row[1], row[2], row[3], row[4], row[5], row[6])

    # GET all employees
def select_all_employees() -> list[Works]:
    cursor = getDBCursor()
    cursor.execute("SELECT * FROM works")
    output = cursor.fetchall()

    all_emp_list: list[Works] = []
    for row in output:
        all_emp_list.append(row_to_works(row))
    
    close_connection()
    return all_emp_list

# GET Employee by ID
def select_employee_id(id: int) -> Works:
    cursor = getDBCursor()
    cursor.execute("SELECT * FROM works WHERE work_id = ?", (id,))
    output = cursor.fetchone()

    close_connection()
    return row_to_works(output) if output else Works()

# POST new Employee
def create_new_workloyee(new_work: Works) -> Works:
    conn = getDBConnection()
    cursor = conn.cursor()

    try:
        cursor.execute("INSERT INTO works(work_datetime, work_amount, work_tip, work_discount, work_grandtotal, work_notes) VALUES(?, ?, ?, ?, ?, ?)",
                       (new_work.work_datetime, new_work.work_amount, new_work.work_tip, new_work.work_discount, new_work.work_grandtotal, new_work.work_notes))
        conn.commit()
    except Error as e:
        print(e)
        conn.rollback()
        close_connection()
        return Works()
    
    cursor.execute("SELECT last_insert_rowid()")
    new_work.work_id = cursor.fetchone()[0]

    close_connection()
    return new_work

# PUT existing Employee
def update_existing_employee(exist_emp: Works) -> Works:
    conn = getDBConnection()
    cursor = conn.cursor()

    try:
        cursor.execute("UPDATE works SET work_datetime=?, work_amount=?, work_tip=?, work_discount=?, work_grandtotal=?, work_notes=? WHERE work_id=?",
                       (exist_emp.work_datetime, exist_emp.work_amount, exist_emp.work_tip, exist_emp.work_discount, exist_emp.work_grandtotal, exist_emp.work_notes, exist_emp.work_id))
        conn.commit()
    except Error as e:
        print(e)
        conn.rollback()
        close_connection()
        return Works()
    
    close_connection()
    return exist_emp

# DELETE existing employee by ID
def delete_existing_employee(exist_work_id: int) -> Works:
    conn = getDBConnection()
    cursor = conn.cursor()

    try:
        found_emp = select_employee_id(exist_work_id)
        if found_emp.work_id != -1:
            cursor.execute("DELETE FROM works WHERE work_id=?", (exist_work_id,))
            conn.commit()
        else:
            raise Error
    except Error as e:
        print(e)
        conn.rollback()
        close_connection()
        return Works()
    
    close_connection()
    return found_emp
    