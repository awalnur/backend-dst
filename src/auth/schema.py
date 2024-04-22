# ============================================
#                                           
#   Project Name :  be_sistem_pakar               
#   -------------------------------------   
#   Create by    : hexa at 09/03/24       
#   Copyright © 2024 Delameta Bilano     
#                                           
# ============================================
from typing import Literal

from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str | None = "Bearer"
    refresh_token: str


class AccessToken(BaseModel):
    access_token: str
    token_type: str


class UserLogin(BaseModel):
    username: str
    password: str


class TokenData(BaseModel):
    user_id: str | None = None
    scopes: list[str] = []


class LogoutModel(BaseModel):
    device: Literal["all", "single"] = "single"
    access_token: str
    refresh_token: str
