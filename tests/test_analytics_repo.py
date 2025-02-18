import pytest
import pytest_asyncio
from unittest.mock import MagicMock
from domain.entities.llm_response import AnalyticsEntity
from infra.db.mongo_db.models.analytics import Analytics
from infra.db.mongo_db.repositories.analytics import AnalyticsRepository


@pytest_asyncio.fixture
async def mock_analytics_repo():
    repo = AnalyticsRepository()
    
    repo.save_llm_response = MagicMock(return_value=AnalyticsEntity(
        user_id=1,
        input_text="Test input",
        full_response={"response": "Test response"}
    ))
    
    repo.get_user_analytics = MagicMock(return_value=[
        AnalyticsEntity(
            user_id=1,
            input_text="Test input",
            full_response={"response": "Test response"}
        ),
        AnalyticsEntity(
            user_id=1,
            input_text="Another input",
            full_response={"response": "Another response"}
        )
    ])
    
    return repo


@pytest.mark.asyncio
async def test_save_llm_response(mock_analytics_repo):
    llm_response = AnalyticsEntity(
        user_id=1,
        input_text="Test input",
        full_response={"response": "Test response"}
    )
    
    saved_response =  mock_analytics_repo.save_llm_response(llm_response)
    
    assert saved_response.user_id == 1
    assert saved_response.input_text == "Test input"
    assert saved_response.full_response == {"response": "Test response"}


@pytest.mark.asyncio
async def test_get_user_analytics(mock_analytics_repo):
    user_analytics =  mock_analytics_repo.get_user_analytics(1)
    
    assert len(user_analytics) == 2
    
    assert user_analytics[0].user_id == 1
    assert user_analytics[0].input_text == "Test input"
    assert user_analytics[0].full_response == {"response": "Test response"}
    
    assert user_analytics[1].user_id == 1
    assert user_analytics[1].input_text == "Another input"
    assert user_analytics[1].full_response == {"response": "Another response"}
