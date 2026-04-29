class TransactionCompletedEvent:
    """
    <<Event>>
    Published when a purchase transaction finishes successfully.
    """
    def __init__(self, kiosk_id: str, product_id: str, price: float):
        self.kiosk_id = kiosk_id
        self.product_id = product_id
        self.price = price
        self.event_name = "TransactionCompleted"

    def __str__(self):
        return f"Event[TransactionCompleted] Kiosk:{self.kiosk_id} Product:{self.product_id} Price:{self.price}"
