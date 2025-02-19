import structlog
from typing import List

from application.analytics_service import AnalyticsService
from domain.entities.llm_response import AnalyticsEntity
from domain.entities.request import RequestEntity
from infra.db.postgres.uow import SQLAlchemyUnitOfWork
from presentation.schemas.request import RequestDTO
from domain.interfaces.llm import IOllamaClient


class RequestService:

    def __init__(
        self,
        uow: SQLAlchemyUnitOfWork,
        llm: IOllamaClient,
        logger: structlog.stdlib.BoundLogger,
    ) -> None:
        self._uow = uow
        self._llm = llm
        self._logger = logger

    async def create_request(self, req: RequestDTO, user_id: int) -> RequestEntity:
        self._logger.info(
            "Creating request",
            extra={"user_id": user_id, "user_message": req.user_message},
        )
        try:
            llm_response = await self._llm.chat(req.user_message)
            response_text = llm_response.get("message").get("content")
            request = RequestEntity(
                user_id=user_id,
                input_text=req.user_message,
                response_text=response_text,
            )
            async with self._uow as uow:
                created_request = await uow.request_repository.create(request)
                await uow.commit()
            await self._analytics_service.save_llm_response(
                user_id, req.user_message, llm_response
            )
            self._logger.info(
                "Request created successfully",
                extra={"user_id": user_id, "request_id": created_request.id},
            )
            return created_request
        except Exception as e:
            self._logger.error(
                "Error creating request", extra={"user_id": user_id, "error": str(e)}
            )
            raise

    async def get_user_request_history(self, user_id: int) -> List[RequestEntity]:
        self._logger.info("Fetching user request history", extra={"user_id": user_id})
        try:
            async with self._uow as uow:
                req_history = await uow.request_repository.get_requests_by_user_id(
                    user_id
                )
            self._logger.info(
                "Successfully fetched user request history",
                extra={"user_id": user_id, "history_count": len(req_history)},
            )
            return req_history
        except Exception as e:
            self._logger.error(
                "Error fetching user request history",
                extra={"user_id": user_id, "error": str(e)},
            )
            raise

