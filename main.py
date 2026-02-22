from core.interactors.hello_terminal import HelloTerminal
from core.interactors.test_responder import TestResponder
from core.interactors.help_user import HelpUser

from external.adapters.cmd_terminal import CmdTerminal
from external.adapters.ollama_llama_responder import OllamaLlamaResponder
from external.adapters.ollama_nemesis_responder import OllamaNemesisResponder

if __name__ == '__main__':
    cmdTerminal = CmdTerminal()
    helloTerminal = HelloTerminal(cmdTerminal)
    helloTerminal.execute()

    ollamaResponder = OllamaNemesisResponder()
    responderTester = TestResponder(ollamaResponder)
    responderTester.test()

    userHelper = HelpUser(cmdTerminal, ollamaResponder)
    userHelper.help()

