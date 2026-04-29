from failure.failure_handler import FailureHandler

class RecalibrationHandler(FailureHandler):
    """
    <<Concrete Handler 2>>
    Attempts to recalibrate the hardware module (motor/sensor).
    """
    def handle(self, failure_context: dict) -> bool:
        error_code = failure_context.get("error_code", "UNKNOWN")
        
        if "ALIGNMENT" in error_code or "SENSOR_DRIFT" in error_code:
            print(f"  [Recalibration] Alignment error '{error_code}' detected. Triggering recalibration sequence...")
            # Simulate calibration
            print("  [Recalibration] V Hardware recalibrated successfully.")
            return True
            
        print(f"  [Recalibration] Error '{error_code}' is not a calibration issue. Passing to next handler.")
        return super().handle(failure_context)
