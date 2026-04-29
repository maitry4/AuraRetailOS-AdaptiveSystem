"""
core/kiosk_interface.py
PATTERN 1 — Facade
KioskInterface: the ONLY entry point that external callers (city dashboards,
mobile apps, operator consoles) are permitted to use.
Hides: KioskCore, InventoryManager, HardwareController, CentralRegistry.
"""
from core.kiosk_core import KioskCore
from core.central_registry import CentralRegistry
from factory.kiosk_factory import KioskFactory
from hardware.hardware_controller import HardwareController
from inventory.inventory_manager import InventoryManager
from modes.active_mode import ActiveMode
from modes.maintenance_mode import MaintenanceMode
from modes.emergency_lockdown_mode import EmergencyLockdownMode
from modes.power_saving_mode import PowerSavingMode


class KioskInterface:
    """
    <<Facade>> Single, simplified entry point for external interaction.

    External callers NEVER touch KioskCore or lower layers directly.
    Four public operations match the diagram exactly:
      - purchaseItem(productId, userId)
      - refundTransaction(txId)
      - runDiagnostics()
      - restockInventory(productId, qty)

    Also exposes kiosk-lifecycle helpers used during bootstrapping.
    """

    def __init__(self, kiosk_id: str, factory: KioskFactory, initial_stock: dict = None):
        """
        Build a complete kiosk from a factory.
        The factory supplies the compatible component family (Pattern 3).
        The KioskCore starts in ActiveMode (Pattern 4).
        The kiosk registers itself with CentralRegistry (Pattern 2).
        """
        print(f"\n[KioskInterface] Building kiosk '{kiosk_id}' using {factory.factory_name}...")

        # Abstract Factory creates the compatible component family
        dispenser    = factory.create_dispenser()
        sensor       = factory.create_sensor()
        verification = factory.create_verification_module()
        policy       = factory.create_inventory_policy()

        hw_controller = HardwareController(dispenser, sensor, verification)
        inv_manager   = InventoryManager(initial_stock or {})

        self._core = KioskCore(
            kiosk_id=kiosk_id,
            hardware_controller=hw_controller,
            inventory_manager=inv_manager,
            inventory_policy=policy,
            initial_mode=ActiveMode(),
        )

        # Singleton: register with the central registry
        registry = CentralRegistry.get_instance()
        registry.register_kiosk(self._core)

        print(f"[KioskInterface] Kiosk '{kiosk_id}' ready. Status: {self._core.operational_status}\n")

    # -- Public Facade API ----------------------------------------------------

    def purchase_item(self, product_id: str, user_id: str) -> bool:
        """External entry point for a purchase transaction."""
        print(f"\n{'-'*50}")
        print(f"[Facade] purchaseItem(product='{product_id}', user='{user_id}')")
        result = self._core.handle_request({
            "action": "purchase",
            "product_id": product_id,
            "user_id": user_id,
        })
        if result:
            CentralRegistry.get_instance().increment_transactions()
        print(f"[Facade] Result: {'SUCCESS OK' if result else 'FAILED FAILED'}")
        return result

    def refund_transaction(self, tx_id: str) -> bool:
        """External entry point for a refund."""
        print(f"\n{'-'*50}")
        print(f"[Facade] refundTransaction(txId='{tx_id}')")
        result = self._core.handle_request({"action": "refund", "tx_id": tx_id})
        print(f"[Facade] Result: {'SUCCESS OK' if result else 'FAILED FAILED'}")
        return result

    def run_diagnostics(self) -> dict:
        """External entry point to run hardware and software diagnostics."""
        print(f"\n{'-'*50}")
        print(f"[Facade] runDiagnostics()")
        result = self._core.current_mode.run_diagnostics(self._core)
        print(f"[Facade] Diagnostics report: {result}")
        return result

    def restock_inventory(self, product_id: str, qty: int) -> bool:
        """External entry point for restocking a product."""
        print(f"\n{'-'*50}")
        print(f"[Facade] restockInventory(product='{product_id}', qty={qty})")
        result = self._core.handle_request({
            "action": "restock",
            "product_id": product_id,
            "qty": qty,
        })
        print(f"[Facade] Result: {'SUCCESS OK' if result else 'FAILED FAILED'}")
        return result

    # -- Mode-switching helpers (operator use only, still via Facade) ---------

    def set_maintenance_mode(self) -> None:
        print(f"\n[Facade] Switching '{self._core.kiosk_id}' to MAINTENANCE mode.")
        self._core.switch_mode(MaintenanceMode())
        CentralRegistry.get_instance().update_status(self._core.kiosk_id, "MAINTENANCE")

    def set_active_mode(self) -> None:
        print(f"\n[Facade] Switching '{self._core.kiosk_id}' to ACTIVE mode.")
        self._core.switch_mode(ActiveMode())
        CentralRegistry.get_instance().update_status(self._core.kiosk_id, "ACTIVE")

    def set_power_saving_mode(self) -> None:
        print(f"\n[Facade] Switching '{self._core.kiosk_id}' to POWER_SAVING mode.")
        self._core.switch_mode(PowerSavingMode())

    def activate_emergency_lockdown(self) -> None:
        print(f"\n[Facade] !  EMERGENCY LOCKDOWN on '{self._core.kiosk_id}'.")
        self._core.switch_mode(EmergencyLockdownMode())
        CentralRegistry.get_instance().activate_emergency()

    # -- Status & Reporting ---------------------------------------------------
    
    def get_inventory_report(self) -> list:
        """
        Returns a list of dicts describing inventory with adaptive prices.
        Hides InventoryManager and PricingStrategy from the UI.
        """
        stock = self._core.inventory_manager.list_stock()
        report = []
        for pid, qty in stock.items():
            # Assume 10.0 base price for demo
            price = self._core.pricing_strategy.compute_price(pid, 10.0)
            report.append({"id": pid, "stock": qty, "price": float(price)})
        return report

    def get_verification_info(self) -> dict:
        """
        Returns kiosk-specific verification policy details.
        Hides VerificationModule details from the UI.
        """
        # Logic moved from UI to Facade/Subsystem
        v_module = self._core.hardware_controller.get_verification()
        
        info = {
            "policy": "Open (No Verification)",
            "users": []
        }

        # Introspect the verification module (could be formalised with an interface method)
        if hasattr(v_module, "VALID_PRESCRIPTIONS"):
            info["policy"] = "Restricted (Prescription Required)"
            info["users"] = list(v_module.VALID_PRESCRIPTIONS)
        elif v_module.__class__.__name__ == "AgeVerifier":
            info["policy"] = "Semi-Restricted (Age Verification)"

        return info

    @property
    def status(self) -> str:
        return self._core.operational_status

    @property
    def kiosk_id(self) -> str:
        return self._core.kiosk_id
