"""inventory/inventory_policy.py — <<interface>> ABC for purchase eligibility."""
from abc import ABC, abstractmethod

class InventoryPolicy(ABC):
    @abstractmethod
    def can_purchase(self, product_id: str, qty: int, ctx: dict) -> bool: ...
    @abstractmethod
    def on_purchase_complete(self, product_id: str, qty: int) -> None: ...
