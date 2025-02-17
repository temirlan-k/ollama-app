from abc import ABC, abstractmethod


class IOllamaClient(ABC):

    @abstractmethod
    def chat(self, message:str) -> str:
        raise NotImplementedError()
    
