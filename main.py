"""
main.py - Aura Retail OS | Interactive System Shell
===================================================
A fully interactive console for managing the smart retail ecosystem.
Demonstrates 9 design patterns across 4 development phases.

Implemented Path: Path A (Transactional Integrity & Dynamic Pricing)
"""

import os
import sys
from typing import Dict

# Ensure local imports work
sys.path.insert(0, os.path.dirname(__file__))

from core.kiosk_interface import KioskInterface
from core.central_registry import CentralRegistry
from factory.pharmacy_kiosk_factory import PharmacyKioskFactory
from factory.food_kiosk_factory import FoodKioskFactory
from factory.emergency_kiosk_factory import EmergencyKioskFactory
from events.event_bus import EventBus
from events.emergency_mode_activated import EmergencyModeActivated
from pricing.discounted_pricing import DiscountedPricing
from pricing.emergency_pricing import EmergencyPricing

# Mock classes for hardware failure demo
from hardware.dispenser import Dispenser

class BrokenDispenser(Dispenser):
    def dispense(self, product_id: str) -> bool:
        print(f"\n  [HW_ERROR] !!! MOTOR STALL while releasing '{product_id}' !!!")
        return False
    def wait_for_completion(self) -> bool: return False
    def self_test(self) -> bool: return True
    @property
    def model_name(self) -> str: return "Faulty-X"

class BrokenFoodFactory(FoodKioskFactory):
    def create_dispenser(self) -> Dispenser: return BrokenDispenser()


