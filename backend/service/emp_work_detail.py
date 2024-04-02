from dataclasses import dataclass

@dataclass
class Detail:
    detail_id: int = -1
    work_id: int = 0
    emp_id: int = 0
    emp_amount: float = 0
    emp_tip: float = 0
    detail_notes: str = ""
    
    # Implement all 4 CRUD operations on emp_work_detail table
    
