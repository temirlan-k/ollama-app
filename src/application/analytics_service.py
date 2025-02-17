from domain.entities.llm_response import AnalyticsEntity
from domain.interfaces.analytics import IAnalyticsRepository
from typing import List

class AnalyticsService:
    def __init__(self, analytics_repo: IAnalyticsRepository):
        self._analytics_repo = analytics_repo

    async def save_llm_response(self, user_id: int, input_text: str, full_response: dict):
        llm_response = AnalyticsEntity(user_id=user_id, input_text=input_text, full_response=full_response)
        return await self._analytics_repo.save_llm_response(llm_response)

    async def get_user_analytics(self, user_id: int) -> List[AnalyticsEntity]:
        return await self._analytics_repo.get_user_analytics(user_id)
