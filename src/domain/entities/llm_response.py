from typing import Any
from pydantic import BaseModel


class AnalyticsEntity(BaseModel):
    id: str | None = None
    user_id: int
    input_text: str
    full_response: Any
