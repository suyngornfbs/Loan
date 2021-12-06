from fastapi import APIRouter
from pony.orm import db_session
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
        _hash = Hash()
        password = _hash.get_password_hash(request.password)

        user = Model.User(
            name=request.name,
            email=request.email,
            password=password,
        )
    return [UserOut.from_orm(user)]


@router.put('/user/{id}', tags=['User'])
def update_user(id: int, request: UserOut):
    with db_session:
        Model.User[id].name = request.name
        Model.User[id].email = request.email
        Model.User[id].password = request.password
        user = Model.User.select()
    return [UserOut.from_orm(u) for u in user if u.id == id]


@router.delete('/user/{id}', tags=['User'])
def delete_user(id: int):
    with db_session:
        user = Model.User.select(lambda u: u.id == id)
        user.delete()
        return {
            'message': 'Delete successfully'
        }
