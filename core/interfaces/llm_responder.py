from abc import ABC, abstractmethod

class ILLMResponder(ABC):
    @abstractmethod
    def ask(self, prompt: str) -> str:
        """
        Gives response to a prompt using LLM
        """