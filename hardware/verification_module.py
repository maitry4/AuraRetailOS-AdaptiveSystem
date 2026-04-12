"""hardware/verification_module.py — <<interface>> ABC for user/product verification."""
from abc import ABC, abstractmethod

class VerificationModule(ABC):
    @abstractmethod
    def verify(self, user_id: str, product_id: str) -> bool: ...
