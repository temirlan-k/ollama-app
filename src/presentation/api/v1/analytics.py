from fastapi import APIRouter
from fastapi import APIRouter, Depends, HTTPException

from application.analytics_service import AnalyticsService
from bootstrap.di_container import DIContainer
from dependency_injector.wiring import Provide, inject

from infra.db.cache.cache_decorator import cache_result
from infra.security.auth.jwt_bearer import JWTBearer

analytics_router = APIRouter(prefix='/analytics',tags=['Analytics'])


@analytics_router.get(
    "/all",
    summary="Получить аналитику по запросам",
    description="Возвращает аналитические данные о запросах пользователей и ответов LLM.",
    responses={
        200: {"description": "Аналитика успешно получена."},
        401: {"description": "Ошибка аутентификации."},
        500: {"description": "Ошибка сервера."},
    },
)
@cache_result(3600)
@inject
async def get_analytics(
    analytics_service: AnalyticsService = Depends(Provide[DIContainer.analytics_service]),
):
    """
    **Получить аналитику по запросам**

    - **analytics_service**: Сервис работы с аналитикой

    **Возвращает**:
    - Данные об аналитике запросов пользователей
    """
    try:
        return await analytics_service.get_all_analytics()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

