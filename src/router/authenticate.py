from datetime import timedelta

from fastapi import APIRouter, status, Depends, HTTPException, Response
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel

from ..config.token import ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token
from ..models.model import Model
from ..models.schemasIn import Token
from pony.orm import db_session
from ..utils.hashPassword import Hash
from ..config.auth import get_current_user, get_current_active_user
from ..models.schemasIn import UserIn

router = APIRouter()


@router.post('/login', response_model=Token, tags=['Authenticate'])
def login(request: OAuth2PasswordRequestForm = Depends()):
    with db_session:
        user = Model.User.get(email=request.username)
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")
        if not Hash.verify_password(user.password, request.password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")

    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/logout")
async def logout(response: Response, current_user: UserIn = Depends(get_current_active_user)):
    # Also tried following two comment lines
    # response.set_cookie(key="access_token", value="", max_age=1)
    # response.delete_cookie("access_token", domain="localhost")
    response.delete_cookie("access_token")
    return response
