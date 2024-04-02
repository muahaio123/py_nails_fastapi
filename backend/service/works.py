from dataclasses import dataclass

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
    