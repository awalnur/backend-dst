# ============================================
#                                           
#   Project Name :  be_sistem_pakar               
#   -------------------------------------   
#   Create by    : hexa at 25/02/24       
#   Copyright © 2024 Delameta Bilano     
#                                           
# ============================================
import os

import psycopg2  # Pastikan telah menginstal driver psycopg2
import redis

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from config.config import config

# from app.core.config import settings

# SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"

# SQLALCHEMY_DATABASE_URL = f"postgresql://dev:userdev@{settings.DB_HOST}/{settings.DB_NAME}"
# SQLALCHEMY_DATABASE_URL = f"postgresql://postgres:postgres@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
SQLALCHEMY_DATABASE_URL = f"postgresql://{config.DB_USER}:{config.DB_PASS}@{config.DB_HOST}:{config.DB_PORT}/{config.DB_NAME}"

# engine = create_engine(
#     SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
# )

# SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}/{settings.DB_NAME}"

engine = create_engine(SQLALCHEMY_DATABASE_URL, isolation_level="AUTOCOMMIT", pool_pre_ping=True,
                       connect_args={
                           "keepalives": 1,
                           "keepalives_idle": 30,
                           "keepalives_interval": 10,
                           "keepalives_count": 5,
                       })

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db_session = SessionLocal()
    try:
        yield db_session
    finally:
        db_session.close()


Base = declarative_base()

redis_url = config.REDIS_URL


# def get_redis():
def get_redis():
    redis_con = redis.from_url(redis_url)
    try:
        yield redis_con
    finally:
        redis_con.close()
