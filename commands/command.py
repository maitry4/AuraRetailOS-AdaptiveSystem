from abc import ABC, abstractmethod

class Command(ABC):
    """
    <<Command Interface>>
    Encapsulates a request as an object, allowing for queuing, 
    logging, and undoable operations.
    """

    @abstractmethod
    def execute(self) -> bool:
        """Execute the command logic."""
        pass

    @abstractmethod
    def undo(self) -> bool:
        """Roll back the changes made by this command."""
        pass

    @abstractmethod
    def log(self) -> str:
        """Return a string representation of the command for auditing."""
        pass
