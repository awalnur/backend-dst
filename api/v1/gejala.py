# ============================================
#                                           
#   Project Name :  be_sistem_pakar               
#   -------------------------------------   
#   Create by    : hexa at 14/03/24       
#   Copyright © 2024 Delameta Bilano     
#                                           
# ============================================
from typing import Annotated

from fastapi import APIRouter, Depends, Body, Security
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from config.connection import get_db
from src.gejala.model import ModelGejala, ModelUpdateGejala
from src.gejala.service import ServiceGejala
from src.schema import Users
from utils.model.response import DefaultResponse, ErrorResponse
from utils.security import get_current_user

router_gejala = APIRouter(tags=['Gejala Router'], prefix='/gejala')


@router_gejala.post('/create', responses={201: {"model": DefaultResponse},
                                          422: {"model": ErrorResponse, "description": "Unprocessable Entity"},
                                          400: {"model": ErrorResponse, "description": "Bad Request"},
                                          500: {"model": ErrorResponse, "description": "Internal Server Error"}
                                          })
async def create_gejala(db: Annotated[Session, Depends(get_db)],

                        data: ModelGejala):
    service = ServiceGejala(db=db)
    resp, message, code = await service.create_gejala(data)
    return JSONResponse(status_code=code, content={'status_code':201, 'message':message, 'data':resp})

@router_gejala.get('/all')
async def get_all_gejala(db: Annotated[Session, Depends(get_db)], limit: int = 10, offset: int = 0, searchBy: str = "", search: str = "", order: str = "", by: str = ""):
    service = ServiceGejala(db=db)
    resp = await service.get_all_gejala(limit=limit, offset=offset, searchBy=searchBy, search=search, order=order, by=by)
    return DefaultResponse(status_code=200, message="Success to get all gejala", data=resp)

@router_gejala.get('/get/{kode_gejala}')
async def get_gejala_by_id(db: Annotated[Session, Depends(get_db)], kode_gejala: str):
    service = ServiceGejala(db=db)
    resp = await service.get_gejala_by_id(kode_gejala=kode_gejala)
    return DefaultResponse(status_code=200, message="Success to get gejala by id", data=resp)
@router_gejala.patch('/update/{kode_gejala}', responses={200: {"model": DefaultResponse},
                                                            422: {"model": ErrorResponse, "description": "Unprocessable Entity"}})
async def update_gejala_by_id(db: Annotated[Session, Depends(get_db)],
                              current_user: Annotated[Users, Security(get_current_user, scopes=["Admin"])],
                              kode_gejala: str, data: ModelUpdateGejala):
    service = ServiceGejala(db=db)

    resp, message = await service.update_gejala_by_id(kode_gejala=kode_gejala, gejala=data.gejala)
    return DefaultResponse(status_code=200, message=message, data=[])

@router_gejala.delete('/delete/{kode_gejala}', responses={200: {"model": DefaultResponse},
                                                            422: {"model": ErrorResponse, "description": "Unprocessable Entity"}})
async def delete_gejala_by_id(db: Annotated[Session, Depends(get_db)],
                              current_user: Annotated[Users, Security(get_current_user, scopes=["Admin"])],
                              kode_gejala: str):
    service = ServiceGejala(db=db)

    resp, message = await service.delete_gejala_by_id(kode_gejala=kode_gejala)
    return DefaultResponse(status_code=200, message=message, data=[])