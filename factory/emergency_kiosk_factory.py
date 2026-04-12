"""
factory/emergency_kiosk_factory.py
Concrete factory — produces components for emergency relief kiosks.
Applies rationed inventory policy and no-frills dispensing.
"""
from factory.kiosk_factory import KioskFactory
from hardware.dispenser import Dispenser
from hardware.sensor_module import SensorModule, SensorData
from hardware.verification_module import VerificationModule
from inventory.inventory_policy import InventoryPolicy
from inventory.emergency_inventory_policy import EmergencyInventoryPolicy

class BasicDispenser(Dispenser):
    def dispense(self, product_id: str) -> bool:
        print(f"      [BasicDispenser] Releasing essential item '{product_id}'...")
        return True
    def self_test(self) -> bool:
        print("      [BasicDispenser] Self-test: basic dispenser OK.")
        return True

class EmergencySensor(SensorModule):
    def read_status(self) -> SensorData:
        return SensorData(temperature=25.0, humidity=60.0, is_blocked=False)
    def calibrate(self) -> bool:
        print("      [EmergencySensor] Calibrated.")
        return True

class OpenVerifier(VerificationModule):
    """No verification required during emergency — open access."""
    def verify(self, user_id: str, product_id: str) -> bool:
        print(f"      [OpenVerifier] Emergency access granted for {user_id}.")
        return True

class EmergencyKioskFactory(KioskFactory):
    @property
    def factory_name(self) -> str:
        return "EmergencyKioskFactory"

    def create_dispenser(self) -> Dispenser:
        return BasicDispenser()

    def create_sensor(self) -> SensorModule:
        return EmergencySensor()

    def create_verification_module(self) -> VerificationModule:
        return OpenVerifier()

    def create_inventory_policy(self) -> InventoryPolicy:
        return EmergencyInventoryPolicy(max_qty=2)
