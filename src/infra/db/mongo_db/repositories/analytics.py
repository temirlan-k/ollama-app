from typing import List
from domain.entities.llm_response import AnalyticsEntity
from domain.interfaces.analytics import IAnalyticsRepository
from infra.db.mongo_db.models.analytics import Analytics


class AnalyticsRepository(IAnalyticsRepository):

    async def save_llm_response(self, llm_response: AnalyticsEntity) -> AnalyticsEntity:
        analytics_db = Analytics(
            user_id=llm_response.user_id,
            input_text=llm_response.input_text,
            full_response=llm_response.full_response,
        )
        await analytics_db.insert()
        return llm_response

    async def get_user_analytics(self, user_id: int) -> List[AnalyticsEntity]:
        analytics_db = await Analytics.find({"user_id": user_id}).to_list()
        return [
            AnalyticsEntity(
                user_id=res.user_id,
                input_text=res.input_text,
                full_response=res.full_response,
            )
            for res in analytics_db
        ]


analytics_repo = AnalyticsRepository()
