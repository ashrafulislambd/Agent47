from abc import ABC, abstractmethod
from core.dtos.terminal_result import TerminalResultDTO

class ITerminal(ABC):
    @abstractmethod
    def execute(self, prompt: str) -> TerminalResultDTO:
        """
        Executes the prompt in terminal and returns the result
        """