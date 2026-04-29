from abc import ABC, abstractmethod
from decimal import Decimal

class PricingStrategy(ABC):
    """
    <<Strategy Interface>>
    Defines a family of interchangeable pricing algorithms.
    """
    @abstractmethod
    def compute_price(self, product_id: str, base_price: float) -> Decimal:
        """Calculate the final price for a product."""
        pass

    @property
    @abstractmethod
    def strategy_name(self) -> str:
        pass
