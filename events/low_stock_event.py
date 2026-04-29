class LowStockEvent:
    """
    <<Event>>
    Triggered when a product's stock falls below a critical threshold.
    """
    def __init__(self, kiosk_id: str, product_id: str, current_stock: int):
        self.kiosk_id = kiosk_id
        self.product_id = product_id
        self.current_stock = current_stock
        self.event_name = "LowStockEvent"

    def __str__(self):
        return f"Event[LowStock] Kiosk:{self.kiosk_id} Product:{self.product_id} Stock:{self.current_stock}"
