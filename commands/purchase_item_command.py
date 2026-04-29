from commands.command import Command
from memento.state_snapshot import StateSnapshot
import datetime

class PurchaseItemCommand(Command):
    """
    <<Concrete Command>>
    Encapsulates a purchase transaction. 
    Uses Memento for rollback if hardware fails.
    """
    def __init__(self, ctx, product_id: str, user_id: str, pricing_strategy):
        self.ctx = ctx
        self.product_id = product_id
        self.user_id = user_id
        self.pricing_strategy = pricing_strategy
        self.timestamp = datetime.datetime.now()
        self.status = "PENDING"
        self.final_price = 0
        self._snapshot = None

    def execute(self) -> bool:
        print(f"  [Command] Executing PurchaseItemCommand for '{self.product_id}'")
        
        # 1. Hardware Health Check
        if not self.ctx.hardware_controller.is_healthy():
            print("  [Command] Hardware failure detected before start.")
            self.status = "FAILED: HW_UNHEALTHY"
            return False

        # 2. User Verification
        if not self.ctx.hardware_controller.get_verification().verify(self.user_id, self.product_id):
            print("  [Command] User verification failed.")
            self.status = "FAILED: VERIFICATION"
            return False

        # 3. Calculate Price via Strategy
        # Assume base price lookup (mocked)
        base_price = 10.0 
        self.final_price = self.pricing_strategy.compute_price(self.product_id, base_price)
        print(f"  [Command] Calculated price: ${self.final_price} (Strategy: {self.pricing_strategy.strategy_name})")

        # 4. Inventory Policy Check
        available = self.ctx.inventory_manager.get_available_stock(self.product_id)
        policy_ctx = {"available_stock": available, "price": self.final_price}
        if not self.ctx.inventory_policy.can_purchase(self.product_id, 1, policy_ctx):
            print("  [Command] Purchase denied by inventory policy.")
            self.status = "FAILED: POLICY_DENIED"
            return False

        # 5. Save Memento (Snapshot) before risky operation
        self._snapshot = StateSnapshot(self.product_id, available, 1)
        
        # 6. Reserve stock
        if not self.ctx.inventory_manager.reserve(self.product_id, 1):
            self.status = "FAILED: RESERVATION"
            return False

        # 7. Hardware Dispense (Risky Operation)
        print(f"  [Command] Memento saved: {self._snapshot}. Attempting dispense...")
        dispensed = self.ctx.hardware_controller.get_dispenser().dispense(self.product_id)
        
        if not dispensed:
            # Phase 3: Initiate recovery chain (Khushi Odedara's task)
            print(f"  [Command] Initial dispense failed. Initiating recovery chain...")
            # Simulate a specific error code for the demo
            error_code = "TRANSIENT_MOTOR_STALL" 
            resolved = self.ctx.hardware_controller.report_failure(
                self.ctx.kiosk_id, "Dispenser", error_code
            )
            if resolved:
                print(f"  [Command] Recovery chain resolved the issue. Proceeding to commit.")
                dispensed = True
            else:
                print(f"  [Command] Recovery chain failed to resolve the issue.")

        if dispensed:
            # 8. Success: Commit changes
            self.ctx.inventory_manager.commit(self.product_id, 1)
            self.status = "COMPLETED"
            print(f"  [Command] Purchase completed successfully.")
            return True
        else:
            # 9. Failure: Rollback using Memento
            print(f"  [Command] Hardware failure could not be recovered. Rolling back...")
            self.undo()
            self.status = "FAILED: HARDWARE_ERROR"
            return False

    def undo(self) -> bool:
        if self._snapshot:
            print(f"  [Memento] RESTORING STATE from: {self._snapshot}")
            # Logic: We are releasing the reservation that failed to dispense
            self.ctx.inventory_manager.release_reservation(self.product_id, self._snapshot.reservation_qty)
            print(f"  [Memento] Rollback complete. Stock is back to available: {self.ctx.inventory_manager.get_available_stock(self.product_id)}")
            return True
        return False

    def log(self) -> str:
        return f"{self.timestamp.isoformat()} | PURCHASE | {self.product_id} | User:{self.user_id} | Price:${self.final_price} | Status:{self.status}"
