from dataclasses import dataclass

@dataclass
class TerminalResultDTO:
    stdout: str
    stderr: str
    return_code: int