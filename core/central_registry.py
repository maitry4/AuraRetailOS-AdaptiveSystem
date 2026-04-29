"""
core/central_registry.py
PATTERN 2 — Singleton
CentralRegistry: one source of truth for system config, kiosk registration,
and system-wide status. Thread-safe singleton via class-level lock.
"""
import threading
from dataclasses import dataclass, field
from typing import Dict, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from core.kiosk_core import KioskCore

@dataclass
class SystemConfig:
    system_name: str = "Aura Retail OS"
    version: str = "1.0.0"
    max_kiosks: int = 50
    default_currency: str = "INR"

@dataclass
class SystemStatus:
    online_kiosks: int = 0
    emergency_active: bool = False
    total_transactions: int = 0
    alerts: list = field(default_factory=list)

class CentralRegistry:
    """
    <<Singleton>> Global registry for kiosk instances, config, and system status.
    getInstance() always returns the same object — guaranteed by double-checked locking.
    """
    _instance: Optional["CentralRegistry"] = None
    _lock: threading.Lock = threading.Lock()

    def __new__(cls) -> "CentralRegistry":
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    instance = super().__new__(cls)
                    instance._config = SystemConfig()
                    instance._status = SystemStatus()
                    instance._kiosks: Dict[str, "KioskCore"] = {}
                    cls._instance = instance
        return cls._instance

    @classmethod
    def get_instance(cls) -> "CentralRegistry":
        return cls()

    # -- Config ---------------------------------------------------------------

    def get_config(self) -> SystemConfig:
        return self._config

    def update_config(self, **kwargs) -> None:
        for key, value in kwargs.items():
            if hasattr(self._config, key):
                setattr(self._config, key, value)

    # -- Kiosk Registration ---------------------------------------------------

    def register_kiosk(self, kiosk: "KioskCore") -> None:
        with self._lock:
            self._kiosks[kiosk.kiosk_id] = kiosk
            self._status.online_kiosks = len(self._kiosks)
        print(f"  [CentralRegistry] Kiosk '{kiosk.kiosk_id}' registered. Total online: {self._status.online_kiosks}.")

    def get_kiosk(self, kiosk_id: str) -> Optional["KioskCore"]:
        return self._kiosks.get(kiosk_id)

    def list_kiosks(self) -> Dict[str, str]:
        return {kid: k.operational_status for kid, k in self._kiosks.items()}

    # -- Status ---------------------------------------------------------------

    def update_status(self, kiosk_id: str, status: str) -> None:
        print(f"  [CentralRegistry] Status update — kiosk '{kiosk_id}': {status}.")

    def get_status(self) -> SystemStatus:
        return self._status

    def activate_emergency(self) -> None:
        self._status.emergency_active = True
        self.add_alert("SYSTEM", "Emergency Mode Activated system-wide.")
        print("  [CentralRegistry] !  EMERGENCY MODE ACTIVATED system-wide.")

    def add_alert(self, source: str, message: str) -> None:
        with self._lock:
            self._status.alerts.append(f"[{source}] {message}")
            if len(self._status.alerts) > 10:
                self._status.alerts.pop(0)

    def get_alerts(self) -> list:
        return self._status.alerts

    def increment_transactions(self) -> None:
        with self._lock:
            self._status.total_transactions += 1

    def summary(self) -> str:
        cfg = self._config
        st = self._status
        alert_summary = f"Recent Alerts: {len(st.alerts)}"
        return (
            f"\n{'='*55}\n"
            f"  {cfg.system_name} v{cfg.version}\n"
            f"  Online kiosks    : {st.online_kiosks}\n"
            f"  Total tx         : {st.total_transactions}\n"
            f"  Emergency active : {st.emergency_active}\n"
            f"  {alert_summary}\n"
            f"{'='*55}"
        )
