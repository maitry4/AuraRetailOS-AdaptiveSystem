"""
factory/pharmacy_kiosk_factory.py
Concrete factory — produces prescription-grade components for pharmacy kiosks.
"""
from factory.kiosk_factory import KioskFactory
from hardware.dispenser import Dispenser
from hardware.sensor_module import SensorModule, SensorData
from hardware.verification_module import VerificationModule
from inventory.inventory_policy import InventoryPolicy
from inventory.standard_inventory_policy import StandardInventoryPolicy

# ── Concrete products ────────────────────────────────────────────────────────

class SealedPharmaDispenser(Dispenser):
    """Sealed, controlled-substance dispenser with tamper detection."""
    def dispense(self, product_id: str) -> bool:
        print(f"      [SealedPharmaDispenser] Dispensing controlled item '{product_id}'...")
        # Simulating hardware delay (Phase 2)
        return True

    def wait_for_completion(self) -> bool:
        print("      [SealedPharmaDispenser] Waiting for sensor confirmation...")
        return True

    def self_test(self) -> bool:
        print("      [SealedPharmaDispenser] Self-test: OK (seal intact).")
        return True

    @property
    def model_name(self) -> str:
        return "MedSafe-X1"

class PharmaSensor(SensorModule):
    def read_status(self) -> SensorData:
        return SensorData(temperature=18.0, humidity=40.0, is_blocked=False)
    def calibrate(self) -> bool:
        print("      [PharmaSensor] Calibrated.")
        return True

class PrescriptionVerifier(VerificationModule):
    """Checks that the user has a valid prescription for the product."""
    VALID_PRESCRIPTIONS = {("user_alice", "amoxicillin"), ("user_bob", "ibuprofen")}
    def verify(self, user_id: str, product_id: str) -> bool:
        ok = (user_id, product_id) in self.VALID_PRESCRIPTIONS
        status = "valid" if ok else "NOT found"
        print(f"      [PrescriptionVerifier] Prescription for {user_id}/{product_id}: {status}.")
        return ok

# ── Factory ──────────────────────────────────────────────────────────────────

class PharmacyKioskFactory(KioskFactory):
    @property
    def factory_name(self) -> str:
        return "PharmacyKioskFactory"

    def create_dispenser(self) -> Dispenser:
        return SealedPharmaDispenser()

    def create_sensor(self) -> SensorModule:
        return PharmaSensor()

    def create_verification_module(self) -> VerificationModule:
        return PrescriptionVerifier()

    def create_inventory_policy(self) -> InventoryPolicy:
        return StandardInventoryPolicy()
