from commands.command import Command
import datetime

class RefundCommand(Command):
    """
    <<Concrete Command>>
    Encapsulates a refund operation.
    """
    def __init__(self, ctx, tx_id: str):
        self.ctx = ctx
        self.tx_id = tx_id
        self.timestamp = datetime.datetime.now()
        self.status = "PENDING"

    def execute(self) -> bool:
        print(f"  [Command] Executing RefundCommand for transaction '{self.tx_id}'")
        # In a real system, we would look up the transaction and restore stock.
        # For this demo, we simulate a successful refund.
        self.status = "COMPLETED"
        print(f"  [Command] Refund processed successfully.")
        return True

    def undo(self) -> bool:
        # Undoing a refund would mean re-charging the customer, which is complex.
        print(f"  [Command] Undo not supported for RefundCommand.")
        return False

    def log(self) -> str:
        return f"{self.timestamp.isoformat()} | REFUND   | TxID:{self.tx_id} | Status:{self.status}"
