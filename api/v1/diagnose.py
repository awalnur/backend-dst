# ============================================
#                                           
#   Project Name :  be_sistem_pakar               
#   -------------------------------------   
#   Create by    : hexa at 26/02/24       
#   Copyright © 2024 Delameta Bilano     
#                                           
# ============================================
from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from config.connection import get_db
from src.diagnosa.service import DempsterShafer
from utils.model.response import DefaultResponse

diagnose = APIRouter(tags=['Diagnose Router'], prefix='/diagnose')
class Gejala(BaseModel):
    gejala: list

@diagnose.post('')
async def diagnose_api(db: Annotated[Session, Depends(get_db)], gejala: Gejala):
    # TODO
    dempster = DempsterShafer(db)
    print(gejala.gejala)
    if len(gejala.gejala) < 2:

        return DefaultResponse(status_code=422, message="Minimal 2 gejala", data=[])
    else:
        res = dempster.dempster_shafer(data=gejala.dict())
        return DefaultResponse(status_code=200, message="Success to diagnose", data=res)
    # res = dempster.dempster_shafer(data={'gejala':['G1', 'G2', 'G3', 'G4','G33']})
    # return res

