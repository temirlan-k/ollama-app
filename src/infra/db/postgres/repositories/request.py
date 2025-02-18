from typing import List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from domain.entities.request import RequestEntity
from infra.db.postgres.models.requests import Request


class RequestRepository:

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, request: RequestEntity) -> RequestEntity:
        request_db = Request(
            user_id=request.user_id,
            input_text=request.input_text,
            response_text=request.response_text,
        )
        self._session.add(request_db)
        await self._session.flush()
        return RequestEntity(
            id=request_db.id,
            user_id=request_db.user_id,
            input_text=request_db.input_text,
            response_text=request_db.response_text,
        )

    async def get_requests_by_user_id(self, user_id: int) -> List[RequestEntity]:
        result = await self._session.execute(
            select(Request).where(Request.user_id == user_id)
        )
        requests_db = result.scalars().all()
        print(requests_db)
        return [
            RequestEntity(
                id=request.id,
                user_id=request.user_id,
                input_text=request.input_text,
                response_text=request.response_text,
            )
            for request in requests_db
        ]
