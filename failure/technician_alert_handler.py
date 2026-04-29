from failure.failure_handler import FailureHandler
from events.event_bus import EventBus
from events.hardware_failure_event import HardwareFailureEvent

class TechnicianAlertHandler(FailureHandler):
    """
    <<Concrete Handler 3 - Terminal>>
    Alerts a human technician and publishes a system-wide event if all auto-recovery fails.
    """
    def handle(self, failure_context: dict) -> bool:
        kiosk_id = failure_context.get("kiosk_id", "UNKNOWN")
        component = failure_context.get("component", "UNKNOWN")
        error_code = failure_context.get("error_code", "UNKNOWN")

        print(f"  [TechnicianAlert] !!! CRITICAL FAILURE !!! Kiosk:{kiosk_id} Component:{component} Error:{error_code}")
        print("  [TechnicianAlert] Sending SMS/Email to maintenance team...")
        
        # Phase 4: Publish HardwareFailureEvent (Khushi Odedara's task)
        event = HardwareFailureEvent(kiosk_id, component, error_code)
        EventBus.get_instance().publish(event)
        
        return False # Chain failed to resolve the issue automatically
