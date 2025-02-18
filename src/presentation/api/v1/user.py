from fastapi import APIRouter, Depends, HTTPException

from application.user_service import UserService
from domain.exceptions.user_exceptions import (
    UserAlreadyExistsException,
    BadRequestException,
    NotFoundException,
)
from bootstrap.di_container import DIContainer
from dependency_injector.wiring import Provide, inject

from presentation.schemas.user import UserRequestDTO

user_router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@user_router.post(
    "/create",
    summary="Создать нового пользователя",
    description="Регистрирует нового пользователя в системе.",
    responses={
        201: {"description": "Пользователь успешно создан."},
        400: {"description": "Пользователь уже существует."},
        500: {"description": "Ошибка сервера."},
    },
)
@inject
async def create_user(
    req: UserRequestDTO,
    user_service: UserService = Depends(Provide[DIContainer.user_service]),
):
    """
    **Создать нового пользователя**

    - **req**: Данные пользователя для регистрации (UserRequestDTO)
    - **user_service**: Сервис управления пользователями

    **Возвращает**:
    - Данные созданного пользователя в виде JWT токена
    """
    try:
        return await user_service.create_user(req)
    except UserAlreadyExistsException as e:
        raise HTTPException(status_code=400, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@user_router.post(
    "/login",
    summary="Войти в систему",
    description="Авторизует пользователя и возвращает токен.",
    responses={
        200: {"description": "Успешный вход в систему."},
        400: {"description": "Неверные учетные данные."},
        404: {"description": "Пользователь не найден."},
        500: {"description": "Ошибка сервера."},
    },
)
@inject
async def login(
    req: UserRequestDTO,
    user_service: UserService = Depends(Provide[DIContainer.user_service]),
):
    """
    **Войти в систему**

    - **req**: Данные пользователя (логин и пароль)
    - **user_service**: Сервис аутентификации пользователей

    **Возвращает**:
    - Токен авторизации
    """
    try:
        return await user_service.login(req)
    except BadRequestException as e:
        raise HTTPException(status_code=400, detail=e.message)
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
