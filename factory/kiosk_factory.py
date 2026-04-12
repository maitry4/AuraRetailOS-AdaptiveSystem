"""
factory/kiosk_factory.py
PATTERN 3 — Abstract Factory
Abstract base that defines the factory interface for creating
a family of compatible kiosk components.
"""
from abc import ABC, abstractmethod
from hardware.dispenser import Dispenser
from hardware.verification_module import VerificationModule
from inventory.inventory_policy import InventoryPolicy

class KioskFactory(ABC):
    """<<Abstract Factory>> Creates compatible component families per kiosk type."""

    @abstractmethod
    def create_dispenser(self) -> Dispenser: ...

    @abstractmethod
    def create_verification_module(self) -> VerificationModule: ...

    @abstractmethod
    def create_inventory_policy(self) -> InventoryPolicy: ...

    @property
    @abstractmethod
    def factory_name(self) -> str: ...
