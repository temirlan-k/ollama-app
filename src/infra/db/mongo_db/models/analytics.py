from typing import Any, Dict
from beanie import Document

class Analytics(Document):
    user_id: int
    input_text: str
    full_response: Dict[str, Any]

    class Config:
        from_attributes = True