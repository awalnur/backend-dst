# ============================================
#                                           
#   Project Name :  be_sistem_pakar               
#   -------------------------------------   
#   Create by    : hexa at 28/04/24       
#   Copyright © 2024 Delameta Bilano     
#                                           
# ============================================


from typing import Annotated

from fastapi import APIRouter, Depends, Security
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from config.connection import get_db
from src.riwayat.service import RiwayatService
from src.schema import Users
from utils.security import get_current_user

router = APIRouter(tags=['Riwayat Router'], prefix='/riwayat')

@router.get('/all')
async def  get_all_riwayat_data(
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[Users, Security(get_current_user, scopes=["Pengguna", "Admin"])],

    limit: int = 10, page: int = 0, searchBy: str = "", search: str = "", order: str = "", by: str = ""
):
    service = RiwayatService(db)
    if current_user.level == "Pengguna":
        user_id = current_user.kode_user
    else:
        user_id = None
    if page == 0:
        page = 1
    offset = page - 1
    resp = await service.get_all_riwayat(limit=limit, offset=offset, searchBy=searchBy, search=search, order=order, by=by, user_id=user_id)
    if resp is not None:
        return JSONResponse(status_code=200, content={'status_code':200, 'message':'Success to get all riwayat', 'data':resp})
    return JSONResponse(status_code=200, content={'status_code':404, 'message':'Data not Found', 'data':resp})

@router.get('/last')
async def  get_last_diagnose_data(
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[Users, Security(get_current_user, scopes=["Pengguna", "Admin"])]
):
    service = RiwayatService(db)
    resp = await service.get_last_riwayat(kode_user=current_user.kode_user)
    print(current_user.kode_user)
    if resp is not None:
        return JSONResponse(status_code=200, content={'status_code':200, 'message':'Success to get last diagnose', 'data':resp})

@router.delete('/delete/{kode_riwayat}')
async def delete_riwayat(kode_riwayat: str, db: Annotated[Session, Depends(get_db)],
                         current_user: Annotated[Users, Security(get_current_user, scopes=["Pengguna", "Admin"])],
                         kode_user: str=None):
    service = RiwayatService(db)
    if current_user.level == "Pengguna":
        kode_user = current_user.kode_user

    resp, message = await service.delete_riwayat(kode_riwayat=kode_riwayat, kode_user=kode_user)
    if resp:
        return JSONResponse(status_code=200, content={'status_code':200, 'message':'Success to delete riwayat', 'data':[]})
    else:
        return JSONResponse(status_code=400, content={'status_code':400, 'message':message, 'data':[]})
