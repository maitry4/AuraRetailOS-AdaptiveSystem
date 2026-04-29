"""
main.py — Aura Retail OS  |  Patterns 1–4 Demo
================================================
Demonstrates all four patterns in a single terminal run:

  Pattern 1 — Facade        : KioskInterface is the only external entry point
  Pattern 2 — Singleton     : CentralRegistry shared across all kiosks
  Pattern 3 — Abstract Factory: Three kiosk types built from three factories
  Pattern 4 — State         : Runtime mode switching changes behaviour

Run:  python main.py
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from core.kiosk_interface import KioskInterface
from core.central_registry import CentralRegistry
from factory.pharmacy_kiosk_factory import PharmacyKioskFactory
from factory.food_kiosk_factory import FoodKioskFactory
from factory.emergency_kiosk_factory import EmergencyKioskFactory


DIVIDER = "\n" + "=" * 55

def section(title: str) -> None:
    print(f"{DIVIDER}\n  {title}{DIVIDER}")


# -------------------------------------------------------------
# PATTERN 2 DEMO — Singleton: same registry instance everywhere
# -------------------------------------------------------------
def demo_singleton() -> None:
    section("PATTERN 2 — Singleton: CentralRegistry")

    r1 = CentralRegistry.get_instance()
    r2 = CentralRegistry.get_instance()
    # Note: CentralRegistry() constructor is internal/private in a strict singleton, 
    # but here we allow it to return the instance for demo purposes.
    r3 = CentralRegistry() 

    print(f"\n  r1 is r2 : {r1 is r2}")   # True
    print(f"  r2 is r3 : {r2 is r3}")   # True
    print(f"  id(r1)   : {id(r1)}")
    print(f"  id(r2)   : {id(r2)}")
    print(f"\n  System name : {r1.get_config().system_name}")
    print(f"  Version     : {r1.get_config().version}")


# -------------------------------------------------------------
# PATTERN 3 DEMO — Abstract Factory: 3 kiosk types, 3 factories
# -------------------------------------------------------------
def build_kiosks() -> tuple:
    section("PATTERN 3 — Abstract Factory: Building Kiosks")

    pharmacy_kiosk = KioskInterface(
        kiosk_id="PHARMA-01",
        factory=PharmacyKioskFactory(),
        initial_stock={"amoxicillin": 10, "ibuprofen": 20},
    )

    food_kiosk = KioskInterface(
        kiosk_id="FOOD-01",
        factory=FoodKioskFactory(),
        initial_stock={"sandwich": 15, "water": 30, "chips": 25},
    )

    emergency_kiosk = KioskInterface(
        kiosk_id="EMERG-01",
        factory=EmergencyKioskFactory(),
        initial_stock={"water": 50, "first_aid_kit": 20, "emergency_ration": 30},
    )

    return pharmacy_kiosk, food_kiosk, emergency_kiosk


# -------------------------------------------------------------
# PATTERN 1 DEMO — Facade: external callers use only 4 methods
# -------------------------------------------------------------
def demo_facade(pharmacy: KioskInterface, food: KioskInterface, emergency: KioskInterface) -> None:
    section("PATTERN 1 — Facade: KioskInterface as sole entry point")

    print("\n  > PHARMACY KIOSK — valid prescription purchase")
    pharmacy.purchase_item("amoxicillin", "user_alice")

    print("\n  > PHARMACY KIOSK — invalid prescription (should be denied)")
    pharmacy.purchase_item("amoxicillin", "user_charlie")

    print("\n  > FOOD KIOSK — normal purchase")
    food.purchase_item("sandwich", "user_bob")

    print("\n  > FOOD KIOSK — refund")
    food.refund_transaction("TX-9901")

    print("\n  > EMERGENCY KIOSK — essential item purchase")
    emergency.purchase_item("water", "user_dave")

    print("\n  > FOOD KIOSK — diagnostics via Facade")
    food.run_diagnostics()

    print("\n  > FOOD KIOSK — restock via Facade")
    food.restock_inventory("sandwich", 10)


# -------------------------------------------------------------
# PATTERN 4 DEMO — State: runtime mode changes alter behaviour
# -------------------------------------------------------------
def demo_state(food: KioskInterface, emergency: KioskInterface) -> None:
    section("PATTERN 4 — State: Mode Switching Changes Behaviour")

    # --- Maintenance Mode ---
    print("\n  -- Switching Food kiosk to MAINTENANCE --")
    food.set_maintenance_mode()

    print("\n  > Purchase attempt while in MAINTENANCE (should be blocked):")
    food.purchase_item("chips", "user_eve")

    print("\n  > Restock IS allowed in MAINTENANCE:")
    food.restock_inventory("chips", 50)

    print("\n  > Diagnostics IS allowed in MAINTENANCE:")
    food.run_diagnostics()

    # --- Back to Active ---
    print("\n  -- Restoring Food kiosk to ACTIVE --")
    food.set_active_mode()
    print("\n  > Purchase now works again:")
    food.purchase_item("chips", "user_eve")

    # --- Power Saving -> auto-wake ---
    print("\n  -- Switching Food kiosk to POWER_SAVING --")
    food.set_power_saving_mode()
    print("\n  > Purchase triggers auto-wake to ActiveMode:")
    food.purchase_item("water", "user_frank")

    # --- Emergency Lockdown ---
    print("\n  -- Activating EMERGENCY LOCKDOWN on Emergency kiosk --")
    emergency.activate_emergency_lockdown()

    print("\n  > Non-essential item blocked in lockdown:")
    emergency.purchase_item("chips", "user_grace")

    print("\n  > Essential item allowed (with quantity cap):")
    emergency.purchase_item("first_aid_kit", "user_grace")

    print("\n  > Refund blocked in lockdown:")
    emergency.refund_transaction("TX-0042")


# -------------------------------------------------------------
# REGISTRY SUMMARY — shows Singleton aggregated everything
# -------------------------------------------------------------
def show_registry_summary() -> None:
    section("PATTERN 2 — Singleton Summary: CentralRegistry State")
    registry = CentralRegistry.get_instance()
    print(registry.summary())
    print("\n  Registered kiosks:")
    for kid, status in registry.list_kiosks().items():
        print(f"    - {kid:15s}  ->  {status}")


# -------------------------------------------------------------
# ENTRY POINT
# -------------------------------------------------------------
if __name__ == "__main__":
    print("\n" + "#" * 55)
    print("  AURA RETAIL OS  -  Simulation Run")
    print("  Facade . Singleton . Abstract Factory . State")
    print("#" * 55)

    demo_singleton()
    pharmacy, food, emergency = build_kiosks()
    demo_facade(pharmacy, food, emergency)
    demo_state(food, emergency)
    show_registry_summary()

    print(f"\n{'-'*55}")
    print("  Demo complete.")
    print("-" * 55 + "\n")
