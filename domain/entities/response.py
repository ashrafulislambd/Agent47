from dataclasses import dataclass
from domain.entities.chat_element import ChatElement

@dataclass
class Response(ChatElement):
    type: str       # one of "terminal", "response" or "exit"
    body: str       # main body of response
    command: str    # command if the type is terminal
