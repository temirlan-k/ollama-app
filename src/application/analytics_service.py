import structlog
from typing import List

from domain.entities.llm_response import AnalyticsEntity
from domain.interfaces.analytics import IAnalyticsRepository


class AnalyticsService:
    def __init__(
        self, analytics_repo: IAnalyticsRepository, logger: structlog.stdlib.BoundLogger
    ):
        self._analytics_repo = analytics_repo
        self._logger = logger

    async def save_llm_response(
        self, user_id: int, input_text: str, full_response: dict
    ):
        self._logger.info(
            "Saving LLM response", extra={"user_id": user_id, "input_text": input_text}
        )
        llm_response = AnalyticsEntity(
            user_id=user_id, input_text=input_text, full_response=full_response
        )
        try:
            result = await self._analytics_repo.save_llm_response(llm_response)
            self._logger.info(
                "LLM response saved",
                extra={"user_id": user_id, "input_text": input_text},
            )
            return result
        except Exception as e:
            self._logger.error(
                "Error saving LLM response",
                extra={"user_id": user_id, "input_text": input_text, "error": str(e)},
            )
            raise e

    async def get_user_analytics(self, user_id: int) -> List[AnalyticsEntity]:
        self._logger.info("Fetching user analytics", extra={"user_id": user_id})
        try:
            analytics = await self._analytics_repo.get_user_analytics(user_id)
            self._logger.info(
                "User analytics fetched",
                extra={"user_id": user_id, "analytics_count": len(analytics)},
            )
            return analytics
        except Exception as e:
            self._logger.error(
                "Error fetching user analytics",
                extra={"user_id": user_id, "error": str(e)},
            )
            raise e
