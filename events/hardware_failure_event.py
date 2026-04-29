class HardwareFailureEvent:
    """
    <<Event>>
    Triggered when a hardware module fails after multiple recovery attempts.
    """
    def __init__(self, kiosk_id: str, component: str, error_code: str):
        self.kiosk_id = kiosk_id
        self.component = component
        self.error_code = error_code
        self.event_name = "HardwareFailureEvent"

    def __str__(self):
        return f"Event[HW_Failure] Kiosk:{self.kiosk_id} Component:{self.component} Error:{self.error_code}"
