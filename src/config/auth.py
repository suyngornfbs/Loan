from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from ..models.schemasIn import UserIn
from . import token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


async def get_current_user(_token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    return token.verify_token(_token, credentials_exception)


async def get_current_active_user(current_user: UserIn = Depends(get_current_user)):
    return current_user



