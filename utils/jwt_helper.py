from typing import Optional
from datetime import datetime, timedelta
import jwt
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
import logging
from config import settings


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

class JwtHelper:
    def __init__(self):
        self._secret_key = settings.SECRET_KEY
        self._algorithm = settings.ALGORITHM
        self._access_token_expire_minutes = settings.ACCESS_TOKEN_EXPIRE_MINUTES
        self._refresh_token_expire_minutes = settings.REFRESH_TOKEN_EXPIRE_MINUTES

    def create_access_token(self, data: dict,type:int) -> bytes:
        if type == 1:
            expire = datetime.utcnow() + timedelta(minutes=self._access_token_expire_minutes)
        else:
            expire = datetime.utcnow() + timedelta(minutes=self._refresh_token_expire_minutes)
        to_encode = data.copy()
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self._secret_key, algorithm=self._algorithm)
        return encoded_jwt

    async def get_current_user(self, token: str = Depends(OAuth2PasswordBearer(tokenUrl="/login"))) -> Optional[dict]:
        try:
            payload = jwt.decode(token, self._secret_key, algorithms=[self._algorithm])
            _id:int = payload.get("id")
            if _id is None:
                raise HTTPException(status_code=401, detail="Invalid authentication credentials")
        except jwt.exceptions.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token has expired")
        except jwt.exceptions.JWTError:
            raise HTTPException(status_code=401, detail="Invalid token")
        return {"id":_id}
    