from dependency_injector import containers, providers

from bootstrap.log import setup_logging
from application.analytics_service import AnalyticsService
from application.request_service import RequestService
from application.user_service import UserService
from infra.db.postgres.db import async_session_factory
from infra.db.postgres.uow import SQLAlchemyUnitOfWork
from infra.llm_provider.ollama import OllamaClient
from infra.db.mongo_db.repositories.analytics import analytics_repo


class DIContainer(containers.DeclarativeContainer):

    wiring_config = containers.WiringConfiguration(packages=["presentation.api.rest.v1"])

    db_session_factory = providers.Object(async_session_factory)
    logger = providers.Singleton(setup_logging)
    uow = providers.Factory(SQLAlchemyUnitOfWork, session_factory=db_session_factory)

    llm = providers.Factory(OllamaClient, logger=logger)
    analytics_service = providers.Factory(
        AnalyticsService, analytics_repo=analytics_repo, logger=logger
    )
    user_service = providers.Factory(UserService, uow=uow, logger=logger)
    request_service = providers.Factory(
        RequestService,
        uow=uow,
        llm=llm,
        analytics_service=analytics_service,
        logger=logger,
    )
