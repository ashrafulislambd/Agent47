from core.interfaces.llm_responder import ILLMResponder
import ollama

class OllamaLlamaResponder(ILLMResponder):
    def ask(self, prompt: str):
        response = ollama.generate(model="llama3:8b", prompt=prompt)
        return response['response']