from datetime import datetime, timedelta
from fastapi import HTTPException
import jwt
from core.configs import config

def create_access_token(payload: dict) -> str:
    to_encode = payload.copy()
    expire = datetime.utcnow() + timedelta(minutes=config.access_token_expire_minutes)
    to_encode.update({
        "exp": expire,
        "type": "access",
        "iat": datetime.utcnow()
    })
    return jwt.encode(to_encode, config.secret_key, algorithm=config.algorithm)

def decode_token(token: str) -> dict:
    try:
        payload = jwt.decode(
            token, 
            config.secret_key, 
            algorithms=['HS256'],
        )
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
