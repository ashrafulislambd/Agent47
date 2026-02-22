from core.interfaces.llm_responder import ILLMResponder

class TestResponder:
    def __init__(self, responder: ILLMResponder):
        self.responder = responder

    def test(self):
        response = self.responder.ask("Hello!")
        print(response)