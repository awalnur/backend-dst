# ============================================
#                                           
#   Project Name :  be_sistem_pakar               
#   -------------------------------------   
#   Create by    : hexa at 23/04/24       
#   Copyright © 2024 Delameta Bilano     
#                                           
# ============================================
from typing import Annotated

from sqlalchemy.orm import Session

from src.farm.repository import RepoFarm

class FarmService:

    def __init__(self, db: Session):
        self.db = db
        self.repo = RepoFarm(db=self.db)
    async def create(self, user_id: str, data: dict):
        insert_data = {
            "kode_user": user_id,
            "nama_peternakan": data["nama_peternakan"],
            "alamat_peternakan": data["alamat_peternakan"]
        }
        success, message =await self.repo.create_farm(data=insert_data)

        return success, message

    async def update(self, kode_peternakan: str, data: dict, kode_user: str):
        update_data = {
            "nama_peternakan": data["nama_peternakan"],
            "alamat_peternakan": data["alamat_peternakan"]
        }
        success, message, data = await self.repo.update_farm(id=kode_peternakan, data=update_data, kode_user=kode_user)
        return success, message, data

    async def delete(self, kode_peternakan: str, kode_user: str):
        success, message = await self.repo.delete_farm(id=kode_peternakan, kode_user=kode_user)
        return success, message
    async def get_farm(self,kode_pengguna=None, limit: int = 100, offset: int = 0, searchBy: str = "", search: str = "", order: str = "", by: str = ""):
        repo = RepoFarm(db=self.db)
        farmdata= await repo.get_all_farm(kode_pengguna=kode_pengguna)
        if farmdata is None:
            return None
        entries=[]
        for data in farmdata:
            entries.append({
                'kode_peternakan': data.kode_peternakan,
                'nama_peternakan': data.nama_peternakan,
                'alamat_peternakan': data.alamat_peternakan
            })
        data = {
            'entries': entries,
            'total': len(entries)
        }
        return data



    async def option_farm(self, kode_user: str):
        repo = RepoFarm(db=self.db)
        option_data = await repo.option_farm(kode_user=kode_user)
        if len(option_data) is 0:
            return None
        option = []
        for data in option_data:
            option.append({"id": data.kode_peternakan, "value": data.nama_peternakan})

        return option