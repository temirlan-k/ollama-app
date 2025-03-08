import strawberry

@strawberry.type
class User:
    email: str
    password: str

@strawberry.type
class Token:
    access_token: str
