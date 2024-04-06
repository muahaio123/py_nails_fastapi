from dataclasses import dataclass
from sqlite3 import Error
from typing import Any
from database import pool

@dataclass
class Detail:
    detail_id: int = -1
    work_id: int = 0
    emp_id: int = 0
    emp_amount: float = 0
    emp_tip: float = 0
    detail_notes: str = ""
    
# Implement all 4 CRUD operations on emp_work_detail table
# Implement all 4 CRUD operations on Detail table
async def row_to_detail(row: list[Any]):
    return Detail(row[0], row[1], row[2], row[3], row[4], row[5])

async def list_to_detail(rows: list[Any]):
    return [await row_to_detail(row) for row in rows]

# GET all emp_work_detail
async def select_all_detail() -> list[Detail]:
    with pool.connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM emp_work_detail")
        output = cursor.fetchall()
        
    return await list_to_detail(output)

# GET emp_work_detail by ID
async def select_detail_id(id: int) -> Detail:
    with pool.connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM emp_work_detail WHERE detail_id = ?", (id,))
        output = cursor.fetchone()

    return await row_to_detail(output) if output else Detail()

# GET emp_work_detail by list of work_id(s):
async def select_detail_workdids(work_ids: list[int]) -> list[Detail]:
    with pool.connection() as conn:
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM emp_work_detail WHERE work_id IN (?)", (', '.join(map(str, work_ids)),))
        output = cursor.fetchall()
    
    return await list_to_detail(output)

# GET emp_work_detail by emp_id and list of work_id(s):
async def select_detail_between_dates(emp_id: int, work_ids: list[int]) -> list[Detail]:
    with pool.connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM emp_work_detail WHERE emp_id = ? AND work_id IN (?)", (emp_id, ', '.join(map(str, work_ids))))
        output = cursor.fetchall()
    
    return await list_to_detail(output)

# POST / create new emp_work_detail
async def create_new_detail(new_detail: Detail) -> Detail:
    with pool.connection() as conn:
        cursor = conn.cursor()

        try:
            cursor.execute("INSERT INTO emp_work_detail(detail_id, work_id, emp_id, emp_amount, emp_tip, detail_notes) VALUES(?, ?, ?, ?, ?, ?)",
                        (new_detail.detail_id, new_detail.work_id, new_detail.emp_id, new_detail.emp_amount, new_detail.emp_tip, new_detail.detail_notes))
            cursor.execute("SELECT detail_id FROM emp_work_detail ORDER BY detail_id DESC LIMIT 1")
            new_detail.work_id = cursor.fetchone()[0]
            conn.commit()
        except Error as e:
            print(e)
            conn.rollback()
            return Detail()
        
    return new_detail

# PUT / update existing emp_work_detail
async def update_existing_detail(exist_detail: Detail) -> Detail:
    with pool.connection() as conn:
        cursor = conn.cursor()

        try:
            found_detail = await select_detail_id(exist_detail.detail_id)
            if found_detail != -1:
                cursor.execute("UPDATE emp_work_detail SET work_id=?, emp_id=?, emp_amount=?, emp_tip=?, detail_notes=? WHERE detail_id=?",
                            (exist_detail.work_id, exist_detail.emp_id, exist_detail.emp_amount, exist_detail.emp_tip, exist_detail.detail_notes, exist_detail.detail_id))
                conn.commit()
            else:
                raise Error
        except Error as e:
            print(e)
            conn.rollback()
            return Detail()
    
    return exist_detail

# DELETE existing detail by ID
async def delete_existing_work(exist_detail_id: int) -> Detail:
    with pool.connection() as conn:
        cursor = conn.cursor()

        try:
            found_detail = await select_detail_id(exist_detail_id)
            if found_detail.work_id != -1:
                cursor.execute("DELETE FROM emp_work_detail WHERE detail_id=?", (exist_detail_id,))
                conn.commit()
            else:
                raise Error
        except Error as e:
            print(e)
            conn.rollback()
            return Detail()
    
    return found_detail
    
