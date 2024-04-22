# ============================================
#                                           
#   Project Name :  be_sistem_pakar               
#   -------------------------------------   
#   Create by    : hexa at 26/02/24       
#   Copyright © 2024 Delameta Bilano     
#                                           
# ============================================
from typing import Annotated

from fastapi import APIRouter, Security

from src.schema import Users
from utils.security import get_current_user

router = APIRouter(prefix='/user', tags=['User Router'])

@router.get('/current_user')
async def get_current_user(
    current_user: Annotated[Users, Security(get_current_user, scopes=["Pengguna", "Admin"])]):
    return current_user

