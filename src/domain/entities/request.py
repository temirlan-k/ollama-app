from pydantic import BaseModel


class RequestEntity(BaseModel):
    id: int | None = None
    user_id: int
    input_text: str
    response_text: str

    class Config:
        from_attributes = True
