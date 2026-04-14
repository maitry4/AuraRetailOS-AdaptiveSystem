"""inventory/standard_inventory_policy.py — Standard purchase policy."""
from inventory.inventory_policy import InventoryPolicy

class StandardInventoryPolicy(InventoryPolicy):
    def can_purchase(self, product_id: str, qty: int, ctx: dict) -> bool:
        available = ctx.get("available_stock", 0)
        if qty > available:
            print(f"      [StandardPolicy] Denied: only {available} units of '{product_id}' available.")
            return False
        return True

    def on_purchase_complete(self, product_id: str, qty: int) -> None:
        print(f"      [StandardPolicy] Purchase logged: {qty}x '{product_id}'.")
