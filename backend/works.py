
class Works:
    def __init__(self, id, datetime, amount, tip, discount, grandtotal, notes) -> None:
        self.work_id = id
        self.work_datetime = datetime
        self.work_amount = amount
        self.work_tip = tip
        self.work_discount = discount
        self.work_grandtotal = grandtotal
        self.work_notes = notes
