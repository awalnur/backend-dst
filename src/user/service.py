# ============================================
#                                           
#   Project Name :  be_sistem_pakar               
#   -------------------------------------   
#   Create by    : hexa at 04/03/24       
#   Copyright © 2024 Delameta Bilano     
#                                           
# ============================================
import uuid
from typing import Type

from fastapi import HTTPException
from redis import Redis
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session
from starlette import status

from src.schema import PasswordHash, Users
from utils.password_handler import PasswordHandler



class UserService():

    def __init__(self, db):
        self.session = db
        self.redis = Redis()

    def signup(self, username, email, password, nama_depan, nama_belakang, alamat):
        # Validasi input
        if not (username and email and password and nama_depan and nama_belakang and alamat):
            print("Semua kolom harus diisi.")
            return

        # Validasi panjang kolom
        if len(username) > 28 or len(email) > 255 or len(nama_depan) > 25 or len(nama_belakang) > 25:
            print("Panjang kolom melebihi batas.")
            return

        # Cek apakah email atau username sudah digunakan
        if self.session.query(Users).filter_by(email=email).first() or self.session.query(Users).filter_by(
            username=username).first():
            print("Email atau username sudah digunakan.")
            return

        # Generate salt dan hash password menggunakan PasswordHandler yang telah dibuat sebelumnya
        password_handler = PasswordHandler()
        cek_password_string = password_handler.validate_password_string(password)
        if cek_password_string['success'] is False:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=cek_password_string['message'])

        hashed_password, salt = password_handler.hash_password(password)

        # Membuat objek User
        new_user = Users(
            username=username,
            email=email,
            nama_depan=nama_depan,
            nama_belakang=nama_belakang,
            alamat=alamat,
            level='Pengguna',
            status='Active'
        )
        # Menyimpan objek User ke database
        self.session.add(new_user)
        self.session.commit()

        # Membuat objek PasswordHash
        password_hash = PasswordHash(
            kode_user=new_user.kode_user,
            salt=salt,
            password_hash=hashed_password
        )

        # Menyimpan objek User dan PasswordHash ke database
        self.session.add(new_user)
        self.session.add(password_hash)
        self.session.commit()

        print("Pendaftaran berhasil!")

    # Fungsi untuk melakukan login


    def get_user(self,  db: Session, username) -> Users:
        try:
            user = db.query(Users).filter(Users.username == username).first()
            res = Users.model_validate(user) if user else None
        except NoResultFound:
            res = None

        return res

    def get_user_by_id(self, db: Session, user_id: str) -> Type[Users] | None:
        user_uuid = uuid.UUID(user_id).hex
        try:
            user = db.query(Users).filter(Users.kode_user == user_uuid).first()
            res = user
        except NoResultFound:
            res = None
        return res

