# ============================================
#                                           
#   Project Name :  be_sistem_pakar               
#   -------------------------------------   
#   Create by    : hexa at 26/02/24       
#   Copyright © 2024 Delameta Bilano     
#                                           
# ============================================
import json
from typing import Annotated

from fastapi import APIRouter, Depends, Body, HTTPException, File, UploadFile, Form
from sqlalchemy.orm import Session

from config.connection import get_db
from src.penyakit.model import ModelPenyakit, UpdatePenyakit
from src.penyakit.service import Penyakit
from utils.model.response import DefaultResponse

# from utils.model.response import DefaultResponse

router_penyakit = APIRouter(tags=['Penyakit Router'], prefix='/penyakit')


@router_penyakit.get('/get/{kode_penyakit}', responses={200: {"model": DefaultResponse}})
async def get_penyakit_by_id(db: Annotated[Session, Depends(get_db)], kode_penyakit: str):
    penyakit = Penyakit(db=db)
    get_penyakit = await penyakit.get_data_penyakit_by_id(kode_penyakit=kode_penyakit)
    if get_penyakit is None:
        raise HTTPException(status_code=404, detail="Penyakit not found")
    response = dict(get_penyakit._mapping)
    return DefaultResponse(status_code=200, message="Success to get penyakit", data=response)

@router_penyakit.get('/all', responses={200: {"model": DefaultResponse}})
async def get_all_penyakit(db: Annotated[Session, Depends(get_db)], limit: int = 10, offset: int = 0, searchBy: str = "", search: str = "", order: str = "", by: str = ""):
    penyakit = Penyakit(db=db)
    try:
        get_all_penyakit = await penyakit.get_all_penyakit(limit=limit, offset=offset, searchBy=searchBy, search=search, order=order, by=by)
        return DefaultResponse(status_code=200, message="Success to get all penyakit", data=get_all_penyakit)
    except Exception as e:
        print(f"error when get all penyakit, detail{e}")
        raise HTTPException(status_code=400, detail="Failed to get all penyakit")
@router_penyakit.post('/create', responses={201: {"model": DefaultResponse}})
async def create_penyakit(db: Annotated[Session, Depends(get_db)],
                          gambar: Annotated[UploadFile, File()]=None,
                          kode_penyakit: Annotated[str, Form()]=None,
                          nama_penyakit:Annotated[str, Form()]=None,
                          definisi:Annotated[str, Form()]=None,
                          penyebab:Annotated[str, Form()]=None,
                          penularan:Annotated[str, Form()]=None,
                          pencegahan:Annotated[str, Form()]=None,
                          penanganan:Annotated[str, Form()]=None):
    penyakit = Penyakit(db=db)
    await penyakit.add_penyakit(kode_penyakit=kode_penyakit, nama_penyakit=nama_penyakit, definisi=definisi, penyebab=penyebab, penularan=penularan, pencegahan=pencegahan, penanganan=penanganan, gambar=gambar)
    return DefaultResponse(status_code=201, message="berhasil menambahkan data penyakit", data=[])

@router_penyakit.put('/update/{kode_penyakit}', responses={201: {"model": DefaultResponse}})
async def update_penyakit(db: Annotated[Session, Depends(get_db)], kode_penyakit: str,
                          gambar: Annotated[UploadFile, File()]=None,
                          nama_penyakit:Annotated[str, Form()]=None,
                          definisi:Annotated[str, Form()]=None,
                          penyebab:Annotated[str, Form()]=None,
                          penularan:Annotated[str, Form()]=None,
                          pencegahan:Annotated[str, Form()]=None,
                          penanganan:Annotated[str, Form()]=None):
    penyakit = Penyakit(db=db)
    try:
        update_penyakit = await penyakit.update_penyakit(kode_penyakit=kode_penyakit, gambar=gambar, nama_penyakit=nama_penyakit, definisi=definisi, penyebab=penyebab, penularan=penularan, pencegahan=pencegahan, penanganan=penanganan)
        return DefaultResponse(status_code=201, message="Success to update penyakit", data=[])
    except Exception as e:
        print(f"error when update penyakit, detail{e}")
        raise HTTPException(status_code=400, detail="Failed to update penyakit")


@router_penyakit.delete('/delete/{kode_penyakit}', responses={201: {"model": DefaultResponse}})
async def delete_penyakit(db: Annotated[Session, Depends(get_db)], kode_penyakit: str):
    penyakit = Penyakit(db=db)
    delete_penyakit = await penyakit.delete_penyakit(kode_penyakit=kode_penyakit)
    if delete_penyakit is False:
        raise HTTPException(status_code=404, detail="Failed to delete penyakit")
    return DefaultResponse(status_code=201, message="Success to delete penyakit", data=[])
