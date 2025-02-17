from dependency_injector import containers, providers
from application.request_service import RequestService
from infra.db.postgres.db import async_session_factory
from infra.db.postgres.uow import SQLAlchemyUnitOfWork
from application.user_service import UserService
from infra.llm_provider.ollama import OllamaClient
from application.analytics_service import AnalyticsService
from infra.db.mongo_db.repositories.analytics import analytics_repo


class DIContainer(containers.DeclarativeContainer):

    wiring_config = containers.WiringConfiguration(packages=["presentation.api.v1"])

    db_session_factory = providers.Object(async_session_factory)

    uow = providers.Factory(SQLAlchemyUnitOfWork, session_factory=db_session_factory)
    llm = providers.Factory(OllamaClient)
    analytics_service = providers.Factory(AnalyticsService,analytics_repo=analytics_repo)

    user_service = providers.Factory(UserService, uow=uow)

    request_service = providers.Factory(RequestService, uow=uow, llm=llm,analytics_service=analytics_service)