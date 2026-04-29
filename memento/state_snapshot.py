import datetime

class StateSnapshot:
    """
    <<Memento>>
    Captures the state of inventory and transaction context before a dispense operation.
    """
    def __init__(self, product_id: str, stock_level: int, reservation_qty: int):
        self.product_id = product_id
        self.stock_level = stock_level
        self.reservation_qty = reservation_qty
        self.timestamp = datetime.datetime.now()

    def __repr__(self):
        return f"Snapshot[{self.product_id}] Stock:{self.stock_level} Reserved:{self.reservation_qty}"

    def __str__(self):
        return f"Snapshot[{self.product_id}] Pre-Stock:{self.stock_level} Reserved:{self.reservation_qty}"
