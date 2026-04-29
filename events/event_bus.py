import threading

class EventBus:
    """
    <<Singleton / Subject>>
    Central event dispatch system with Priority Routing support.
    Ensures critical events (Emergency) are processed before standard ones.
    """
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(EventBus, cls).__new__(cls)
                    # { event_type: [ (priority, callback), ... ] }
                    cls._instance._subscribers = {}
        return cls._instance

    @classmethod
    def get_instance(cls):
        return cls()

    def subscribe(self, event_type: str, callback, priority: int = 1):
        """
        priority: 0 = High (Immediate), 1 = Standard, 2 = Low (Deferred)
        """
        if event_type not in self._subscribers:
            self._subscribers[event_type] = []
        
        self._subscribers[event_type].append((priority, callback))
        # Keep subscribers sorted by priority (lowest number first)
        self._subscribers[event_type].sort(key=lambda x: x[0])

    def publish(self, event):
        event_type = getattr(event, "event_name", type(event).__name__)
        is_priority = getattr(event, "is_high_priority", False)
        
        prefix = "[PRIORITY]" if is_priority else "[Standard]"
        print(f"  [EventBus] {prefix} Publishing: {event}")

        if event_type in self._subscribers:
            for priority, callback in self._subscribers[event_type]:
                callback(event)
