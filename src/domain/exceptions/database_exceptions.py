

from domain.exceptions.base import BaseDomainException
from sqlalchemy.exc import SQLAlchemyError


class DatabaseException(BaseDomainException):
    def __init__(self, message: str = "Database error"):
        super().__init__(self.message)