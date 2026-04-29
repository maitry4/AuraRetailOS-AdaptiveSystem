from modes.kiosk_mode import KioskMode
from commands.purchase_item_command import PurchaseItemCommand
from commands.refund_command import RefundCommand
from commands.restock_command import RestockCommand

class ActiveMode(KioskMode):
    @property
    def mode_name(self) -> str:
        return "ACTIVE"

    def handle_purchase(self, ctx, product_id: str, user_id: str) -> bool:
        print(f"  [ActiveMode] Creating PurchaseItemCommand...")
        cmd = PurchaseItemCommand(ctx, product_id, user_id, ctx.pricing_strategy)
        return ctx.execute_command(cmd)

    def handle_refund(self, ctx, tx_id: str) -> bool:
        print(f"  [ActiveMode] Creating RefundCommand...")
        cmd = RefundCommand(ctx, tx_id)
        return ctx.execute_command(cmd)

    def handle_restock(self, ctx, product_id: str, qty: int) -> bool:
        print(f"  [ActiveMode] Creating RestockCommand...")
        cmd = RestockCommand(ctx, product_id, qty)
        return ctx.execute_command(cmd)

    def run_diagnostics(self, ctx) -> dict:
        healthy = ctx.hardware_controller.is_healthy()
        stock = ctx.inventory_manager.list_stock()
        return {"mode": self.mode_name, "hardware_healthy": healthy, "stock": stock}
