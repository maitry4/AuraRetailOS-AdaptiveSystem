"""
inventory/inventory_manager.py
Manages stock with atomic reserve/commit.
available = total - reserved - faulted  [derived attribute]
"""
import threading
import json
import os
from typing import Dict

class InventoryManager:
    def __init__(self, products: Dict[str, int] = None, storage_path: str = "data/inventory.json"):
        self._products: Dict[str, int] = products or {}
        self._reserved: Dict[str, int] = {}
        self._faulted: Dict[str, int] = {}
        self._storage_path = storage_path
        self._lock = threading.Lock()
        
        # Phase 4: Bootstrap (Hardik's task)
        if os.path.exists(self._storage_path):
            self.load_from_file()

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
            
            # Phase 3: LowStockEvent trigger (Hardik's task)
            new_stock = self.get_available_stock(product_id)
            if new_stock < 3: # Threshold
                from events.event_bus import EventBus
                from events.low_stock_event import LowStockEvent
                event = LowStockEvent("LOCAL_KIOSK", product_id, new_stock)
                EventBus.get_instance().publish(event)
            
            # Phase 4: Persistence
            self.save_to_file()

    def release_reservation(self, product_id: str, qty: int) -> None:
        with self._lock:
            self._reserved[product_id] = max(0, self._reserved.get(product_id, 0) - qty)

    def restock(self, product_id: str, qty: int) -> None:
        with self._lock:
            self._products[product_id] = self._products.get(product_id, 0) + qty
            # Phase 4: Persistence
            self.save_to_file()
        print(f"      [InventoryManager] Restocked {qty}x '{product_id}'. New total: {self._products[product_id]}.")

    def save_to_file(self) -> None:
        """Saves current stock levels to JSON."""
        os.makedirs(os.path.dirname(self._storage_path), exist_ok=True)
        with open(self._storage_path, "w") as f:
            json.dump(self._products, f, indent=4)

    def load_from_file(self) -> None:
        """Loads stock levels from JSON."""
        try:
            with open(self._storage_path, "r") as f:
                self._products = json.load(f)
            print(f"      [InventoryManager] Loaded stock from {self._storage_path}")
        except Exception as e:
            print(f"      [InventoryManager] Error loading stock: {e}")

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