"""modes/active_mode.py — Full normal operation; purchases and refunds allowed."""
from modes.kiosk_mode import KioskMode

class ActiveMode(KioskMode):
    @property
    def mode_name(self) -> str:
        return "ACTIVE"

    def handle_purchase(self, ctx, product_id: str, user_id: str) -> bool:
        print(f"  [ActiveMode] Processing purchase: product='{product_id}', user='{user_id}'")
        hw = ctx.hardware_controller
        if not hw.is_healthy():
            print("  [ActiveMode] Hardware not healthy — purchase aborted.")
            return False
        if not hw.get_verification().verify(user_id, product_id):
            print("  [ActiveMode] Verification failed — purchase denied.")
            return False
        available = ctx.inventory_manager.get_available_stock(product_id)
        policy_ctx = {"available_stock": available}
        if not ctx.inventory_policy.can_purchase(product_id, 1, policy_ctx):
            return False
        reserved = ctx.inventory_manager.reserve(product_id, 1)
        if not reserved:
            print("  [ActiveMode] Could not reserve stock.")
            return False
        dispensed = hw.get_dispenser().dispense(product_id)
        if dispensed:
            ctx.inventory_manager.commit(product_id, 1)
            ctx.inventory_policy.on_purchase_complete(product_id, 1)
            print(f"  [ActiveMode] ✓ Purchase successful.")
            return True
        else:
            ctx.inventory_manager.release_reservation(product_id, 1)
            print("  [ActiveMode] Dispense failed — reservation released.")
            return False

    def handle_refund(self, ctx, tx_id: str) -> bool:
        print(f"  [ActiveMode] Processing refund for transaction '{tx_id}'")
        print(f"  [ActiveMode] ✓ Refund approved.")
        return True

    def handle_restock(self, ctx, product_id: str, qty: int) -> bool:
        print(f"  [ActiveMode] Restocking '{product_id}' with {qty} units.")
        ctx.inventory_manager.restock(product_id, qty)
        return True

    def run_diagnostics(self, ctx) -> dict:
        healthy = ctx.hardware_controller.is_healthy()
        stock = ctx.inventory_manager.list_stock()
        return {"mode": self.mode_name, "hardware_healthy": healthy, "stock": stock}
