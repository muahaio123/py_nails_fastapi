from dataclasses import dataclass

@dataclass
class Payments:
    pmt_id: int = -1
    work_id: int = 0
    pmt_amount: float = 0
    pmt_type: str = ""

    # Implement all 4 CRUD operations on Payments table