class AuraShell:
    def __init__(self):
        self.registry = CentralRegistry.get_instance()
        self.bus = EventBus.get_instance()
        self.kiosks: Dict[str, KioskInterface] = {}
        self.current_kiosk: KioskInterface = None
        self._setup_subscribers()
        self._bootstrap()

    def _setup_subscribers(self):
        """Setup global monitoring observers."""
        self.bus.subscribe("TransactionCompleted", lambda e: print(f"\n  [Global Monitor] Tx Success: {e.product_id} at {e.kiosk_id}"))
        self.bus.subscribe("LowStockEvent", lambda e: print(f"\n  [Global Monitor] WARNING: Low stock for {e.product_id} at {e.kiosk_id} ({e.current_stock} left)"))
        self.bus.subscribe("HardwareFailureEvent", lambda e: print(f"\n  [Global Monitor] ALERT: Hardware failure at {e.kiosk_id}! Component: {e.component}"))

    def _bootstrap(self):
        """Initialize default kiosks."""
        print("\n[System] Bootstrapping Aura Retail OS...")
        self.kiosks["PHARMA-01"] = KioskInterface("PHARMA-01", PharmacyKioskFactory(), {"amoxicillin": 10, "ibuprofen": 5})
        self.kiosks["FOOD-01"] = KioskInterface("FOOD-01", FoodKioskFactory(), {"sandwich": 20, "water": 15})
        self.kiosks["EMERG-01"] = KioskInterface("EMERG-01", EmergencyKioskFactory(), {"water": 50, "first_aid": 10})
        self.current_kiosk = self.kiosks["FOOD-01"]

    def header(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print("="*60)
        print("             AURA RETAIL OS - INTERACTIVE SHELL")
        print("="*60)
        print(f"  Current Kiosk: {self.current_kiosk.kiosk_id} [{self.current_kiosk.status}]")
        print(f"  System Mode  : {'EMERGENCY' if self.registry.get_status().emergency_active else 'NORMAL'}")
        print("-" * 60)

    def run(self):
        while True:
            self.header()
            print("  1. Select Kiosk")
            print("  2. View Current Kiosk Inventory")
            print("  3. View Verification Info (Users)")
            print("  4. Purchase Item")
            print("  5. Restock Item")
            print("  6. View System Summary (CentralRegistry)")
            print("  7. Switch Kiosk Mode (State Pattern)")
            print("  8. Trigger City-Wide Emergency (EventBus)")
            print("  9. Simulate Hardware Failure (Chain of Resp/Memento)")
            print("  0. Exit")
            print("-" * 60)
            
            choice = input("Select an option: ")

            if choice == "1": self._select_kiosk()
            elif choice == "2": self._view_inventory()
            elif choice == "3": self._view_users()
            elif choice == "4": self._do_purchase()
            elif choice == "5": self._do_restock()
            elif choice == "6": self._view_summary()
            elif choice == "7": self._switch_mode()
            elif choice == "8": self._trigger_emergency()
            elif choice == "9": self._simulate_failure()
            elif choice == "0": break
            else: input("\nInvalid choice. Press Enter to continue...")

    def _select_kiosk(self):
        print("\nAvailable Kiosks:")
        for kid in self.kiosks:
            print(f"  - {kid}")
        kid = input("\nEnter Kiosk ID: ").upper()
        if kid in self.kiosks:
            self.current_kiosk = self.kiosks[kid]
        else:
            input("Kiosk not found. Press Enter...")

    def _view_inventory(self):
        print(f"\nInventory for {self.current_kiosk.kiosk_id}:")
        report = self.current_kiosk.get_inventory_report()
        if not report:
            print("  (Empty)")
        for item in report:
            print(f"  - {item['id']:15s} | Stock: {item['stock']:2d} | Est. Price: ${item['price']:.2f}")
        input("\nPress Enter to continue...")

    def _view_users(self):
        print(f"\nVerification Policy for {self.current_kiosk.kiosk_id}:")
        v_info = self.current_kiosk.get_verification_info()
        print(f"  Policy: {v_info['policy']}")
        if v_info["users"]:
            print("  Known Registered Users & Requirements:")
            for user in v_info["users"]:
                print(f"  - {user}")
        input("\nPress Enter to continue...")

    def _do_purchase(self):
        print(f"\n--- {self.current_kiosk.kiosk_id} Purchase ---")
        report = self.current_kiosk.get_inventory_report()
        print("Available Items:")
        valid_ids = []
        for item in report:
            print(f"  - {item['id']:15s} (Stock: {item['stock']})")
            valid_ids.append(item['id'])
            
        pid = input("\nEnter Product ID to buy: ")
        if pid not in valid_ids:
            print("  [Error] Product not found in this kiosk.")
            input("\nPress Enter to continue...")
            return

        uid = input("Enter User ID: ")
        self.current_kiosk.purchase_item(pid, uid)
        input("\nPress Enter to continue...")

    def _do_restock(self):
        pid = input("\nEnter Product ID: ")
        qty = int(input("Enter Quantity: "))
        self.current_kiosk.restock_inventory(pid, qty)
        input("\nPress Enter to continue...")

    def _view_summary(self):
        print(self.registry.summary())
        input("\nPress Enter to continue...")

    def _switch_mode(self):
        print("\nModes:")
        print("  1. Active")
        print("  2. Maintenance")
        print("  3. Power Saving")
        print("  4. Emergency Lockdown")
        m = input("\nSelect Mode: ")
        if m == "1": self.current_kiosk.set_active_mode()
        elif m == "2": self.current_kiosk.set_maintenance_mode()
        elif m == "3": self.current_kiosk.set_power_saving_mode()
        elif m == "4": self.current_kiosk.activate_emergency_lockdown()
        input("\nPress Enter to continue...")

    def _trigger_emergency(self):
        print("\n!!! DECLARING CITY-WIDE EMERGENCY !!!")
        self.registry.activate_emergency()
        self.bus.publish(EmergencyModeActivated(region="Global"))
        input("\nAll kiosks have transitioned. Press Enter to continue...")

    def _simulate_failure(self):
        print("\nInitializing Faulty Kiosk (FAULTY-01)...")
        faulty = KioskInterface("FAULTY-01", BrokenFoodFactory(), {"chips": 5})
        self.kiosks["FAULTY-01"] = faulty
        self.current_kiosk = faulty
        print("\n[System] Current kiosk switched to FAULTY-01.")
        print("[System] Attempting a purchase to trigger failure chain...")
        faulty.purchase_item("chips", "user_test")
        input("\nFailure handled. Press Enter to continue...")

if __name__ == "__main__":
    shell = AuraShell()
    shell.run()
