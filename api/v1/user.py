# ============================================
#                                           
#   Project Name :  be_sistem_pakar               
#   -------------------------------------   
#   Create by    : hexa at 26/02/24       
#   Copyright © 2024 Delameta Bilano     
#                                           
# ============================================
from typing import Annotated

from fastapi import APIRouter, Security, Depends
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from config.connection import get_db
from src.schema import Users
from src.user.model import UserBase, UserCreate
from src.user.service import UserService
from utils.model.request import updatePassword, updateUser
from utils.model.response import DefaultResponse
from utils.security import get_current_user

router = APIRouter(prefix='/user', tags=['User Router'])






@router.get('/all')
async def get_all_user(
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[Users, Security(get_current_user, scopes=["Pengguna", "Admin"])],
    # FIXME ^^ This is must be activate later, Please
    limit: int = 10,
    page: int = 1,
    searchBy: str = "",
    search: str = "",
    order: str = "",
    by: str = ""
) :
    user = UserService(db=db)
    resp = await user.get_all_users(limit, page, searchBy, search, order, by)

    return DefaultResponse(status_code=200, message="Success to get all user", data=resp)

@router.get('/current_user')
async def get_current_user(
    current_user: Annotated[Users, Security(get_current_user, scopes=["Pengguna", "Admin"])]):
    return current_user


@router.put('/update_password')
async def update_password(
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[Users, Security(get_current_user, scopes=["Pengguna", "Admin"])],
    payload: updatePassword,
    kode_user: str
):
    user = UserService(db=db)
    if kode_user is None:
        userid = current_user.kode_user
        # userid = None
        bypas=False
    else:
        userid = kode_user
        bypas=True

    status, message = await user.update_password(
        user_id=userid,
        password=payload.password,
        new_password=payload.new_password,
        baypass=bypas
    )
    if status:
        return DefaultResponse(status_code=200, message=message, data=[])
    else:
        return JSONResponse(status_code=422, content={'status_code': '42201', 'message': message, 'data': []})
@router.put('/update_profile')
async def update_profile(
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[Users, Security(get_current_user, scopes=["Pengguna", "Admin"])],
    payload: updateUser,
    kode_user: str= None
):
    # print('.'+kode_user+'.')
    user = UserService(db=db)
    if kode_user is None:
        userid = current_user.kode_user
        # userid = None
    else:
        userid = kode_user
    print(userid)
    status, message = await user.update_profile(
        user_id=userid,
        data=payload
    )
    if status:
        return DefaultResponse(status_code=200, message=message, data=[])
    else:
        return JSONResponse(status_code=422, content={'message': message, 'data': []})



@router.delete('/delete/{kode_user}')
async def delete_user(
    db: Annotated[Session, Depends(get_db)],
    # current_user: Annotated[Users, Security(get_current_user, scopes=["Pengguna", "Admin"])],
    kode_user: str
):
    user = UserService(db=db)

    status, message = await user.delete_user(
        kode_user=kode_user
    )
    if status:
        return DefaultResponse(status_code=200, message=message, data=[])
    else:
        return JSONResponse(status_code=422, content={'message': message, 'data': []})


@router.post('/create')
async def create_user(db: Annotated[Session, Depends(get_db)],
                      # current_user: Annotated[Users, Security(get_current_user, scopes=["Pengguna", "Admin"])],
                    data: UserCreate
                      ):
    user = UserService(db=db)
    status, http_res, message = await user.create_user(data)
    if status:
        return DefaultResponse(status_code=200, message=message, data=[])
    else:
        return JSONResponse(status_code=400, content={'message': message, 'data': []})


@router.get('/get/{kode_user}')
async def get_user_by_id(
    db: Annotated[Session, Depends(get_db)],
    # current_user: Annotated[Users, Security(get_current_user, scopes=["Pengguna", "Admin"])],
    kode_user: str
):
    user = UserService(db=db)
    resp = await user.get_user_data('kode_user', kode_user)
    if resp:
        res  = {
            'kode_user': str(resp.kode_user),
            'username': resp.username,
            'email': resp.email,
            'level': resp.level,
            'nama_depan': resp.nama_depan,
            'nama_belakang': resp.nama_belakang,
            'alamat': resp.alamat
        }
        return JSONResponse(status_code=200, content={'status_code':200, 'message':'Success to get user', 'data':res})
    else:
        return JSONResponse(status_code=404, content={'status_code': 404, 'message': 'User not found', 'data': []})