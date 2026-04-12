"""
modes/emergency_lockdown_mode.py
EMERGENCY (Priority Override) — Most ops disabled; essential items only with quantity cap.
EmergencyLockdownMode overrides all other states immediately on EmergencyModeActivated event.
"""
from modes.kiosk_mode import KioskMode

class EmergencyLockdownMode(KioskMode):
    ESSENTIAL_PRODUCTS = {"water", "first_aid_kit", "emergency_ration"}

    @property
    def mode_name(self) -> str:
        return "EMERGENCY_LOCKDOWN"

    def handle_purchase(self, ctx, product_id: str, user_id: str) -> bool:
        print(f"  [EmergencyLockdown] Purchase request for '{product_id}'.")
        if product_id not in self.ESSENTIAL_PRODUCTS:
            print(f"  [EmergencyLockdown] ✗ Non-essential product denied during emergency.")
            return False
        available = ctx.inventory_manager.get_available_stock(product_id)
        policy_ctx = {"available_stock": available}
        if not ctx.inventory_policy.can_purchase(product_id, 1, policy_ctx):
            return False
        reserved = ctx.inventory_manager.reserve(product_id, 1)
        if not reserved:
            print("  [EmergencyLockdown] Insufficient stock.")
            return False
        dispensed = ctx.hardware_controller.get_dispenser().dispense(product_id)
        if dispensed:
            ctx.inventory_manager.commit(product_id, 1)
            ctx.inventory_policy.on_purchase_complete(product_id, 1)
            print(f"  [EmergencyLockdown] ✓ Essential item dispensed.")
            return True
        ctx.inventory_manager.release_reservation(product_id, 1)
        return False

    def handle_refund(self, ctx, tx_id: str) -> bool:
        print("  [EmergencyLockdown] ✗ Refunds suspended during emergency.")
        return False

    def handle_restock(self, ctx, product_id: str, qty: int) -> bool:
        print(f"  [EmergencyLockdown] Emergency restock: '{product_id}' +{qty}.")
        ctx.inventory_manager.restock(product_id, qty)
        return True

    def run_diagnostics(self, ctx) -> dict:
        return {"mode": self.mode_name, "alert": "EMERGENCY LOCKDOWN ACTIVE", "hw_healthy": ctx.hardware_controller.is_healthy()}
