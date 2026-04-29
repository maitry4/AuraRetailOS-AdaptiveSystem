"""hardware/hardware_controller.py — aggregates hardware modules; isHealthy() is derived."""
from hardware.dispenser import Dispenser
from hardware.sensor_module import SensorModule
from hardware.verification_module import VerificationModule
from failure.auto_retry_handler import AutoRetryHandler
from failure.recalibration_handler import RecalibrationHandler
from failure.technician_alert_handler import TechnicianAlertHandler

class HardwareController:
    def __init__(self, dispenser: Dispenser, sensor: SensorModule, verification: VerificationModule):
        self._dispenser = dispenser
        self._sensor = sensor
        self._verification = verification

    def get_dispenser(self) -> Dispenser: return self._dispenser
    def get_sensor(self) -> SensorModule: return self._sensor
    def get_verification(self) -> VerificationModule: return self._verification

    # Phase 3: Chain of Responsibility initialization (Khushi Odedara's task)
    def _get_failure_chain(self):
        retry = AutoRetryHandler()
        recal = RecalibrationHandler()
        alert = TechnicianAlertHandler()
        
        retry.set_next(recal).set_next(alert)
        return retry

    def report_failure(self, kiosk_id: str, component: str, error_code: str) -> bool:
        """Initiates the recovery chain."""
        print(f"  [HardwareController] Reporting failure: {component} Error:{error_code}")
        failure_context = {
            "kiosk_id": kiosk_id,
            "component": component,
            "error_code": error_code,
            "retry_count": 0
        }
        return self._get_failure_chain().handle(failure_context)

    def is_healthy(self) -> bool:
        """Derived: dispenser self-test OK AND sensor not blocked."""
        dispenser_ok = self._dispenser.self_test()
        sensor_data = self._sensor.read_status()
        return dispenser_ok and not sensor_data.is_blocked
