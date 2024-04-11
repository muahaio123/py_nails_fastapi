from dataclasses import dataclass
from sqlite3 import Error
from typing import Any
from database import pool

@dataclass
class Payments:
    pmt_id: int = -1
    work_id: int = 0
    pmt_amount: float = 0
    pmt_type: str = ""

def getDefaultPayment() -> Payments:
    return Payments(pmt_id=-1, work_id=0, pmt_amount=0, pmt_type="")

# Implement all 4 CRUD operations on Payments table
async def row_to_payment(row: list[Any]):
    return Payments(pmt_id=row[0], work_id=row[1], pmt_amount=row[2], pmt_type=row[3])

async def list_to_payments(rows: list[Any]):
    return [await row_to_payment(row) for row in rows]

# GET all payments
async def select_all_payments() -> list[Payments]:
    with pool.connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM payments")
        output = cursor.fetchall()

    return await list_to_payments(output)

# GET payment by ID
async def select_payment_id(pmt_id: int) -> Payments:
    with pool.connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM payments WHERE pmt_id = ?", (pmt_id,))
        output = cursor.fetchone()

    return await row_to_payment(output) if output else getDefaultPayment()

# GET payments by list of pmt_ids(s):
async def select_payment_workdids(pmt_ids: list[int]) -> list[Payments]:
    with pool.connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM payments WHERE pmt_id IN (?)", (', '.join(map(str, pmt_ids)),))
        output = cursor.fetchall()
    
    return await list_to_payments(output)

# POST / create new payment
async def create_new_payment(new_payment: Payments) -> Payments:
    with pool.connection() as conn:
        cursor = conn.cursor()

        try:
            cursor.execute("INSERT INTO payments(detail_id, work_id, pmt_amount, pmt_type) VALUES(?, ?, ?, ?)",
                        (new_payment.pmt_id, new_payment.work_id, new_payment.pmt_amount, new_payment.pmt_type))
            cursor.execute("SELECT pmt_id FROM payments ORDER BY pmt_id DESC LIMIT 1")
            new_payment.work_id = cursor.fetchone()[0]
            conn.commit()
        except Error as e:
            print(e)
            conn.rollback()
            return getDefaultPayment()
        
    return new_payment

# PUT / update existing emp_work_detail
async def update_existing_payment(exist_pmt: Payments) -> Payments:
    with pool.connection() as conn:
        cursor = conn.cursor()

        try:
            found_detail = await select_payment_id(exist_pmt.pmt_id)
            if found_detail != -1:
                cursor.execute("UPDATE payments SET work_id=?, pmt_amount=?, pmt_type=? WHERE pmt_id=?",
                            (exist_pmt.work_id, exist_pmt.pmt_amount, exist_pmt.pmt_type, exist_pmt.pmt_id))
                conn.commit()
            else:
                raise Error(f"pmt_id={exist_pmt.pmt_id} cannot be found in table:payments")
        except Error as e:
            print(e)
            conn.rollback()
            return getDefaultPayment()
    
    return exist_pmt

# DELETE existing detail by ID
async def delete_existing_payment(exist_pmt_id: int) -> Payments:
    with pool.connection() as conn:
        cursor = conn.cursor()

        try:
            found_detail = await select_payment_id(exist_pmt_id)
            if found_detail.work_id != -1:
                cursor.execute("DELETE FROM payments WHERE pmt_id=?", (exist_pmt_id,))
                conn.commit()
            else:
                raise Error(f"pmt_id={exist_pmt_id} cannot be found in table:payments")
        except Error as e:
            print(e)
            conn.rollback()
            return getDefaultPayment()
    
    return found_detail