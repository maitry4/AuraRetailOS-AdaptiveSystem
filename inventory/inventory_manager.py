"""
inventory/inventory_manager.py
Manages stock with atomic reserve/commit.
available = total - reserved - faulted  [derived attribute]
"""
import threading
from typing import Dict

class InventoryManager:
    def __init__(self, products: Dict[str, int] = None):
        self._products: Dict[str, int] = products or {}
        self._reserved: Dict[str, int] = {}
        self._faulted: Dict[str, int] = {}
        self._lock = threading.Lock()

    def add_product(self, product_id: str, qty: int) -> None:
        with self._lock:
            self._products[product_id] = self._products.get(product_id, 0) + qty

    def get_available_stock(self, product_id: str) -> int:
        total = self._products.get(product_id, 0)
        reserved = self._reserved.get(product_id, 0)
        faulted = self._faulted.get(product_id, 0)
        return max(0, total - reserved - faulted)

    def reserve(self, product_id: str, qty: int) -> bool:
        with self._lock:
            if self.get_available_stock(product_id) >= qty:
                self._reserved[product_id] = self._reserved.get(product_id, 0) + qty
                return True
            return False

    def commit(self, product_id: str, qty: int) -> None:
        with self._lock:
            self._reserved[product_id] = max(0, self._reserved.get(product_id, 0) - qty)
            self._products[product_id] = max(0, self._products.get(product_id, 0) - qty)

    def release_reservation(self, product_id: str, qty: int) -> None:
        with self._lock:
            self._reserved[product_id] = max(0, self._reserved.get(product_id, 0) - qty)

    def restock(self, product_id: str, qty: int) -> None:
        with self._lock:
            self._products[product_id] = self._products.get(product_id, 0) + qty
        print(f"      [InventoryManager] Restocked {qty}x '{product_id}'. New total: {self._products[product_id]}.")

    def snapshot(self) -> dict:
        with self._lock:
            return {"products": dict(self._products), "reserved": dict(self._reserved), "faulted": dict(self._faulted)}

    def restore(self, state: dict) -> None:
        with self._lock:
            self._products = dict(state.get("products", {}))
            self._reserved = dict(state.get("reserved", {}))
            self._faulted = dict(state.get("faulted", {}))

    def list_stock(self) -> dict:
        with self._lock:
            return {pid: self.get_available_stock(pid) for pid in self._products}
