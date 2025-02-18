import ollama
import structlog
from domain.interfaces.llm import IOllamaClient
from typing import Dict, Any


class OllamaClient(IOllamaClient):
    def __init__(
        self,
        logger: structlog.stdlib.BoundLogger,
        model: str = "tinyllama",
        host: str = "http://ollama:11434",
    ):
        self.model = model
        self.host = host
        self._logger = logger

    async def chat(self, message: str) -> Dict[str, Any]:
        self._logger.info(
            "Sending chat request to Ollama",
            extra={"model": self.model, "message": message},
        )
        try:
            response = await ollama.AsyncClient(host=self.host).chat(
                model=self.model,
                messages=[
                    {
                        "role": "user",
                        "content": message,
                    }
                ],
            )
            self._logger.info(
                f"Received response from Ollama",
                extra={"model": self.model, "response": response},
            )
            return response.model_dump()
        except Exception as e:
            self._logger.error(
                f"Error while chatting with Ollama",
                extra={"model": self.model, "error": str(e)},
            )
            raise
