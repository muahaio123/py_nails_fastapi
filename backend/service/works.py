from service.database import pool
from typing import Any
from sqlite3 import Error
from pydantic import BaseModel, field_validator
import logging

logger = logging.getLogger(__name__)

class Works(BaseModel):
    work_id: int = -1
    work_datetime: str = ""
    work_amount: float = 0
    work_tip: float = 0
    work_discount: float = 0
    work_grandtotal: float = 0
    work_notes: str = ""
    
    @field_validator('work_amount', 'work_tip', 'work_discount', 'work_grandtotal')
    @classmethod
    def validate_amounts(cls, v):
        if v < 0:
            raise ValueError('Amounts cannot be negative')
        return v

def getDefaultWorks() -> Works:
    return Works(work_id=-1, work_datetime="", work_amount=0, work_tip=0, work_discount=0, work_grandtotal=0, work_notes="")

# Implement all 4 CRUD operations on works table
def row_to_works(row: list[Any]):
    return Works(work_id=row[0], work_datetime=row[1], work_amount=row[2], work_tip=row[3], work_discount=row[4], work_grandtotal=row[5], work_notes=row[6])

def list_to_works(rows: list[Any]):
    return [row_to_works(row) for row in rows]

# GET all works
def select_all_works() -> list[Works]:
    with pool.connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM works")
        output = cursor.fetchall()
    
    return list_to_works(output)

# GET work by ID
def select_work_id(id: int) -> Works:
    with pool.connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM works WHERE work_id = ?", (id,))
        output = cursor.fetchone()

    return row_to_works(output) if output else getDefaultWorks()

# GET works between any 2 dates:
def select_works_between_dates(from_date: str, to_date: str) -> list[Works]:
    with pool.connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM works WHERE work_datetime BETWEEN ? AND ?", (from_date, to_date))
        output = cursor.fetchall()

    return list_to_works(output)


# POST / create new works
def create_new_work(new_work: Works) -> Works:
    with pool.connection() as conn:
        cursor = conn.cursor()

        try:
            cursor.execute("INSERT INTO works(work_datetime, work_amount, work_tip, work_discount, work_grandtotal, work_notes) VALUES(?, ?, ?, ?, ?, ?)",
                        (new_work.work_datetime, new_work.work_amount, new_work.work_tip, new_work.work_discount, new_work.work_grandtotal, new_work.work_notes))
            cursor.execute("SELECT work_id FROM works ORDER BY work_id DESC LIMIT 1")
            new_work.work_id = cursor.fetchone()[0]
            conn.commit()
            logger.info(f"Work created: {new_work.work_id} on {new_work.work_datetime}")
        except Error as e:
            logger.error(f"Database error creating work: {e}")
            conn.rollback()
            return getDefaultWorks()

    return new_work

# PUT / update existing work
def update_existing_work(exist_work: Works) -> Works:
    with pool.connection() as conn:
        cursor = conn.cursor()

        try:
            found_work = select_work_id(exist_work.work_id)
            if found_work.work_id != -1:
                cursor.execute("UPDATE works SET work_datetime=?, work_amount=?, work_tip=?, work_discount=?, work_grandtotal=?, work_notes=? WHERE work_id=?",
                            (exist_work.work_datetime, exist_work.work_amount, exist_work.work_tip, exist_work.work_discount, exist_work.work_grandtotal, exist_work.work_notes, exist_work.work_id))
                conn.commit()
                logger.info(f"Work updated: {exist_work.work_id}")
            else:
                raise Error(f"work_id={found_work.work_id} cannot be found in table:works")
        except Error as e:
            logger.error(f"Database error updating work {exist_work.work_id}: {e}")
            conn.rollback()
            return getDefaultWorks()
    
    return exist_work

# DELETE existing work by ID
def delete_existing_work(exist_work_id: int) -> Works:
    with pool.connection() as conn:
        cursor = conn.cursor()

        try:
            found_work = select_work_id(exist_work_id)
            if found_work.work_id != -1:
                cursor.execute("DELETE FROM works WHERE work_id=?", (exist_work_id,))
                conn.commit()
                logger.info(f"Work deleted: {exist_work_id}")
            else:
                raise Error(f"work_id={found_work.work_id} cannot be found in table:works")
        except Error as e:
            logger.error(f"Database error deleting work {exist_work_id}: {e}")
            conn.rollback()
            return getDefaultWorks()
    
    return found_work
    