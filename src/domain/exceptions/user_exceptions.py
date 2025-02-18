class BaseException(Exception):
    def __init__(self, message: str):
        self.message = message  
        super().__init__(message)



class UserAlreadyExistsException(BaseException):
    def __init__(self, email: str):
        super().__init__(f"User with email {email} already exists.")


class AuthenticationException(BaseException):
    def __init__(self, message: str = "Authentication error"):
        super().__init__(message)


class NotFoundException(BaseException):
    def __init__(self, email: str):
        super().__init__(f"User with email {email} not found.")


class BadRequestException(BaseException):
    def __init__(self, message: str):
        super().__init__(message)
