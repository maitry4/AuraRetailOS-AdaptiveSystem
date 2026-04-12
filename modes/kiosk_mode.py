"""
modes/kiosk_mode.py
PATTERN 4 — State Pattern
Abstract base for all KioskMode states.
KioskCore holds a reference to the current mode and delegates all
request handling to it. Switching mode = swapping this object.
"""
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.kiosk_core import KioskCore

class KioskMode(ABC):
    """<<State Pattern>> Abstract kiosk operating mode."""

    @abstractmethod
    def handle_purchase(self, ctx: "KioskCore", product_id: str, user_id: str) -> bool:
        """Handle a purchase request in this mode."""
        ...

    @abstractmethod
    def handle_refund(self, ctx: "KioskCore", tx_id: str) -> bool:
        """Handle a refund request in this mode."""
        ...

    @abstractmethod
    def handle_restock(self, ctx: "KioskCore", product_id: str, qty: int) -> bool:
        """Handle a restock request in this mode."""
        ...

    @abstractmethod
    def run_diagnostics(self, ctx: "KioskCore") -> dict:
        """Run diagnostics in this mode."""
        ...

    @property
    @abstractmethod
    def mode_name(self) -> str:
        """Human-readable name of this mode."""
        ...

    def __str__(self) -> str:
        return self.mode_name
