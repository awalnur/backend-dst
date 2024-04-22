# ============================================
#                                           
#   Project Name :  be_sistem_pakar               
#   -------------------------------------   
#   Create by    : hexa at 26/02/24       
#   Copyright © 2024 Delameta Bilano     
#                                           
# ============================================
from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from redis import Redis
from sqlalchemy.orm import Session

from config.connection import get_db, get_redis
from src.auth.service import Auth
from src.user.service import UserService
from utils.model.request import loginRequest, RegisterRequest
from utils.model.response import DefaultResponse, Token

auth = APIRouter(tags=['Authentication Router'], prefix='/auth')

@auth.post('/login',responses={200: {"model": DefaultResponse}})
async def login(db:Annotated[Session, Depends(get_db)],redis: Annotated[Redis, Depends(get_redis)], request: loginRequest):
    user = Auth(db = db, redis=redis)
    response = user.login(redis= redis,username=request.username, password=request.password)

    return response

@auth.post('/token',responses={200: {"model": DefaultResponse}})
async def login_for_access_token(
db:Annotated[Session, Depends(get_db)],redis: Annotated[Redis, Depends(get_redis)],
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    user = Auth(db = db, redis=redis)

    response = user.login(redis=redis, username=form_data.username, password=form_data.password)

    return Token(access_token=response['data']['accesstoken'], token_type="bearer")



@auth.post('/register')
async def register(db: Annotated[Session, Depends(get_db)], registerData: RegisterRequest):
    user = UserService(db = db)
    user.signup(username=registerData.username, email=registerData.email, password=registerData.password,
                nama_depan=registerData.first_name, nama_belakang=registerData.last_name, alamat=registerData.address)
    return 0
