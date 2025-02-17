from pydantic import BaseModel


class RequestDTO(BaseModel):
    user_message:str