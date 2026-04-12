"""hardware/sensor_module.py — <<interface>> ABC for sensor hardware."""
from abc import ABC, abstractmethod
from dataclasses import dataclass, field

@dataclass
class SensorData:
    temperature: float = 22.0
    humidity: float = 45.0
    is_blocked: bool = False

class SensorModule(ABC):
    @abstractmethod
    def read_status(self) -> SensorData: ...
    @abstractmethod
    def calibrate(self) -> bool: ...
