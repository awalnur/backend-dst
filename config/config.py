# ============================================
#                                           
#   Project Name :  be_sistem_pakar               
#   -------------------------------------   
#   Create by    : hexa at 25/02/24       
#   Copyright © 2024 Delameta Bilano     
#                                           
# ============================================
from pydantic_settings import BaseSettings


class Config(BaseSettings):
    # API_VERSION: str
    DB_HOST: str
    DB_PORT: str
    DB_NAME: str
    DB_USER: str
    DB_PASS: str
    SECRET_KEY: str
    REFRESH_TOKEN_SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_DAYS: int

    class Config:
        env_file = 'env/.env_devel'
        env_file_encoding = 'utf-8'


config = Config()
