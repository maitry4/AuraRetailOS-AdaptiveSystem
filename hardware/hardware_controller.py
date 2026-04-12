"""hardware/hardware_controller.py — aggregates hardware modules; isHealthy() is derived."""
from hardware.dispenser import Dispenser
from hardware.sensor_module import SensorModule
from hardware.verification_module import VerificationModule

class HardwareController:
    def __init__(self, dispenser: Dispenser, sensor: SensorModule, verification: VerificationModule):
        self._dispenser = dispenser
        self._sensor = sensor
        self._verification = verification

    def get_dispenser(self) -> Dispenser: return self._dispenser
    def get_sensor(self) -> SensorModule: return self._sensor
    def get_verification(self) -> VerificationModule: return self._verification

    def is_healthy(self) -> bool:
        """Derived: dispenser self-test OK AND sensor not blocked."""
        dispenser_ok = self._dispenser.self_test()
        sensor_data = self._sensor.read_status()
        return dispenser_ok and not sensor_data.is_blocked
