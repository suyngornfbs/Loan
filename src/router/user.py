from fastapi import APIRouter, Depends

from pony.orm import db_session, commit, flush
from ..models.model import Model
from ..models.schemasIn import UserIn
from ..models.schemasOut import UserOut
from ..utils.hashPassword import Hash
from ..utils import helper
from ..config.auth import get_current_user, get_current_active_user

router = APIRouter()


@router.get("/users/me", response_model=UserOut, tags=['User'])
async def read_users_me(current_user: UserIn = Depends(get_current_active_user)):
    return current_user


@router.get('/user', tags=['User'])
async def get_all_user():
    with db_session:
        user = Model.User.select()
        result = [UserIn.from_orm(u) for u in user]
    return result


@router.get('/user/{id}', tags=['User'])
def get_user_by_id(id: int, current_user: UserIn = Depends(get_current_user)):
    with db_session:
        user = Model.User.select()
        result = [UserIn.from_orm(u) for u in user if u.id == id]
    return result


@router.post('/register', tags=['Authenticate'])
def register(request: UserIn):
    with db_session:
        if not helper.isEmail(request.email):
            return {
                'message': "email request '@gamil.com'"
            }
        password = Hash.get_password_hash(request.password)
        email = Model.User.get(lambda u: u.email == request.email)
        if email is not None:
            return {
                'message': "email is already token"
            }
        user = Model.User(
            name=request.name,
            email=request.email,
            password=password,
        )
    return UserIn.from_orm(user)


@router.post('/user/update', response_model=UserOut, tags=['User'])
def update_current_user(body: UserIn, current_user: UserOut = Depends(get_current_user)):
    with db_session:
        _id = current_user.id

        Model.User[_id].name = body.name if body.name is not None else Model.User[_id].name
        # Model.User[_id].email = body.email
        if body.password is not None:
            password = Hash.get_password_hash(body.password)
            Model.User[_id].password = password

        return current_user


# @router.put('/user/{id}', tags=['User'])
# def update_user(body: UserUpdate, id: int, current_user: UserOut = Depends(get_current_user)):
#     with db_session:
#         password = Hash.get_password_hash(body.password)
#         Model.User[id].name = body.name
#         Model.User[id].email = body.email
#         Model.User[id].password = password
#         user = Model.User[id]
#         return user


@router.delete('/user/{id}', tags=['User'])
def delete_user(id: int, current_user: UserIn = Depends(get_current_user)):
    with db_session:
        if id != current_user.id:
            user = Model.User.select(lambda u: u.id == id)
            user.delete()
            return {
                'message': 'Delete successfully'
            }
        else:
            return {
                'message': "Can not delete your current user"
            }
