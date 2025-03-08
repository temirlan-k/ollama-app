from fastapi import HTTPException
import strawberry

from presentation.api.graphql.schemas import User

@strawberry.type
class Query:

    @strawberry.field
    def user(self, id: int)-> User:
        users = {
            1 : {"id":1,"email":"user1@example.com","password":"pass11"},
            2 : {"id":2,"email":"user2@example.com","password":"pass22"}
        }
        user_data = users.get(id)
        if not user_data:
            raise HTTPException(status_code=404,detail='User not found')
        return User(**user_data)
    
