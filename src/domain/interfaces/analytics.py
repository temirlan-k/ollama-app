from typing import List
from abc import ABC, abstractmethod
from domain.entities.llm_response import AnalyticsEntity


class IAnalyticsRepository(ABC):
    @abstractmethod
    async def save_llm_response(self, llm_response: AnalyticsEntity) -> AnalyticsEntity:
        raise NotImplementedError()

    @abstractmethod
    async def get_user_analytics(self, user_id: int) -> List[AnalyticsEntity]:
        raise NotImplementedError()
