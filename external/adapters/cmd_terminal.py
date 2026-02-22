from core.interfaces.terminal import ITerminal
from core.dtos.terminal_result import TerminalResultDTO

import subprocess

class CmdTerminal(ITerminal):
    def execute(self, prompt: str):
        result = subprocess.run(f"cmd /c {prompt}",
            text=True,
            capture_output=True,
        )
        return TerminalResultDTO(result.stdout, result.stderr, result.returncode)