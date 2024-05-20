# ============================================
#                                           
#   Project Name :  be_sistem_pakar               
#   -------------------------------------   
#   Create by    : hexa at 23/04/24       
#   Copyright © 2024 Delameta Bilano     
#                                           
# ============================================
from typing import Annotated

from fastapi import APIRouter, Depends, Security
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from config.connection import get_db
from src.farm.model import FarmData
from src.farm.service import FarmService
from src.schema import Users
from utils.model.response import DefaultResponse
from utils.security import get_current_user

farm_api = APIRouter(tags=['Farm Router'], prefix='/farm')

@farm_api.post('/create')
async def create_farm(db: Annotated[Session, Depends(get_db)], data: FarmData, current_user: Annotated[Users, Security(get_current_user, scopes=["Pengguna"])]):
    serv = FarmService(db=db)
    create, message = await serv.create(user_id=current_user.kode_user, data=data.dict())
    if create is False:
        return DefaultResponse(status_code=422, message=message, data=None)
    return DefaultResponse(status_code=201, message=message, data=[])
@farm_api.get('/farm')
async def get_farm(db: Annotated[Session, Depends(get_db)],
                   current_user: Annotated[Users, Security(get_current_user, scopes=["Pengguna"])],
                   limit: int = 10, offset: int = 0, searchBy: str = "", search: str = "", order: str = "", by: str = "",
                   ):
    serv = FarmService(db=db)
    farm = await serv.get_farm(kode_pengguna=current_user.kode_user)
    if farm is None:
        return DefaultResponse(status_code=404, message="Farm data not found", data=farm)

    return DefaultResponse(status_code=200, message="Success to get farm", data=farm)


@farm_api.get('/option')
async def get_option(db: Annotated[Session, Depends(get_db)], current_user: Annotated[Users, Security(get_current_user, scopes=["Pengguna"])]):
    serv = FarmService(db=db)
    option = await serv.option_farm(kode_user=current_user.kode_user)

    if option is None:
        return DefaultResponse(status_code=404, message="Option data not found", data=option)
    return DefaultResponse(status_code=200, message="Success to get option", data=option)



@farm_api.put('/update/{id}')
async def update_farm(db: Annotated[Session, Depends(get_db)], id: str, data: FarmData, current_user: Annotated[Users, Security(get_current_user, scopes=["Pengguna"])]):
    serv = FarmService(db=db)
    update, message,res_data = await serv.update(kode_peternakan=id, data=data.dict(), kode_user = current_user.kode_user)
    if update is False:
        return JSONResponse(status_code=422, content={'status_code': 422, 'message': message, 'data': []}) # DefaultResponse(status_code=422, message=message, data=None)
    return DefaultResponse(status_code=200, message=message, data=res_data)

@farm_api.delete('/delete/{id}')
async def delete_farm(db: Annotated[Session, Depends(get_db)], id: str, current_user: Annotated[Users, Security(get_current_user, scopes=["Pengguna"])]):
    serv = FarmService(db=db)
    delete, message = await serv.delete(kode_peternakan=id, kode_user = current_user.kode_user)
    if delete is False:
        return JSONResponse(status_code=422, content={'status_code': 422, 'message': message, 'data': []}) # DefaultResponse(status_code=422, message=message, data=None)
    return DefaultResponse(status_code=200, message=message, data=[])
