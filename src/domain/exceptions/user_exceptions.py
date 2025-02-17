from domain.exceptions.base import BaseDomainException

class UserAlreadyExistsException(BaseDomainException):
    def __init__(self, email: str):
        super().__init__(f"User with email {email} already exists.")

class AuthenticationException(BaseDomainException):
    def __init__(self, message: str = "Authentication error"):
        super().__init__(message)