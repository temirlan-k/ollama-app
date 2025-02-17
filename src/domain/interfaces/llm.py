from abc import ABC, abstractmethod

from ollama import ChatResponse



class IOllamaClient(ABC):

    @abstractmethod
    def chat(self, message:str) -> dict:
        raise NotImplementedError()
    
