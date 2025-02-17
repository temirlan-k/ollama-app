import ollama
from domain.interfaces.llm import IOllamaClient
from domain.entities.chat import ChatResponse



class OllamaClient(IOllamaClient):
    def __init__(self, model: str = "tinyllama"):
        self.model = model

    async def chat(self, message: str) -> dict:
        response = await ollama.AsyncClient(host='http://ollama:11434').chat(
            model=self.model,
            messages=[{
                "role": 'user',
                "content": message,
            }],
        )
        return response.model_dump()