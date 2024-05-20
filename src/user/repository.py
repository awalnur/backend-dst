# ============================================
#                                           
#   Project Name :  be_sistem_pakar               
#   -------------------------------------   
#   Create by    : hexa at 16/05/24       
#   Copyright © 2024 Delameta Bilano     
#                                           
# ============================================
from sqlalchemy.orm import Session

from src.schema import Users, PasswordHash


class RepoUser:

    def __init__(self, db: Session):
        self.db = db

    async def get_all_user(self, limit: int = 10, offset: int = 0, searchBy: str = "", search: str = "", order: str = "", by: str = ""):
        query = self.db.query(Users).filter(Users.level != "Admin")
        total_data = query.count()
        if searchBy and search:
            if searchBy == "email":
                query = query.filter(Users.email.like(f"%{search}%"))
            if searchBy == "username":
                query = query.filter(Users.username.like(f"%{search}%"))
            if searchBy == "nama_depan":
                query = query.filter(Users.nama_depan.like(f"%{search}%"))
            if searchBy == "nama_belakang":
                query = query.filter(Users.nama_belakang.like(f"%{search}%"))
        if order and by:
            if by == "asc":
                query = query.order_by(getattr(Users, order).asc())
            if by == "desc":
                query = query.order_by(getattr(Users, order).desc())
        data = query.offset(offset).limit(limit).all()
        return total_data, data

    async def get_user_by_id(self, id):
        return self.db.query(Users).filter(Users.kode_user == id).first()
    async def select_by(self, column, data):
        col = getattr(Users, column)
        return self.db.query(Users).filter(col == data).first()
    async def update_user(self, id, data):
        user = self.get_user_by_id(self.db, id)
        if not user:
            return False, 'user not found'

        try:
            user.username = data.username
            user.email = data.email
            user.alamat = data.address
            user.nama_depan = data.first_name
            user.nama_belakang = data.last_name
            self.db.commit()
            return True, 'Perubahan berhasil disimpan'
        except Exception as e:
            self.db.rollback()
            print(e)
            return False, 'Failed to update profile'

    async def add_user(self, data: Users, password_hash, salt):
        try:
            new_user = Users(
                username=data.username,
                email=data.email,
                nama_depan=data.nama_depan,
                nama_belakang=data.nama_belakang,
                alamat=data.alamat,
                level=data.level,
                status='Active'
            )
            # Menyimpan objek User ke database
            self.db.add(new_user)
            self.db.commit()

            # Membuat objek PasswordHash
            password_hash = PasswordHash(
                kode_user=new_user.kode_user,
                salt=salt,
                password_hash=password_hash
            )

            # Menyimpan objek User dan PasswordHash ke database
            self.db.add(password_hash)
            self.db.commit()
            return True, 'Berhasil menambahkan User Baru'

        except Exception as e:
            self.db.rollback()
            print(e)
            return False, 'Failed to create user'

    async def delete_user(self, kode_user: str):
        user = await self.get_user_by_id(kode_user)
        if not user:
            return False, 'user not found'

        try:
            self.db.delete(user)
            self.db.commit()
            return True, 'Success to delete user'
        except Exception as e:
            self.db.rollback()
            print(e)
            return False, 'Failed to delete user'