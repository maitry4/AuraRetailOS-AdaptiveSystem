from commands.command import Command
import datetime

class RestockCommand(Command):
    """
    <<Concrete Command>>
    Encapsulates an inventory restocking operation.
    """
    def __init__(self, ctx, product_id: str, qty: int):
        self.ctx = ctx
        self.product_id = product_id
        self.qty = qty
        self.timestamp = datetime.datetime.now()
        self.status = "PENDING"

    def execute(self) -> bool:
        print(f"  [Command] Executing RestockCommand: '{self.product_id}' +{self.qty}")
        self.ctx.inventory_manager.restock(self.product_id, self.qty)
        self.status = "COMPLETED"
        return True

    def undo(self) -> bool:
        print(f"  [Command] Undoing Restock: removing {self.qty} from '{self.product_id}'")
        # Simplified: just subtract the qty added.
        self.ctx.inventory_manager.reserve(self.product_id, self.qty)
        self.ctx.inventory_manager.commit(self.product_id, self.qty)
        return True

    def log(self) -> str:
        return f"{self.timestamp.isoformat()} | RESTOCK  | {self.product_id} | Qty:{self.qty} | Status:{self.status}"
