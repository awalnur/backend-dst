# ============================================
#                                           
#   Project Name :  be_sistem_pakar               
#   -------------------------------------   
#   Create by    : hexa at 19/05/24       
#   Copyright © 2024 Delameta Bilano     
#                                           
# ============================================
from typing import Annotated

from fastapi import APIRouter, Depends, Security
from sqlalchemy.orm import Session

from config.connection import get_db
from src.dashboard.service import AdminService
from src.schema import Users
from utils.model.response import DefaultResponse
from utils.security import get_current_user

admin = APIRouter(tags=['Admin Router'], prefix='/admin')

@admin.get('/graph')
async def get_graph(db: Annotated[Session, Depends(get_db)],
                    current_user: Annotated[Users, Security(get_current_user, scopes=["Admin"])],
                    ):
    service =AdminService(db)
    entry = await service.get_dashboard()
    print(entry)
    return DefaultResponse(status_code=200, message="Success to get graph", data=entry)

