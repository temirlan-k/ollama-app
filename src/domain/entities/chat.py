

from typing import Any, Dict
from pydantic import BaseModel


class ChatResponse(BaseModel):
    response: str
    full_response: Dict[str, Any] | None = None
    error: str | None = None