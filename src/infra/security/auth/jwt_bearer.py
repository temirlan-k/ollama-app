from fastapi import Depends, Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt

from infra.security.auth.auth_handler import decode_token
from core.configs import config

from fastapi import Depends, Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt

from core.configs import config


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> dict:
        credentials: HTTPAuthorizationCredentials = await super(
            JWTBearer, self
        ).__call__(request)

        if not credentials:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")

        if credentials.scheme != "Bearer":
            raise HTTPException(
                status_code=403, detail="Invalid authentication scheme."
            )

        try:
            token = credentials.credentials.encode("utf-8")
            payload = jwt.decode(
                token, config.secret_key, algorithms=[config.algorithm]
            )
            if not payload:
                raise HTTPException(status_code=403, detail="Invalid token payload.")
            return payload
        except Exception as e:
            raise HTTPException(status_code=403, detail=str(e))
