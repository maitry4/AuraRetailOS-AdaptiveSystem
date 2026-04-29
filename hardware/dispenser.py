from abc import ABC, abstractmethod

class Dispenser(ABC):
    """
    <<Interface>>
    Abstract base for all product dispensers.
    Supports 'Delayed Hardware Response' by separating dispense and confirmation.
    """
    @abstractmethod
    def dispense(self, product_id: str) -> bool:
        """Start the dispense process."""
        pass

    @abstractmethod
    def wait_for_completion(self) -> bool:
        """
        Phase 2: Support for delayed response. 
        Waits for the motor/sensor to confirm product drop.
        """
        pass

    @abstractmethod
    def self_test(self) -> bool:
        """Check hardware health."""
        pass

    @property
    @abstractmethod
    def model_name(self) -> str:
        pass
