from fastapi import APIRouter, Depends, HTTPException

from application.request_service import RequestService
from application.user_service import UserService
from core.di_container import DIContainer
from dependency_injector.wiring import Provide, inject

from domain.exceptions.user_exceptions import AuthenticationException
from infra.db.cache.cache_decarator import cache_result
from presentation.schemas.request import RequestDTO
from presentation.schemas.user import UserRequestDTO
from infra.security.auth.jwt_bearer import JWTBearer

request_router = APIRouter()    

@request_router.post("/process")
@cache_result(3600)
@inject
async def get_request(
    req: RequestDTO,
    current_user: dict = Depends(JWTBearer()),
    request_service: RequestService = Depends(Provide[DIContainer.request_service])
):
    try:
        return await request_service.create_request(req, current_user.get('sub'))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@request_router.get('/history')
@cache_result(3600)
@inject
async def get_user_history(
    current_user: dict = Depends(JWTBearer()),
    request_service: RequestService = Depends(Provide[DIContainer.request_service])
):
    try:
        return await request_service.get_user_request_history(current_user.get('sub'))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@request_router.get('/analytics')
@cache_result(3600)
@inject
async def get_analytics(
    current_user: dict = Depends(JWTBearer()),
    request_service: RequestService = Depends(Provide[DIContainer.request_service])
):
    return await request_service.get_all_analytics(current_user.get('sub'))
