from fastapi import APIRouter, Depends, HTTPException

from application.user_service import UserService
from domain.exceptions.database_exceptions import DatabaseException
from domain.exceptions.user_exceptions import UserAlreadyExistsException
from core.di_container import DIContainer
from dependency_injector.wiring import Provide, inject

from presentation.schemas.user import UserRequestDTO
from infra.security.auth.jwt_bearer import JWTBearer


user_router = APIRouter()

@user_router.post("/create")
@inject
async def create_user(req: UserRequestDTO, user_service: UserService = Depends(Provide[DIContainer.user_service])):
    try:
        return await user_service.create_user(req)
    except UserAlreadyExistsException as e:
        raise HTTPException(status_code=400, detail=e.message)
    except DatabaseException as e:
        raise HTTPException(status_code=500, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
# @user_router.get("/me")   
# async def get_current_user(
#     user_service: UserService = Depends(Provide[DIContainer.user_service])
# ):
#     try:
#         return await user_service.get_user_by_email(current_user)
#     except DatabaseException as e:
#         raise HTTPException(status_code=500, detail=e.message)
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
    