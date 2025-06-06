# ============================================
#                                           
#   Project Name :  be_sistem_pakar               
#   -------------------------------------   
#   Create by    : hexa at 09/03/24       
#   Copyright © 2024 Delameta Bilano     
#                                           
# ============================================

from datetime import datetime, timedelta
from typing import Annotated
import re

from fastapi import Depends, HTTPException, Security
from fastapi.security import (
    OAuth2PasswordBearer,
    SecurityScopes,
)
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import ValidationError
from redis import Redis
from sqlalchemy.orm import Session

from config.config import config
from config.connection import get_db, get_redis
from src.auth.schema import TokenData
from utils.exceptions import ForbiddenException, CredentialsException, ValidationError as UPE

from src.schema import Users
from src.user.service import UserService
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/auth/token",
    scopes={"Admin": "Read information about the current user.", "Pengguna}": "Read items."},
)



def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def authenticate_user(db, username: str, password: str):
    user = UserService(db=db).get_user(db, username)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


def create_access_token(redis_con: Redis, data: dict, expires_delta: timedelta | None = None,
                        ):
    to_encode = data.copy()
    default_exp = timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + default_exp
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, config.SECRET_KEY, algorithm=config.ALGORITHM)
    redis_con.setex(name=f"userid_a_{to_encode.get('sub')}", time=default_exp,
                    value=encoded_jwt.encode('utf-8'))
    return encoded_jwt


# def create_refresh_token(data: dict, expires_delta: timedelta | None = None,
#                          ):
#     to_encode = data.copy()
#     if expires_delta:
#         expire = datetime.utcnow() + expires_delta
#     else:
#         expire = datetime.utcnow() + timedelta(days=config.REFRESH_TOKEN_EXPIRE_DAYS)
#     to_encode.update({"exp": expire})
#     encoded_jwt = jwt.encode(to_encode, config.REFRESH_TOKEN_SECRET_KEY, algorithm=config.ALGORITHM)
#     return encoded_jwt


def revoke_access_token(redis_conn: Redis, access_token: str):
    payload = jwt.decode(access_token, config.SECRET_KEY, algorithms=[config.ALGORITHM])
    try:
        redis_conn.delete(f"userid_a_{payload.get('sub')}")
    except Exception as e:
        print(f"error when revoke token, detail{e}")
        return False


# def revoke_refresh_token(db: Session, refresh_token):
#     try:
#         db.query(RefreshToken).filter(RefreshToken.refresh_token == refresh_token).delete()
#         return True
#     except Exception as e:
#         print(f"error when revoke token, detail{e}")
#         return False


async def get_current_user(
        db: Annotated[Session, Depends(get_db)],
        security_scopes: SecurityScopes, token: Annotated[str, Depends(oauth2_scheme)],
        redis_con: Annotated[Redis, Depends(get_redis)]
):
    try:
        payload = jwt.decode(token, config.SECRET_KEY, algorithms=[config.ALGORITHM])
        user_id: str = payload.get("sub")
        #user_id = kode_user
        check_token = redis_con.get(f"userid_a_{user_id}")
        if check_token is None:
            raise CredentialsException

        if token != check_token.decode('utf-8'):

            raise CredentialsException

        if user_id is None:
            raise CredentialsException

        token_scopes = payload.get("scopes", [])
        token_data = TokenData(scopes=token_scopes, user_id=user_id)
    except (JWTError, ValidationError):
        raise CredentialsException
    user = UserService(db=db).get_user_by_id(db, user_id=token_data.user_id)
    if user is None:
        raise ForbiddenException
    # if config.ENVIRONMENT == "production":
    # print(user.level)
    role = [user.level]
    scopes = security_scopes.scopes
    for scope in role:
        print(scope)
        scopes = security_scopes.scopes
        if scope not in scopes:
            raise ForbiddenException

    return user



async def get_current_user_2(
        db: Annotated[Session, Depends(get_db)],
        security_scopes: SecurityScopes, token: Annotated[str, Depends(oauth2_scheme)],
        redis_con: Annotated[Redis, Depends(get_redis)]
):
    try:
        payload = jwt.decode(token, config.SECRET_KEY, algorithms=[config.ALGORITHM])
        user_id: str = payload.get("sub")
        #user_id = kode_user
        check_token = redis_con.get(f"userid_a_{user_id}")
        if check_token is None:
            return None

        if token != check_token.decode('utf-8'):

            return None

        if user_id is None:
            return None

        token_scopes = payload.get("scopes", [])
        token_data = TokenData(scopes=token_scopes, user_id=user_id)
    except (JWTError, ValidationError):
        return None
    user = UserService(db=db).get_user_by_id(db, user_id=token_data.user_id)
    if user is None:
        return None
    # if config.ENVIRONMENT == "production":
    # print(user.level)
    role = [user.level]
    scopes = security_scopes.scopes
    for scope in role:
        scopes = security_scopes.scopes
        if scope not in scopes:
            return None

    return user


async def get_current_active_user(
        current_user: Annotated[Users, Security(get_current_user)]
):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


def extract_refresh_token_data(db, token_data: str):
    try:
        payload = jwt.decode(token_data, config.SECRET_KEY, algorithms=[config.ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise ForbiddenException
        token_scopes = payload.get("scopes", [])
        token_data = TokenData(scopes=token_scopes, user_id=user_id)
    except (JWTError, ValidationError):
        raise ForbiddenException
    user = UserService(db=db).get_user_by_id(db, user_id=token_data.user_id)
    if user is None:
        raise ForbiddenException
    return user


def set_redis_r_token(user_id: str, r_token: str, redis_con: Redis):
    redis_con.setex(f"userid_r_{user_id}", value=r_token, time=600)
