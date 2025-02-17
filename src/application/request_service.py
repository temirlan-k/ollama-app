

from typing import List
from application.analytics_service import AnalyticsService
from domain.entities.llm_response import AnalyticsEntity
from domain.entities.request import RequestEntity
from infra.db.postgres.uow import SQLAlchemyUnitOfWork
from presentation.schemas.request import RequestDTO
from domain.interfaces.llm import IOllamaClient


class RequestService:

    def __init__(self,uow: SQLAlchemyUnitOfWork,llm: IOllamaClient,analytics_service:AnalyticsService) -> None:
        self._uow = uow
        self._llm = llm
        self._analytics_service = analytics_service

    async def create_request(self, req: RequestDTO, user_id:int) -> RequestEntity:
        llm_response = await self._llm.chat(req.user_message)
        response_text = llm_response.get('message').get('content')
        request = RequestEntity(user_id=user_id, input_text=req.user_message, response_text=response_text)
        async with self._uow as uow:
            try:
                created_request = await uow.request_repository.create(request)
                await uow.commit()
            except Exception as e:
                await uow.rollback()
                raise e
        await self._analytics_service.save_llm_response(user_id, req.user_message,llm_response)
        return created_request

        
    async def get_user_request_history(self, user_id:int)-> List[RequestEntity]:
        async with self._uow as uow:
            try:
                req_history = await uow.request_repository.get_requests_by_user_id(user_id)
                return req_history
            except Exception as e:
                await uow.rollback()
                raise e
        
    
    async def get_all_analytics(self,user_id:int)->List[AnalyticsEntity]:
        try:
            res = await self._analytics_service.get_user_analytics(user_id)
            print(res)
            return res
        except Exception:
            raise 
