class EmergencyModeActivated:
    """
    <<High Priority Event>>
    Triggered when a city-wide emergency is declared.
    """
    def __init__(self, region: str = "All"):
        self.region = region
        self.event_name = "EmergencyModeActivated"
        self.is_high_priority = True

    def __str__(self):
        return f"Event[Emergency] Region:{self.region} (CRITICAL)"
