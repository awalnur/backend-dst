# ============================================
#                                           
#   Project Name :  be_sistem_pakar               
#   -------------------------------------   
#   Create by    : hexa at 10/03/24       
#   Copyright © 2024 Delameta Bilano     
#                                           
# ============================================
from fastapi import HTTPException
from sqlalchemy.orm import Session

from src.gejala.model import ModelGejala
from src.gejala.repository import RepoGejala
from src.schema import BaseGejala


class ServiceGejala:

    def __init__(self, db: Session):
        self.db = db

    async def create_gejala(self, data: ModelGejala):
        repo = RepoGejala(db=self.db)
        data_gejala = BaseGejala(kode_gejala=data.kode_gejala, gejala=data.gejala)
        insert, message, code = await repo.insert_gejala(data=data_gejala)
        if insert:
            return True, "Success to create gejala", code
        else:
            raise HTTPException(status_code=code, detail=message)

    async def get_all_gejala(self, limit: int = 10, offset: int = 0, searchBy: str = "", search: str = "", order: str = "", by: str = ""):
        repo = RepoGejala(db=self.db)
        return await repo.get_all_gejala(limit=limit, offset=offset, searchBy=searchBy, search=search, order=order, by=by)

    async def get_gejala_by_id(self, kode_gejala):
        repo = RepoGejala(db=self.db)
        gejala = await repo.get_gejala_by_id(kode_gejala=kode_gejala)
        if gejala is None:
            raise HTTPException(status_code=404, detail="Gejala not found")
        else:
            return {'kode_gejala': gejala.kode_gejala, 'gejala':gejala.gejala}

    async def update_gejala_by_id(self, kode_gejala: str, **kwargs):
        if kwargs.get('gejala') is None:
            raise HTTPException(status_code=422, detail="Gejala cannot be empty")

        repo = RepoGejala(db=self.db)
        update_gejala = await repo.update_gejala(kode_gejala=kode_gejala, **kwargs)

        if update_gejala:
            return True, "Success to update gejala"
        else:
            raise HTTPException(status_code=400, detail="Failed to update gejala")
        # return

    async def delete_gejala_by_id(self, kode_gejala: str):
        if kode_gejala is None:
            raise HTTPException(status_code=422, detail="Kode Gejala cannot be empty")
        repo = RepoGejala(db=self.db)
        status, message, code = await repo.delete_gejala_by_id(kode_gejala=kode_gejala)
        if status:
            return True, "Success to delete gejala"
        else:
            raise HTTPException(status_code=code, detail=message)