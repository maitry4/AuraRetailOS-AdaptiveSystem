class EventBus:
    """
    <<Singleton / Subject>>
    Central event dispatch system.
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(EventBus, cls).__new__(cls)
            cls._instance._subscribers = {}
        return cls._instance

    @classmethod
    def get_instance(cls):
        return cls()

    def subscribe(self, event_type: str, callback):
        if event_type not in self._subscribers:
            self._subscribers[event_type] = []
        self._subscribers[event_type].append(callback)

    def publish(self, event):
        event_type = getattr(event, "event_name", type(event).__name__)
        print(f"  [EventBus] Publishing: {event}")
        if event_type in self._subscribers:
            for callback in self._subscribers[event_type]:
                callback(event)
