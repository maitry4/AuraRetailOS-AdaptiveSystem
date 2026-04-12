"""hardware/dispenser.py — <<interface>> ABC for hardware dispensers."""
from abc import ABC, abstractmethod

class Dispenser(ABC):
    @abstractmethod
    def dispense(self, product_id: str) -> bool: ...
    @abstractmethod
    def self_test(self) -> bool: ...
