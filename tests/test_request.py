


import pytest
from domain.entities.request import RequestEntity
from infra.db.postgres.repositories.request import RequestRepository
from shared import async_session


@pytest.mark.asyncio
async def test_create_request(async_session):
    repo = RequestRepository(async_session)

    request_entity = RequestEntity(
        user_id=1,
        input_text="What is the weather today?",
        response_text="It is sunny."
    )

    created_request = await repo.create(request_entity)

    assert created_request is not None
    assert created_request.user_id == 1
    assert created_request.input_text == "What is the weather today?"
    assert created_request.response_text == "It is sunny."


@pytest.mark.asyncio
async def test_get_requests_by_user_id(async_session):
    repo = RequestRepository(async_session)

    request_entity1 = RequestEntity(
        user_id=1,
        input_text="What is the weather today?",
        response_text="It is sunny."
    )
    request_entity2 = RequestEntity(
        user_id=1,
        input_text="How are you?",
        response_text="I'm fine, thanks."
    )

    await repo.create(request_entity1)
    await repo.create(request_entity2)

    requests = await repo.get_requests_by_user_id(1)

    assert len(requests) == 2
    assert requests[0].user_id == 1
    assert requests[0].input_text == "What is the weather today?"
    assert requests[0].response_text == "It is sunny."
    assert requests[1].user_id == 1
    assert requests[1].input_text == "How are you?"
    assert requests[1].response_text == "I'm fine, thanks."