from core.interfaces.terminal import ITerminal

class HelloTerminal():
    def __init__(self, terminal: ITerminal):
        self.terminal = terminal

    def execute(self):
        res = self.terminal.execute("dir")
        print("Result: ")
        print(res.stdout)