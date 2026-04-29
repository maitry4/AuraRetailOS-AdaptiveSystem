from modes.kiosk_mode import KioskMode
from commands.purchase_item_command import PurchaseItemCommand
from commands.refund_command import RefundCommand
from commands.restock_command import RestockCommand

class EmergencyLockdownMode(KioskMode):
    ESSENTIAL_PRODUCTS = {"water", "first_aid_kit", "emergency_ration"}

    @property
    def mode_name(self) -> str:
        return "EMERGENCY_LOCKDOWN"

    def handle_purchase(self, ctx, product_id: str, user_id: str) -> bool:
        print(f"  [EmergencyLockdown] Checking essential item status for '{product_id}'...")
        if product_id not in self.ESSENTIAL_PRODUCTS:
            print(f"  [EmergencyLockdown] X Non-essential product denied during emergency.")
            return False
        
        print(f"  [EmergencyLockdown] Creating PurchaseItemCommand (Essential Item)...")
        # In emergency mode, we might use a different pricing strategy (handled by Strategy pattern later)
        cmd = PurchaseItemCommand(ctx, product_id, user_id, ctx.pricing_strategy)
        return ctx.execute_command(cmd)

    def handle_refund(self, ctx, tx_id: str) -> bool:
        print("  [EmergencyLockdown] X Refunds suspended during emergency.")
        return False

    def handle_restock(self, ctx, product_id: str, qty: int) -> bool:
        print(f"  [EmergencyLockdown] Creating RestockCommand (Emergency Restock)...")
        cmd = RestockCommand(ctx, product_id, qty)
        return ctx.execute_command(cmd)

    def run_diagnostics(self, ctx) -> dict:
        return {"mode": self.mode_name, "alert": "EMERGENCY LOCKDOWN ACTIVE", "hw_healthy": ctx.hardware_controller.is_healthy()}
