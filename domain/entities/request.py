from dataclasses import dataclass
from domain.entities.chat_element import ChatElement

@dataclass
class Request(ChatElement):
    maker: str       # one of "user", "terminal", "error"
    body: str