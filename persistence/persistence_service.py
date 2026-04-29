import os

class PersistenceService:
    """
    <<Service>>
    Handles writing transaction logs to CSV and updating inventory data.
    """
    def __init__(self, log_path: str = "data/transactions.csv"):
        self.log_path = log_path
        # Ensure data directory exists
        os.makedirs(os.path.dirname(self.log_path), exist_ok=True)
        # Create file with header if not exists
        if not os.path.exists(self.log_path):
            with open(self.log_path, "w") as f:
                f.write("Timestamp,Type,Product,User,Price,Status\n")

    def log_transaction(self, log_entry: str):
        """Append a log entry to the transactions file."""
        # Replace the pipe format from Command.log() with CSV format
        csv_entry = log_entry.replace(" | ", ",").replace("User:", "").replace("Price:$", "").replace("Status:", "")
        with open(self.log_path, "a") as f:
            f.write(csv_entry + "\n")
        print(f"  [Persistence] Logged to {self.log_path}")
