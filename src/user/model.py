# ============================================
#                                           
#   Project Name :  be_sistem_pakar               
#   -------------------------------------   
#   Create by    : hexa at 09/03/24       
#   Copyright © 2024 Delameta Bilano     
#                                           
# ============================================
from typing import List
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    username: str
    email: str
    nama_depan: str
    nama_belakang: str
    alamat: str
    level: str = Field(default='Pengguna', example='Pengguna')


class UserCreate(UserBase):
    password: str

class UserModel(UserBase):
    user_id: UUID
    hashed_password: str
    is_active: bool
    # roles: List[Role] | None = None

    class Config:
        from_attributes = True