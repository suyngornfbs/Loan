from datetime import timedelta

from fastapi import APIRouter, status, Depends, HTTPException
from pydantic import BaseModel

from ..config.token import ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token
from ..models.schemas import Login, UserOut
from ..models.model import Model
from pony.orm import db_session
from ..utils.hashPassword import Hash

router = APIRouter()


@router.post('/login', tags=['Authenticate'])
def login(request: Login):
    with db_session:
        user = Model.User.get(email = request.email)
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")
        if not Hash.verify_password(user.password,request.password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")

    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}
