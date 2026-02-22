from core.interfaces.llm_responder import ILLMResponder
import ollama

class OllamaNemesisResponder(ILLMResponder):
    def ask(self, prompt: str):
        response = ollama.generate(model="BhanuPrakashKona/nemesis", prompt=prompt)
        return response['response']