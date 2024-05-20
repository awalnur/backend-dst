# ============================================
#                                           
#   Project Name :  be_sistem_pakar               
#   -------------------------------------   
#   Create by    : hexa at 09/03/24       
#   Copyright © 2024 Delameta Bilano     
#                                           
# ============================================
from fastapi import HTTPException
from redis import Redis
from sqlalchemy.orm import Session
from starlette import status

from src.schema import PasswordHash, Users
from utils.password_handler import PasswordHandler
from utils.security import create_access_token


class Auth:

    def __init__(self, db: Session, redis: Redis):
        self.db = db
        self.redis = redis
    def login(self, redis, username, password, asAdmin=False):
        # Validasi input
        if not (username and password):
            print("Email/Username dan password harus diisi.")
            return

        # Mendapatkan data user berdasarkan email
        user = self.db.query(Users).filter_by(username=username).first()
        if user:
            # Mendapatkan data password_hash berdasarkan kode_user
            password_hash = self.db.query(PasswordHash).filter_by(kode_user=user.kode_user).first()
            if password_hash:

                # Verifikasi password
                password_handler = PasswordHandler()
                is_password_valid = password_handler.verify_password(password, password_hash.password_hash,
                                                                     password_hash.salt)

                if is_password_valid:
                    print(user.level)
                    if asAdmin and user.level.lower() != 'admin':
                        print("Email/Username dan password harus diisi.")

                        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                            detail="Invalid email or password")

                    elif asAdmin and user.level.lower() == 'admin':

                        accesstoken = create_access_token(redis, data={'sub': str(user.kode_user)})
                        res = {
                            'detail': 'Login Berhasil!',
                            'data':{
                                'accesstoken': accesstoken,
                                'expired': 3600
                            }
                        }
                    else:
                        accesstoken = create_access_token(redis, data={'sub': str(user.kode_user)})
                        res = {
                            'detail': 'Login Berhasil!',
                            'data': {
                                'accesstoken': accesstoken,
                                'expired': 3600
                            }
                        }
                    return res
                else:
                    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")
            else:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")
        else:

            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")