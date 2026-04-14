"""inventory/emergency_inventory_policy.py — Hard cap per transaction."""
from inventory.inventory_policy import InventoryPolicy

class EmergencyInventoryPolicy(InventoryPolicy):
    def __init__(self, max_qty: int = 2):
        self.max_qty = max_qty

    def can_purchase(self, product_id: str, qty: int, ctx: dict) -> bool:
        available = ctx.get("available_stock", 0)
        if qty > self.max_qty:
            print(f"      [EmergencyPolicy] Denied: max {self.max_qty} per transaction (requested {qty}).")
            return False
        if qty > available:
            print(f"      [EmergencyPolicy] Denied: only {available} units available.")
            return False
        return True

    def on_purchase_complete(self, product_id: str, qty: int) -> None:
        print(f"      [EmergencyPolicy] Emergency purchase: {qty}x '{product_id}' (cap={self.max_qty}).")
