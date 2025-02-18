class UserAlreadyExistsException(Exception):
    def __init__(self, email: str):
        super().__init__(f"User with email {email} already exists.")


class AuthenticationException((Exception)):
    def __init__(self, message: str = "Authentication error"):
        super().__init__(message)


class NotFoundException(Exception):
    def __init__(self, email: str):
        super().__init__(f"User with email {email} not found.")


class BadRequestException(Exception):
    def __init__(self, message: str):
        super().__init__(message)
