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

from pydantic import EmailStr
from redis import Redis
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from src.riwayat.repository import RepoRiwayat
from src.schema import PasswordHash, Users
from src.user.model import UserCreate
from src.user.repository import RepoUser
from utils.model.request import updateUser
from utils.password_handler import PasswordHandler



class UserService():

    def __init__(self, db):
        self.session = db
        self.redis = Redis()
        self.repo  = RepoUser(self.session)


    def signup(self, username, email, password, nama_depan, nama_belakang, alamat):
        # Validasi input
        if not (username and email and password):
            print("Semua kolom harus diisi.")
            return False, 42201

        # Validasi panjang kolom
        if len(username) > 28 or len(email) > 255 or len(nama_depan) > 25 or len(nama_belakang) > 25:
            print("Panjang kolom melebihi batas.")
            return False, 42202

        # Cek apakah email atau username sudah digunakan
        if self.session.query(Users).filter_by(email=email).first() or self.session.query(Users).filter_by(
            username=username).first():
            print("Email atau username sudah digunakan.")
            return False, 42201

        # Generate salt dan hash password menggunakan PasswordHandler yang telah dibuat sebelumnya
        password_handler = PasswordHandler()
        cek_password_string = password_handler.validate_password_string(password)
        if cek_password_string['success'] is False:
            return False, 42203

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
        return True, 200


    def get_user(self,  db: Session, username) -> Users:
        try:
            user = db.query(Users).filter(Users.username == username).first()
            res = Users.model_validate(user) if user else None
        except NoResultFound:
            res = None

        return res

    def get_user_by_id(self, db: Session, user_id: str) -> Type[Users] | None:
        # user_uuid = uuid.UUID(user_id).hex
        try:
            user = db.query(Users).filter(Users.kode_user == user_id).first()
            res = user
        except NoResultFound:
            res = None
        return res

    async def update_password(self, user_id:str, password:str, new_password:str, baypass: bool = False):
        user = self.get_user_by_id(self.session, user_id)
        if not user:
            return False, 'user not found'

        password_hash = self.session.query(PasswordHash).filter_by(kode_user=user.kode_user).first()
        password_handler = PasswordHandler()
        cek_password_string = password_handler.validate_password_string(new_password)
        if cek_password_string['success'] is False:
            return False, cek_password_string['message']
        if baypass is False:
            if not password_handler.verify_password(password, password_hash.password_hash, password_hash.salt):
                return False, 'Password lama salah'

        hashed_password, salt = password_handler.hash_password(new_password)
        try:
            password_hash.password_hash = hashed_password
            password_hash.salt = salt
            self.session.commit()
            return True, 'Password successfully updated'
        except Exception as e:
            self.session.rollback()
            print(e)
            return False, 'Failed to update password'

    async def update_profile(self, user_id:str, data: updateUser):
        user = self.get_user_by_id(self.session, user_id)
        if not user:
            return False, 'user not found'

        try:
            user.username = data.username
            user.email = data.email
            user.alamat = data.address
            user.nama_depan = data.first_name
            user.nama_belakang = data.last_name
            self.session.commit()
            return True, 'Profile successfully updated'
        except Exception as e:
            self.session.rollback()
            print(e)
            return False, 'Failed to update profile'


    async def get_all_users(self, limit: int = 10, offset: int = 0, searchBy: str = "", search: str = "", order: str = "", by: str = ""):
        repoUser  =RepoUser(self.session)
        if offset>0:
            p=0
        offset= p*limit
        total_data, user = await  repoUser.get_all_user(limit, offset, searchBy, search, order, by)
        resp = {}
        entry = []
        if user is not None:
            total_data = total_data
            data = user
            resp['total_data'] = total_data
            for d in data:
                user_data = {
                    "kode_user": d.kode_user,
                    "username": d.username,
                    "email": d.email,
                    "level": d.level,
                    "nama_depan": d.nama_depan,
                    "nama_belakang": d.nama_belakang,
                    "alamat": d.alamat
                }
                entry.append(user_data)
            resp['entries'] = entry
            resp['total_data'] = total_data
            resp['entries_total'] =  len(entry)
            resp['total_page'] = int(total_data / limit) + 1 if total_data % limit != 0 else int(total_data / limit)
        return resp


    async def delete_user(self, kode_user:str):
        repo = RepoUser(self.session)
        repoRiwayat = RepoRiwayat(self.session)
        try:
            await repoRiwayat.delete_by_userid(kode_user)
            status, message = await repo.delete_user(kode_user)
        except Exception as e:
            print(e)
            return False, 'Failed to delete user'
        return status, message

    async def create_user(self, data: UserCreate):
        user = RepoUser(self.session)

        # Validasi panjang kolom
        if len(data.username) > 28 or len(data.email) > 255 or len(data.nama_depan) > 25 or len(data.nama_belakang) > 25:
            print("Panjang kolom melebihi batas.")
            return False, 42202, 'Terdapat kolom melebihi batas.'


        # Cek apakah email atau username sudah digunakan
        if await user.select_by('username', data.username) or await user.select_by('email', data.email):
            print("Email atau username sudah digunakan.")
            return False, 42201, 'Email atau username sudah digunakan'

        # Generate salt dan hash password menggunakan PasswordHandler yang telah dibuat sebelumnya
        password_handler = PasswordHandler()
        # cek_password_string = password_handler.validate_password_string(data.password)
        # if cek_password_string['success'] is False:
        #
        #     return False, 42203

        hashed_password, salt = password_handler.hash_password(data.password)

        status, message = await user.add_user(data, hashed_password, salt)
        # Membuat objek User

        return True, 200, message

    async def get_user_data(self, column, data):
        data = await self.repo.select_by(column, data)
        return data