from sqlite3 import Error
from typing import Any
from service.database import pool
from pydantic import BaseModel, field_validator
import logging

logger = logging.getLogger(__name__)

class Payments(BaseModel):
    pmt_id: int = -1
    work_id: int = 0
    pmt_amount: float = 0
    pmt_type: str = ""
    
    @field_validator('pmt_amount')
    @classmethod
    def validate_amount(cls, v):
        if v < 0:
            raise ValueError('Payment amount cannot be negative')
        return v

def getDefaultPayment() -> Payments:
    return Payments(pmt_id=-1, work_id=0, pmt_amount=0, pmt_type="")

# Implement all 4 CRUD operations on Payments table
def row_to_payment(row: list[Any]):
    return Payments(pmt_id=row[0], work_id=row[1], pmt_amount=row[2], pmt_type=row[3])

def list_to_payments(rows: list[Any]):
    return [row_to_payment(row) for row in rows]

# GET all payments
def select_all_payments() -> list[Payments]:
    with pool.connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM payments")
        output = cursor.fetchall()

    return list_to_payments(output)

# GET payment by ID
def select_payment_id(pmt_id: int) -> Payments:
    with pool.connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM payments WHERE pmt_id = ?", (pmt_id,))
        output = cursor.fetchone()

    return row_to_payment(output) if output else getDefaultPayment()

# GET payments by list of pmt_ids(s):
def select_payment_pmtids(pmt_ids: str) -> list[Payments]:
    with pool.connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM payments WHERE pmt_id IN (?)", (pmt_ids.replace('-', ','),))
        output = cursor.fetchall()
    
    return list_to_payments(output)

# POST / create new payment
def create_new_payment(new_payment: Payments) -> Payments:
    with pool.connection() as conn:
        cursor = conn.cursor()

        try:
            cursor.execute("INSERT INTO payments(work_id, pmt_amount, pmt_type) VALUES(?, ?, ?)",
                        (new_payment.work_id, new_payment.pmt_amount, new_payment.pmt_type))
            cursor.execute("SELECT pmt_id FROM payments ORDER BY pmt_id DESC LIMIT 1")
            new_payment.pmt_id = cursor.fetchone()[0]
            conn.commit()
            logger.info(f"Payment created: {new_payment.pmt_id} - ${new_payment.pmt_amount}")
        except Error as e:
            logger.error(f"Database error creating payment: {e}")
            conn.rollback()
            return getDefaultPayment()
        
    return new_payment

# PUT / update existing payment
def update_existing_payment(exist_pmt: Payments) -> Payments:
    with pool.connection() as conn:
        cursor = conn.cursor()

        try:
            found_detail = select_payment_id(exist_pmt.pmt_id)
            if found_detail.pmt_id != -1:
                cursor.execute("UPDATE payments SET work_id=?, pmt_amount=?, pmt_type=? WHERE pmt_id=?",
                            (exist_pmt.work_id, exist_pmt.pmt_amount, exist_pmt.pmt_type, exist_pmt.pmt_id))
                conn.commit()
                logger.info(f"Payment updated: {exist_pmt.pmt_id}")
            else:
                raise Error(f"pmt_id={exist_pmt.pmt_id} cannot be found in table:payments")
        except Error as e:
            logger.error(f"Database error updating payment {exist_pmt.pmt_id}: {e}")
            conn.rollback()
            return getDefaultPayment()
    
    return exist_pmt

# DELETE existing payment by ID
def delete_existing_payment(exist_pmt_id: int) -> Payments:
    with pool.connection() as conn:
        cursor = conn.cursor()

        try:
            found_detail = select_payment_id(exist_pmt_id)
            if found_detail.pmt_id != -1:
                cursor.execute("DELETE FROM payments WHERE pmt_id=?", (exist_pmt_id,))
                conn.commit()
                logger.info(f"Payment deleted: {exist_pmt_id}")
            else:
                raise Error(f"pmt_id={exist_pmt_id} cannot be found in table:payments")
        except Error as e:
            logger.error(f"Database error deleting payment {exist_pmt_id}: {e}")
            conn.rollback()
            return getDefaultPayment()
    
    return found_detail
