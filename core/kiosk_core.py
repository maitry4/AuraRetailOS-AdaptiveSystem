"""
core/kiosk_core.py
Central context object for a single kiosk unit.
Holds the current KioskMode (State pattern), delegates all behaviour to it.
operationalStatus is a derived attribute: mode name + hardware health.
"""
from hardware.hardware_controller import HardwareController
from inventory.inventory_manager import InventoryManager
from inventory.inventory_policy import InventoryPolicy
from modes.kiosk_mode import KioskMode
from pricing.pricing_strategy import PricingStrategy
from pricing.standard_pricing import StandardPricing
from commands.command import Command
from persistence.persistence_service import PersistenceService
from events.event_bus import EventBus
from events.transaction_completed import TransactionCompletedEvent
from typing import List

class KioskCore:
    """
    Context class for the State pattern.
    - currentMode: KioskMode  [State]
    - operationalStatus: str  [derived from currentMode + hardware health]
    - commandHistory: list     [Command pattern — wired in later patterns]
    """

    def __init__(
        self,
        kiosk_id: str,
        hardware_controller: HardwareController,
        inventory_manager: InventoryManager,
        inventory_policy: InventoryPolicy,
        initial_mode: KioskMode,
    ):
        self.kiosk_id = kiosk_id
        self.hardware_controller = hardware_controller
        self.inventory_manager = inventory_manager
        self.inventory_policy = inventory_policy
        self._current_mode: KioskMode = initial_mode
        self._command_history: List[Command] = []
        self._pricing_strategy: PricingStrategy = StandardPricing() # Default
        self._persistence = PersistenceService()
        self._event_bus = EventBus.get_instance()

    # -- State Pattern: mode access & switching -------------------------------

    @property
    def current_mode(self) -> KioskMode:
        return self._current_mode

    def switch_mode(self, new_mode: KioskMode) -> None:
        old = self._current_mode.mode_name
        self._current_mode = new_mode
        print(f"  [KioskCore '{self.kiosk_id}'] Mode switch: {old} -> {new_mode.mode_name}")

    # -- Strategy Pattern: pricing --------------------------------------------

    @property
    def pricing_strategy(self) -> PricingStrategy:
        return self._pricing_strategy

    def set_pricing_strategy(self, strategy: PricingStrategy) -> None:
        print(f"  [KioskCore '{self.kiosk_id}'] Pricing Strategy switch: {self._pricing_strategy.strategy_name} -> {strategy.strategy_name}")
        self._pricing_strategy = strategy

    # -- Command Pattern: execution & history ----------------------------------

    def execute_command(self, command: Command) -> bool:
        """Executes a command, records history, logs to file, and publishes events."""
        success = command.execute()
        self._command_history.append(command)
        
        # Log to file (Maitry's Persistence requirement)
        self._persistence.log_transaction(command.log())

        # Publish event on success (Maitry's Event requirement)
        if success and command.__class__.__name__ == "PurchaseItemCommand":
            from commands.purchase_item_command import PurchaseItemCommand
            cmd: PurchaseItemCommand = command
            event = TransactionCompletedEvent(self.kiosk_id, cmd.product_id, cmd.final_price)
            self._event_bus.publish(event)

        return success

    def get_history_logs(self) -> List[str]:
        return [cmd.log() for cmd in self._command_history]

    # -- Derived attribute ----------------------------------------------------

    @property
    def operational_status(self) -> str:
        """Derived: mode name + hardware health indicator."""
        hw_ok = self.hardware_controller.is_healthy()
        hw_label = "HW:OK" if hw_ok else "HW:FAULT"
        return f"{self._current_mode.mode_name} | {hw_label}"

    # -- Request delegation to current mode ----------------------------------

    def handle_request(self, request: dict) -> bool:
        """
        Generic entry point. Delegates to the current mode.
        request keys: action, product_id, user_id, tx_id, qty
        """
        action = request.get("action", "")
        if action == "purchase":
            return self._current_mode.handle_purchase(self, request["product_id"], request["user_id"])
        elif action == "refund":
            return self._current_mode.handle_refund(self, request["tx_id"])
        elif action == "restock":
            return self._current_mode.handle_restock(self, request["product_id"], request["qty"])
        elif action == "diagnostics":
            result = self._current_mode.run_diagnostics(self)
            print(f"  [KioskCore] Diagnostics: {result}")
            return True
        else:
            print(f"  [KioskCore] Unknown action '{action}'.")
            return False

    def get_available_stock(self, product_id: str) -> int:
        """Derived — proxies InventoryManager."""
        return self.inventory_manager.get_available_stock(product_id)
