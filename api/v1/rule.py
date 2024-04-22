# ============================================
#                                           
#   Project Name :  be_sistem_pakar               
#   -------------------------------------   
#   Create by    : hexa at 17/03/24       
#   Copyright © 2024 Delameta Bilano     
#                                           
# ============================================
from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from config.connection import get_db
from src.rule.model import addRule, updateRule
from src.rule.service import RuleService
from utils.model.response import DefaultResponse, ErrorResponse

router_rule = APIRouter(tags=['Rule Router'], prefix='/rule')

@router_rule.post('/create', responses={201: {"model": DefaultResponse},
                                        422: {"model": ErrorResponse, "description": "Unprocessable Entity"}, })
async def create_rule(db: Annotated[Session, Depends(get_db)], data: addRule):
    print(data)
    service = RuleService(db=db)
    resp, message = await service.create_new_rule(data)
    return JSONResponse(status_code=201, content={'status_code':201, 'message':message, 'data':resp})


@router_rule.put('/update/{kode_penyakit}', responses={200: {"model": DefaultResponse},
                                        422: {"model": ErrorResponse, "description": "Unprocessable Entity"},
                                        400: {"model": ErrorResponse, "description": "Bad Request"}})
async def update_rule(db: Annotated[Session, Depends(get_db)], kode_penyakit: str, data: updateRule):
    service = RuleService(db=db)
    resp, message, code = await service.update_rule(kode_penyakit, data)
    return JSONResponse(status_code=code, content={'status_code':code, 'message':message, 'data':resp})

@router_rule.delete('/delete/{kode_penyakit}', responses={200: {"model": DefaultResponse}})
async def delete_rule(db: Annotated[Session, Depends(get_db)], kode_penyakit: str):
    service = RuleService(db=db)
    resp, message, code = await service.delete_rule(kode_penyakit)
    return JSONResponse(status_code=code, content={'status_code':code, 'message':message, 'data':resp})

@router_rule.get('/all', responses={200: {"model": DefaultResponse}})
async def get_all_rule_data(db: Annotated[Session, Depends(get_db)], limit: int = 10, offset: int = 0, searchBy: str = "", search: str = "", order: str = "", by: str = ""):
    service = RuleService(db=db)
    resp = await service.get_all_rule(limit=limit, offset=offset, searchBy=searchBy, search=search, order=order, by=by)
    return JSONResponse(status_code=200, content={'status_code':200, 'message':'Success to get all rule', 'data':resp})