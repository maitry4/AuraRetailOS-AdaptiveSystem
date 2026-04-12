"""
factory/food_kiosk_factory.py
Concrete factory — produces components for food/snack kiosks.
"""
from factory.kiosk_factory import KioskFactory
from hardware.dispenser import Dispenser
from hardware.sensor_module import SensorModule, SensorData
from hardware.verification_module import VerificationModule
from inventory.inventory_policy import InventoryPolicy
from inventory.standard_inventory_policy import StandardInventoryPolicy

class ConveyorDispenser(Dispenser):
    def dispense(self, product_id: str) -> bool:
        print(f"      [ConveyorDispenser] Conveyor releasing food item '{product_id}'...")
        return True
    def self_test(self) -> bool:
        print("      [ConveyorDispenser] Self-test: conveyor motor OK.")
        return True

class FoodSensor(SensorModule):
    def read_status(self) -> SensorData:
        return SensorData(temperature=6.0, humidity=55.0, is_blocked=False)
    def calibrate(self) -> bool:
        print("      [FoodSensor] Calibrated.")
        return True

class AgeVerifier(VerificationModule):
    """Simple age check (always passes for demo — would call external ID service)."""
    def verify(self, user_id: str, product_id: str) -> bool:
        print(f"      [AgeVerifier] Age check for {user_id}: passed.")
        return True

class FoodKioskFactory(KioskFactory):
    @property
    def factory_name(self) -> str:
        return "FoodKioskFactory"

    def create_dispenser(self) -> Dispenser:
        return ConveyorDispenser()

    def create_sensor(self) -> SensorModule:
        return FoodSensor()

    def create_verification_module(self) -> VerificationModule:
        return AgeVerifier()

    def create_inventory_policy(self) -> InventoryPolicy:
        return StandardInventoryPolicy()
