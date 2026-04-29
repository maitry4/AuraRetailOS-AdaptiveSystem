"""
main.py - Aura Retail OS | Interactive System Shell
===================================================
A fully interactive console for managing the smart retail ecosystem.
Demonstrates 9 design patterns across 4 development phases.

Implemented Path: Path A (Transactional Integrity & Dynamic Pricing)
"""

import os
import sys
import time
import threading
from typing import Dict
# Ensure local imports work
sys.path.insert(0, os.path.dirname(__file__))

from events.transaction_completed import TransactionCompletedEvent

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
        import time
        time.sleep(0.5) # Simulate hardware spin-up failure delay
        return False
    def wait_for_completion(self) -> bool: 
        print("      [HW] waiting for completion signal... TIMEOUT.")
        return False
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
        self.bus.subscribe("TransactionCompleted", lambda e: print(f"  [Global Monitor] Tx Success: {e.product_id} at {e.kiosk_id}"))
        self.bus.subscribe("LowStockEvent", lambda e: print(f"  [Global Monitor] WARNING: Low stock for {e.product_id} at {e.kiosk_id} ({e.current_stock} left)"))
        self.bus.subscribe("HardwareFailureEvent", lambda e: print(f"  [Global Monitor] ALERT: Hardware failure at {e.kiosk_id}! Component: {e.component}"))
        self.bus.subscribe("EmergencyModeActivated", lambda e: print(f"  [Global Monitor] !!! EMERGENCY ALERT: Region {e.region} !!!"))

    def _bootstrap(self):
        """Initialize default kiosks."""
        print("\n[System] Bootstrapping Aura Retail OS...")
        self.kiosks["PHARMA-01"] = KioskInterface("PHARMA-01", PharmacyKioskFactory(), {"amoxicillin": 10, "ibuprofen": 5})
        self.kiosks["FOOD-01"] = KioskInterface("FOOD-01", FoodKioskFactory(), {"sandwich": 20, "water": 15})
        self.kiosks["EMERG-01"] = KioskInterface("EMERG-01", EmergencyKioskFactory(), {"water": 50, "first_aid": 10})
        self.current_kiosk = self.kiosks["FOOD-01"]

    def header(self):
        # os.system('cls' if os.name == 'nt' else 'clear') # Disabled for better scroll history during demo
        print("\n" + "="*70)
        print("             AURA RETAIL OS - INTERACTIVE SHELL")
        print("="*70)
        print(f"  Current Kiosk: {self.current_kiosk.kiosk_id} [{self.current_kiosk.status}]")
        print(f"  System Mode  : {'EMERGENCY' if self.registry.get_status().emergency_active else 'NORMAL'}")
        print("-" * 70)

    def run(self):
        while True:
            self.header()
            print("  1. Select Kiosk")
            print("  2. View Inventory & Pricing")
            print("  3. View Verification Info (Users)")
            print("  4. Purchase Item (Command Pattern)")
            print("  5. Refund / Undo Last Tx (Command/Memento)")
            print("  6. Run Mode-Specific Diagnostics (State Pattern)")
            print("  7. Switch Kiosk Mode (State Pattern)")
            print("  8. Switch Pricing Strategy (Strategy Pattern)")
            print("  9. ADVANCED: Simulate Scenarios (Concurrency/Failure/Priority)")
            print("  0. Exit")
            print("-" * 70)
            
            choice = input("Select an option: ")

            if choice == "1": self._select_kiosk()
            elif choice == "2": self._view_inventory()
            elif choice == "3": self._view_users()
            elif choice == "4": self._do_purchase()
            elif choice == "5": self._do_refund()
            elif choice == "6": self._run_diagnostics()
            elif choice == "7": self._switch_mode()
            elif choice == "8": self._switch_pricing()
            elif choice == "9": self._advanced_demos()
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
            print(f"  - {item['id']:15s} | Stock: {item['stock']:2d} | Price: ${item['price']:.2f}")
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
        valid_ids = [item['id'] for item in report]
        
        pid = input("Enter Product ID: ")
        if pid not in valid_ids:
            print("  [Error] Product not found.")
            return

        uid = input("Enter User ID: ")
        self.current_kiosk.purchase_item(pid, uid)
        input("\nPress Enter to continue...")

    def _do_refund(self):
        tx_id = input("\nEnter Transaction ID to refund (or 'LAST'): ")
        # In a real system, we'd lookup by ID. Here we just demo the Facade entry.
        self.current_kiosk.refund_transaction(tx_id)
        input("\nPress Enter to continue...")

    def _run_diagnostics(self):
        print(f"\nRunning diagnostics for {self.current_kiosk.kiosk_id}...")
        results = self.current_kiosk.run_diagnostics()
        print(f"Final Report: {results}")
        input("\nPress Enter to continue...")

    def _switch_mode(self):
        print("\nModes: 1.Active, 2.Maintenance, 3.PowerSaving, 4.Lockdown")
        m = input("Select Mode: ")
        if m == "1": self.current_kiosk.set_active_mode()
        elif m == "2": self.current_kiosk.set_maintenance_mode()
        elif m == "3": self.current_kiosk.set_power_saving_mode()
        elif m == "4": self.current_kiosk.activate_emergency_lockdown()
        input("\nPress Enter to continue...")

    def _switch_pricing(self):
        print("\nStrategies: 1.STANDARD, 2.DISCOUNTED, 3.EMERGENCY")
        s = input("Select Strategy: ")
        if s == "1": self.current_kiosk.set_pricing_strategy("STANDARD")
        elif s == "2": self.current_kiosk.set_pricing_strategy("DISCOUNTED")
        elif s == "3": self.current_kiosk.set_pricing_strategy("EMERGENCY")
        input("\nPress Enter to continue...")

    def _advanced_demos(self):
        print("\nADVANCED SCENARIOS:")
        print("  1. Concurrent Transactions (Threading/Locks Demo)")
        print("  2. Hardware Failure & Memento Rollback (Self-Healing Demo)")
        print("  3. Priority Event Routing (Emergency Overrides Demo)")
        print("  0. Back")
        
        choice = input("\nSelect Scenario: ")
        if choice == "1": self._demo_concurrency()
        elif choice == "2": self._demo_failure()
        elif choice == "3": self._demo_priority()

    def _demo_concurrency(self):
        print(f"\n[Scenario] Simulating 3 users buying the last 2 'water' at {self.current_kiosk.kiosk_id}...")
        
        def attempt_buy(user_id):
            print(f"  [Thread] User {user_id} starting purchase...")
            self.current_kiosk.purchase_item("water", f"user_{user_id}")

        threads = []
        for i in range(3):
            t = threading.Thread(target=attempt_buy, args=(i,))
            threads.append(t)
            t.start()

        for t in threads: t.join()
        input("\nAll threads finished. Check stock above. Press Enter...")

    def _demo_failure(self):
        print("\n[Scenario] Booting Faulty Kiosk with Broken Dispenser...")
        faulty = KioskInterface("FAULTY-01", BrokenFoodFactory(), {"chips": 1})
        print(f"  [System] Initial Chips Stock: 1")
        print("  [System] Attempting purchase (Failure handler will fail, triggering Rollback)")
        faulty.purchase_item("chips", "user_test")
        print(f"  [System] Post-Failure Chips Stock: {faulty.get_inventory_report()[0]['stock']} (Should be 1)")
        input("\nMemento rollback verified. Press Enter...")

    def _demo_priority(self):
        print("\n[Scenario] Demonstrating Priority Event Routing...")
        print("  1. We will push two 'Standard' events into the bus.")
        print("  2. We will push one 'High Priority' Emergency event.")
        print("  3. The Bus will then process them in priority order (0 before 1).")
        
        
        # Bypass immediate flush for demo
        original_flush = self.bus.flush
        self.bus.flush = lambda: None 
        
        print("\n  [Bus] Queueing Standard: apple")
        self.bus.publish(TransactionCompletedEvent("FOOD-01", "apple", 1.0))
        print("  [Bus] Queueing Standard: pear")
        self.bus.publish(TransactionCompletedEvent("FOOD-01", "pear", 1.0))
        
        print("  [Bus] Queueing HIGH PRIORITY: EmergencyModeActivated")
        self.bus.publish(EmergencyModeActivated(region="Global"))
        
        print("\n  --- STARTING DISPATCH (FLUSH) ---")
        self.bus.flush = original_flush
        self.bus.flush()
        
        input("\nNotice how Emergency (Priority 0) jumped to the front! Press Enter...")

if __name__ == "__main__":
    shell = AuraShell()
    shell.run()
