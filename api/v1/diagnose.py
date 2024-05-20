# ============================================
#                                           
#   Project Name :  be_sistem_pakar               
#   -------------------------------------   
#   Create by    : hexa at 26/02/24       
#   Copyright © 2024 Delameta Bilano     
#                                           
# ============================================
from typing import Annotated

from fastapi import APIRouter, Depends, Security
from pydantic import BaseModel
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from config.connection import get_db
from src.diagnosa.service import DempsterShafer
from src.schema import Users
from utils.model.response import DefaultResponse
from utils.security import get_current_user

diagnose = APIRouter(tags=['Diagnose Router'], prefix='/diagnose')
class Gejala(BaseModel):
    kode_peternakan: str = None
    gejala: list

@diagnose.post('')
async def diagnose_api(db: Annotated[Session, Depends(get_db)], gejala: Gejala, current_user: Annotated[Users, Security(get_current_user, scopes=["Pengguna"])]):
    # TODO
    dempster = DempsterShafer(db)
    if len(gejala.gejala) < 2:
        return JSONResponse(status_code=422, content={'message': 'Minimal 2 gejala', 'data': []}) # DefaultResponse(status_code=422, message="Minimal 2 gejala", data=[])
    else:
        status, message, id = await dempster.dempster_shafer(data=gejala.dict(), user_id=current_user.kode_user)
        if status:
            res = {
                'kode_riwayat': id,
            }
            return DefaultResponse(status_code=200, message=message, data=res)
        else:
            return JSONResponse(status_code=422, content={'message': message,
                                                          'data': []})  # DefaultResponse(status_code=422, message="Minimal 2 gejala", data=[])

    # res = dempster.dempster_shafer(data={'gejala':['G1', 'G2', 'G3', 'G4','G33']})
    # return res


@diagnose.post('/public')
async def diagnose_api(db: Annotated[Session, Depends(get_db)], gejala: Gejala):
    # TODO
    dempster = DempsterShafer(db)
    if len(gejala.gejala) < 2:

        return JSONResponse(status_code=422, content={'message': 'Minimal 2 gejala',
                                                      'data': []})  # DefaultResponse(status_code=422, message="Minimal 2 gejala", data=[])
    else:
        status, message, id = await dempster.dempster_shafer(data=gejala.dict())
        if status:
            res = {
                'kode_riwayat': id,
            }
            return DefaultResponse(status_code=200, message=message, data=res)
        else:
            return JSONResponse(status_code=422, content={'message': message,
                                                          'data': []})  # DefaultResponse(status_code=422, message="Minimal 2 gejala", data=[])



@diagnose.get('/result/{id}')
async def result_public(db: Annotated[Session, Depends(get_db)], id: int, current_user: Annotated[Users, Security(get_current_user, scopes=["Pengguna"])]=None):
    # TODO
    diagnose = DempsterShafer(db)
    status, message, data = await diagnose.get_diagnose_by_id(id=id, kode_user=current_user.kode_user)
    if data is None:
        return JSONResponse(status_code=404, content={'status_code': 404,'message': 'Diagnose not found', 'data': []})

    return DefaultResponse(status_code=200, message=message, data=data)

@diagnose.get('/result/{id}/public')
async def result_public(db: Annotated[Session, Depends(get_db)], id):
    # TODO
    diagnose = DempsterShafer(db)

    status, message, data = await diagnose.get_diagnose_by_id(id=id)
    if data is None:
        return JSONResponse(status_code=404, content={'status_code': 404, 'message': 'Diagnose not found', 'data': []})

    return DefaultResponse(status_code=200, message=message, data=data)

@diagnose.get('/result/{id}/admin')
async def result_public(db: Annotated[Session, Depends(get_db)],
                        current_user: Annotated[Users, Security(get_current_user, scopes=["Admin"])],
                        id: int):
    # TODO
    diagnose = DempsterShafer(db)
    status, message, data = await diagnose.get_diagnose_by_id(id=id, admin=True)
    if data is None:
        return JSONResponse(status_code=404, content={'status_code': 404, 'message': 'Diagnose not found', 'data': []})

    return DefaultResponse(status_code=200, message=message, data=data)