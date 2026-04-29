from abc import ABC, abstractmethod
from typing import Optional

class FailureHandler(ABC):
    """
    <<Chain of Responsibility - Base>>
    Abstract handler for hardware or transaction failures.
    Each handler attempts to resolve the issue or passes it to the next handler in the chain.
    """
    def __init__(self):
        self.next_handler: Optional[FailureHandler] = None

    def set_next(self, handler: 'FailureHandler') -> 'FailureHandler':
        self.next_handler = handler
        return handler

    @abstractmethod
    def handle(self, failure_context: dict) -> bool:
        """
        Processes the failure.
        failure_context keys: error_code, component, kiosk_id, retry_count
        Returns True if resolved, False if chain failed.
        """
        if self.next_handler:
            return self.next_handler.handle(failure_context)
        return False
