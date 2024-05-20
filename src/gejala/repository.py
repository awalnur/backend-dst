# ============================================
#                                           
#   Project Name :  be_sistem_pakar               
#   -------------------------------------   
#   Create by    : hexa at 14/03/24       
#   Copyright © 2024 Delameta Bilano     
#                                           
# ============================================
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

from src.gejala.model import ModelGejala
from src.schema import BaseGejala


class RepoGejala:

    def __init__(self, db: Session):
        self.db = db


    async def get_gejala_by_id(self, kode_gejala):
        return self.db.query(BaseGejala).filter(BaseGejala.kode_gejala == kode_gejala).first()


    async def insert_gejala(self, data: BaseGejala):
        cek_gejala =await self.get_gejala_by_id(kode_gejala=data.kode_gejala)
        if cek_gejala is not None:
            return False, "Failed to create gejala, gejala already exist", 422
        try:
            self.db.add(data)
            self.db.commit()
            return True, "Success to create gejala", 201
        except Exception as e:
            self.db.rollback()
            return False, f"Failed to create gejala {e}", 400

    async def update_gejala(self, kode_gejala: str, **kwargs):
        cek_gejala =await self.get_gejala_by_id(kode_gejala=kode_gejala)
        try:
            if cek_gejala is None:
                return False, "Failed to update gejala or gejala not found"
            cek_gejala.gejala = kwargs.get('gejala')
            self.db.commit()
            return True, "Success to update gejala"
        except Exception as e:
            self.db.rollback()
            return False, f"Failed to update gejala {e}"

    async def delete_gejala_by_id(self, kode_gejala: str):
        cek_gejala =await self.get_gejala_by_id(kode_gejala=kode_gejala)
        if cek_gejala is None:
            return False, "Failed to delete gejala", 422

        try:
            self.db.query(BaseGejala).filter(BaseGejala.kode_gejala == kode_gejala).delete()
            self.db.commit()
            return True, "Success to delete gejala", 200
        except (SQLAlchemyError, IntegrityError):
            self.db.rollback()
            return False, "Failed to delete gejala", 400


    async def get_all_gejala(self, limit: int = 10, offset: int = 0, searchBy: str = "", search: str = "", order: str = "", by: str = ""):
        data = self.db.query(BaseGejala)
        total_data = data.count()
        if searchBy and search:
            print(getattr(BaseGejala, searchBy))
            data = data.filter(getattr(BaseGejala, searchBy).ilike(f'%{search}%'))
        if order:
            if by == "asc":
                data = data.order_by(getattr(BaseGejala, order).asc())
            else:
                data = data.order_by(getattr(BaseGejala, order).desc())
        if limit:
            data = data.limit(limit)
        if offset:
            if offset > 0:
                offset = (offset - 1) * limit
            else:
                offset = 0
            data = data.offset(offset)

        all_data = data.all()
        # penyakit_dicts = [row.dict() for row in all_data]\
        if limit==1000:
            resdata = []
            for row in all_data:
                resdata.append(
                    {
                        "kode_gejala": row.kode_gejala,
                        "gejala": row.gejala,
                    }
                )
        else:
            resdata = {}
            entries = []
            for row in all_data:
                entries.append(
                    {
                        "kode_gejala": row.kode_gejala,
                        "gejala": row.gejala,

                    }
                )
            resdata={
                "entries": entries,
                 'entries_total': len(entries),
                'data_total': total_data,
                'total_page': int(total_data / limit) + 1 if total_data % limit != 0 else int(total_data / limit),
            }
        return resdata