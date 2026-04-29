"""inventory/standard_inventory_policy.py — Standard purchase policy."""
from inventory.inventory_policy import InventoryPolicy

class StandardInventoryPolicy(InventoryPolicy):
    def can_purchase(self, product_id: str, qty: int, ctx: dict) -> bool:
        available = ctx.get("available_stock", 0)
        if qty > available:
            print(f"      [StandardPolicy] Denied: only {available} units of '{product_id}' available.")
            return False
        return True

    def recommend_strategy(self, ctx: dict) -> str:
        """
        Phase 2: Adaptive Pricing Integration (Hardik's task)
        Returns the suggested strategy name based on context.
        """
        if ctx.get("emergency_active", False):
            return "EMERGENCY_SURCHARGE"
        
        available = ctx.get("available_stock", 0)
        if available > 15:
            return "DISCOUNTED"
            
        return "STANDARD"

    def on_purchase_complete(self, product_id: str, qty: int) -> None:
        print(f"      [StandardPolicy] Purchase logged: {qty}x '{product_id}'.")
