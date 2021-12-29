from fastapi import APIRouter, Depends, File, UploadFile
from fastapi.staticfiles import StaticFiles
from pony.orm import db_session, commit, flush
from ..models.model import Model
from ..models.schemasIn import UserIn, RegisterIn
from ..models.schemasOut import UserOut
from ..utils.hashPassword import Hash
from ..utils import helper
from datetime import date
from ..config.auth import get_current_user, get_current_active_user

router = APIRouter()


@router.get("/users/me", response_model=UserOut, tags=['User'])
async def read_users_me(current_user: UserIn = Depends(get_current_active_user)):
    return current_user


@router.get('/user', tags=['User'])
async def get_all_user(current_user: UserIn = Depends(get_current_active_user)):
    with db_session:
        user = Model.User.select()
        result = [UserOut.from_orm(u) for u in user]
    return result


@router.get('/user/{id}', tags=['User'])
def get_user_by_id(id: int, current_user: UserIn = Depends(get_current_user)):
    with db_session:
        user = Model.User.get(lambda u: u.id == id)
        if not user:
            return {'message': f'User id: {id} not found!'}
    return UserIn.from_orm(user)


@router.post('/register', tags=['Authenticate'])
def register(request: RegisterIn):
    with db_session:
        if not helper.isEmail(request.email):
            return {
                'message': "email request '@gmail.com'"
            }
        if not request.password == request.con_password:
            return {
                'message': "Invalid Password and Confirm Password"
            }
        password = Hash.get_password_hash(request.password)
        email = Model.User.get(lambda u: u.email == request.email)
        if email is not None:
            return {
                'message': "email is already token"
            }
        try:
            user = Model.User(
                name=request.name,
                email=request.email,
                password=password,
            )
        except ValueError:
            pass
    return {'message': 'Register successfully'}


@router.post('/user', tags=['User'])
def create_user(request: UserIn, current_user: UserIn = Depends(get_current_active_user)):
    with db_session:
        if not request.email:
            return {
                'success': 0,
                'message': 'Email is request!'
            }
        if not helper.isEmail(request.email):
            return {
                'success': 0,
                'message': "email request '@gmail.com'"
            }
        if request.password:
            if not request.con_password:
                request.con_password = ""
            if not request.password == request.con_password:
                return {
                    'success': 0,
                    'message': "Invalid Password and Confirm Password"
                }
        else:
            return {
                'success': 0,
                'message': 'password is request!'
            }
        password = Hash.get_password_hash(request.password)
        email = Model.User.get(lambda u: u.email == request.email)
        if email is not None:
            return {
                'success': 0,
                'message': "email is already token"
            }
        try:
            user = Model.User(
                name=request.name,
                email=request.email,
                password=password,
                dob=request.dob if request.dob else None,
                gender=request.gender if request.gender else '',
                expires_in='',
                profile_img='',
                about_me=request.about_me if request.about_me else '',
                address=request.address if request.address else ""
            )
        except ValueError:
            pass
    return {
        'success': 1,
        'message': 'Register successfully'
    }


# @router.post('/user/update/{id}', response_model=UserOut, tags=['User'])
# def update_current_user(id: int, body: UserIn, current_user: UserOut = Depends(get_current_user)):
#     with db_session:
#         _id = current_user.id
#
#         Model.User[_id].name = body.name if body.name is not None else Model.User[_id].name
#         # Model.User[_id].email = body.email
#         if body.password is not None:
#             password = Hash.get_password_hash(body.password)
#             Model.User[_id].password = password
#
#         return current_user


@router.put('/user/{id}', tags=['User'])
def update_user(body: UserIn, id: int, current_user: UserOut = Depends(get_current_user)):
    with db_session:
        user = Model.User.get(lambda u: u.id == id)
        if not user:
            return {
                'success': 0,
                'message': 'User not found'
            }
        if body.password:
            if not body.con_password:
                body.con_password = ""
            if not body.password == body.con_password:
                return {
                    'success': 0,
                    'message': "Invalid Password and Confirm Password"
                }
            user.password = Hash.get_password_hash(body.password)
        try:
            user.name = body.name if body.name is not None else user.name
            user.gender = body.gender if body.gender is not None else user.gender
            user.dob = body.dob if body.dob is not None else user.dob
            user.profile_img = ''
            user.about_me = body.about_me if body.about_me is not None else user.about_me
            user.address = body.address if body.address is not None else user.address
            return {
                'success': 1,
                'message': 'Update successfully'
            }
        except ValueError:
            pass


@router.delete('/user/{id}', tags=['User'])
def delete_user(id: int, current_user: UserIn = Depends(get_current_user)):
    with db_session:
        if id != current_user.id:
            user = Model.User.select(lambda u: u.id == id)
            if not user:
                return {'message': f'User id: {id} not found!'}
            user.delete()
            return {
                'message': 'Delete successfully'
            }
        else:
            return {
                'message': "Can not delete your current user"
            }
