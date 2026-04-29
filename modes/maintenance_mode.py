"""modes/maintenance_mode.py — Purchases blocked; restock and diagnostics allowed."""
from modes.kiosk_mode import KioskMode

class MaintenanceMode(KioskMode):
    @property
    def mode_name(self) -> str:
        return "MAINTENANCE"

    def handle_purchase(self, ctx, product_id: str, user_id: str) -> bool:
        print("  [MaintenanceMode] X Purchases are BLOCKED during maintenance.")
        return False

    def handle_refund(self, ctx, tx_id: str) -> bool:
        print("  [MaintenanceMode] X Refunds are BLOCKED during maintenance.")
        return False

    def handle_restock(self, ctx, product_id: str, qty: int) -> bool:
        print(f"  [MaintenanceMode] Restock allowed: '{product_id}' +{qty} units.")
        ctx.inventory_manager.restock(product_id, qty)
        return True

    def run_diagnostics(self, ctx) -> dict:
        healthy = ctx.hardware_controller.is_healthy()
        sensor = ctx.hardware_controller.get_sensor().read_status()
        stock = ctx.inventory_manager.list_stock()
        return {
            "mode": self.mode_name,
            "hardware_healthy": healthy,
            "sensor": {"temp": sensor.temperature, "humidity": sensor.humidity, "blocked": sensor.is_blocked},
            "stock": stock,
        }
