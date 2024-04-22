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

from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    username: str
    email: EmailStr


class UserCreate(UserBase):
    password: str
    role_id: int


class UserModel(UserBase):
    user_id: UUID
    hashed_password: str
    is_active: bool
    # roles: List[Role] | None = None

    class Config:
        from_attributes = True