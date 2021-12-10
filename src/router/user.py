from fastapi import APIRouter
import uvicorn
from starlette.requests import Request
from pony.orm import db_session, commit, flush
from ..models.model import Model
from ..models.schemas import *
from ..utils.hashPassword import Hash

router = APIRouter()


@router.get('/user', tags=['User'])
async def get_all_user():
    with db_session:
        user = Model.User.select()
        result = [UserOut.from_orm(u) for u in user]
    return result


@router.get('/user/{id}', tags=['User'])
def get_user_by_id(id: int):
    with db_session:
        user = Model.User.select()
        result = [UserOut.from_orm(u) for u in user if u.id == id]
    return result


@router.post('/user', tags=['User'])
def create_user(request: UserOut):
    with db_session:
        password = Hash.get_password_hash(request.password)

        user = Model.User(
            name=request.name,
            email=request.email,
            password=password,
        )
    return UserOut.from_orm(user)


@router.put('/user/{id}', tags=['User'])
def update_user(id: int, body: UserOut, request: Request):
    with db_session:
        password = Hash.get_password_hash(body.password)
        Model.User[id].name = body.name
        Model.User[id].email = body.email
        Model.User[id].password = password

        user = Model.User[id]

        return UserOut.from_orm(user)


@router.delete('/user/{id}', tags=['User'])
def delete_user(id: int):
    with db_session:
        user = Model.User.select(lambda u: u.id == id)
        user.delete()
        return {
            'message': 'Delete successfully'
        }
