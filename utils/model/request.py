# ============================================
#                                           
#   Project Name :  be_sistem_pakar               
#   -------------------------------------   
#   Create by    : hexa at 26/02/24       
#   Copyright © 2024 Delameta Bilano     
#                                           
# ============================================
from pydantic import BaseModel


class loginRequest(BaseModel):
    username: str
    password: str
    admin: bool=False


class updatePassword(BaseModel):
    password: str
    new_password: str


class RegisterRequest(BaseModel):
    username: str
    password: str
    first_name: str
    last_name: str
    email: str
    address: str


class updateUser(BaseModel):
    username: str
    first_name: str
    last_name: str
    email: str
    address: str
