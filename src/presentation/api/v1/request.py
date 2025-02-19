from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from typing import List

from application.request_service import RequestService
from bootstrap.di_container import DIContainer
from dependency_injector.wiring import Provide, inject

from infra.db.cache.cache_decorator import cache_result
from infra.prometheus.decorators import track_llm_duration
from presentation.schemas.request import RequestDTO
from infra.security.auth.jwt_bearer import JWTBearer

request_router = APIRouter(
    prefix="/requests",
    tags=["Requests"],
)


@request_router.post(
    "/process",
    summary="Создать запрос",
    description="Создает новый запрос и возвращает результат обработки.",
    responses={
        200: {"description": "Запрос успешно обработан."},
        401: {"description": "Ошибка аутентификации."},
        500: {"description": "Ошибка сервера."},
    },
)
@cache_result(3600)
@track_llm_duration
@inject
async def create_request(
    req: RequestDTO,
    current_user: dict = Depends(JWTBearer()),
    request_service: RequestService = Depends(Provide[DIContainer.request_service]),
):
    """
    **Создать новый запрос**

    - **req**: Данные запроса (RequestDTO)
    - **current_user**: Текущий аутентифицированный пользователь (из JWT)
    - **request_service**: Сервис для работы с запросами

    **Возвращает**:
    - Результат обработки запроса
    """
    try:
        return await request_service.create_request(req, current_user.get("sub"))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@request_router.get(
    "/history",
    summary="Получить историю запросов пользователя",
    description="Возвращает список всех запросов, сделанных пользователем.",
    responses={
        200: {"description": "История запросов успешно получена."},
        401: {"description": "Ошибка аутентификации."},
        500: {"description": "Ошибка сервера."},
    },
)
@cache_result(3600)
@inject
async def get_user_history(
    current_user: dict = Depends(JWTBearer()),
    request_service: RequestService = Depends(Provide[DIContainer.request_service]),
):
    """
    **Получить историю запросов пользователя**

    - **current_user**: Текущий пользователь (из JWT)
    - **request_service**: Сервис работы с запросами

    **Возвращает**:
    - Список всех запросов пользователя
    """
    try:
        return await request_service.get_user_request_history(current_user.get("sub"))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

