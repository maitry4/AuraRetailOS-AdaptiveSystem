"""modes/power_saving_mode.py — Reduced ops; wakes to Active on user interaction."""
from modes.kiosk_mode import KioskMode

class PowerSavingMode(KioskMode):
    @property
    def mode_name(self) -> str:
        return "POWER_SAVING"

    def _wake(self, ctx) -> None:
        from modes.active_mode import ActiveMode
        print("  [PowerSavingMode] Waking kiosk to ActiveMode...")
        ctx.switch_mode(ActiveMode())

    def handle_purchase(self, ctx, product_id: str, user_id: str) -> bool:
        print("  [PowerSavingMode] Purchase triggered — waking kiosk.")
        self._wake(ctx)
        return ctx.current_mode.handle_purchase(ctx, product_id, user_id)

    def handle_refund(self, ctx, tx_id: str) -> bool:
        print("  [PowerSavingMode] Refund triggered — waking kiosk.")
        self._wake(ctx)
        return ctx.current_mode.handle_refund(ctx, tx_id)

    def handle_restock(self, ctx, product_id: str, qty: int) -> bool:
        print("  [PowerSavingMode] Restock triggered — waking kiosk.")
        self._wake(ctx)
        return ctx.current_mode.handle_restock(ctx, product_id, qty)

    def run_diagnostics(self, ctx) -> dict:
        return {"mode": self.mode_name, "note": "Diagnostics available — kiosk in low-power state."}
