import threading
import queue

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
                    # { event_type: [ callback, ... ] }
                    cls._instance._subscribers = {}
                    # Queue for demonstration of priority ordering
                    cls._instance._event_queue = queue.PriorityQueue()
        return cls._instance

    @classmethod
    def get_instance(cls):
        return cls()

    def subscribe(self, event_type: str, callback):
        if event_type not in self._subscribers:
            self._subscribers[event_type] = []
        self._subscribers[event_type].append(callback)

    def publish(self, event):
        """
        Enqueues an event based on its priority.
        High Priority (is_high_priority=True) gets Priority 0.
        Standard events get Priority 1.
        """
        event_type = getattr(event, "event_name", type(event).__name__)
        is_priority = getattr(event, "is_high_priority", False)
        
        # Priority 0 is higher than Priority 1 in PriorityQueue
        prio_val = 0 if is_priority else 1
        
        print(f"  [EventBus] Enqueueing {event_type} (Priority: {prio_val})")
        self._event_queue.put((prio_val, event))
        
        # In a real async system, a separate thread would process this.
        # For the demo, we process immediately but show the ordering if multiple are queued.
        self.flush()

    def flush(self):
        """Processes all currently queued events in priority order."""
        while not self._event_queue.empty():
            prio, event = self._event_queue.get()
            event_type = getattr(event, "event_name", type(event).__name__)
            
            prefix = "[!!! HIGH PRIORITY !!!]" if prio == 0 else "[Standard]"
            print(f"  [EventBus] {prefix} Dispatching: {event_type}")
            
            if event_type in self._subscribers:
                for callback in self._subscribers[event_type]:
                    callback(event)
