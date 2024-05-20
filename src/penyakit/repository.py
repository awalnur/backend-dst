# ============================================
#                                           
#   Project Name :  be_sistem_pakar               
#   -------------------------------------   
#   Create by    : hexa at 10/03/24       
#   Copyright © 2024 Delameta Bilano     
#                                           
# ============================================
import datetime
from typing import List

from fastapi import HTTPException
from redis import Redis
from sqlalchemy import func
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy.orm import Session

from src.penyakit.model import AllPenyakit, UpdatePenyakit
from src.schema import BaseGejala, BasePenyakit, RiwayatDiagnosa


class RepoPenyakit:
    def __init__(self, db: Session, redis:Redis=None):
        self.db = db
        self.redis = redis


    async def get_all_penyakit(self, limit: int = 0, offset: int = 0, searchBy: str = "", search: str = "", order: str = None, by: str = ""):
        data = self.db.query(
            BasePenyakit.kode_penyakit,
            BasePenyakit.nama_penyakit,
            BasePenyakit.definisi,
            BasePenyakit.penyebab,
            BasePenyakit.penularan,
            BasePenyakit.pencegahan,
            BasePenyakit.penanganan,
            BasePenyakit.gambar,
            BasePenyakit.created_at,
            BasePenyakit.updated_at
        )
        data = data.filter(BasePenyakit.kode_penyakit!='00')
        count_all = data.count()
        if searchBy and search:
            print(getattr(BasePenyakit, searchBy))
            data = data.filter(getattr(BasePenyakit, searchBy).ilike(f'%{search}%'))
            print(data)
        if order:
            if by == "asc":
                data = data.order_by(getattr(BasePenyakit, order).asc())
            else:
                data = data.order_by(getattr(BasePenyakit, order).desc())
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
        resdata = []
        for row in all_data:
            resdata.append(
                {
                    "kode_penyakit": row.kode_penyakit,
                    "nama_penyakit": row.nama_penyakit,
                    "definisi": row.definisi,
                    "penyebab": row.penyebab,
                    "penularan": row.penularan,
                    "pencegahan": row.pencegahan,
                    "penanganan": row.penanganan,
                    "gambar": row.gambar,
                }
            )
        return resdata, count_all
    async def get_penyakit_by_id(self, kode_penyakit: str):
        data = self.db.query(
            BasePenyakit.kode_penyakit,
        BasePenyakit.nama_penyakit,
        BasePenyakit.definisi,
        BasePenyakit.penyebab,
        BasePenyakit.penularan,
        BasePenyakit.pencegahan,
        BasePenyakit.penanganan,
        BasePenyakit.gambar,
        BasePenyakit.created_at,
        BasePenyakit.updated_at
        ).filter(BasePenyakit.kode_penyakit == kode_penyakit).first()
        return data
    async def update_penyakit_by_id(self, kode_penyakit: str, **kwargs):
        # print(**kwargs)
        data_penyakit = self.db.query(BasePenyakit).filter(BasePenyakit.kode_penyakit == kode_penyakit).first()
        try:

            if kwargs.get('nama_penyakit') is not None:
                data_penyakit.nama_penyakit = kwargs.get('nama_penyakit')
            if kwargs.get('definisi') is not None:
                data_penyakit.definisi = kwargs.get('definisi')
            if kwargs.get('penyebab') is not None:
                data_penyakit.penyebab = kwargs.get('penyebab')
            if kwargs.get('penularan') is not None:
                data_penyakit.penularan = kwargs.get('penularan')
            if kwargs.get('pencegahan') is not None:
                data_penyakit.pencegahan = kwargs.get('pencegahan')
            if kwargs.get('penanganan') is not None:
                data_penyakit.penanganan = kwargs.get('penanganan')
            if kwargs.get('gambar') is not None:
                data_penyakit.gambar = kwargs.get('gambar')

            data_penyakit.updated_at = datetime.datetime.now()

            self.db.commit()
            return True, "Success to update penyakit"
        except (SQLAlchemyError, IntegrityError):
            self.db.rollback()
            return False, "Failed to update penyakit"

    async def delete_penyakit_by_id(self, kode_penyakit: str):
        cek_penyakit =await self.get_penyakit_by_id(kode_penyakit=kode_penyakit)
        if cek_penyakit is None:
            return False, "Failed to delete penyakit"
        try:
            self.db.query(BasePenyakit).filter(BasePenyakit.kode_penyakit == kode_penyakit).delete()
            self.db.commit()
            return True, "Success to delete penyakit"
        except (SQLAlchemyError, IntegrityError):
            self.db.rollback()
            return False, "Failed to delete penyakit"

    async def create_penyakit(self, data: BasePenyakit):
        try:
            self.db.add(data)
            self.db.commit()
            return True, "Success to create penyakit"
        except Exception as e:
            self.db.rollback()
            return False, f"Failed to create penyakit {e}"


    async def option(self):
        data_penyakit = self.db.query(BasePenyakit.kode_penyakit, BasePenyakit.nama_penyakit).filter(BasePenyakit.kode_penyakit!='00').order_by(BasePenyakit.kode_penyakit.asc()).all()
        return data_penyakit

    async def most_desease(self):
        data = self.db.query(BasePenyakit.kode_penyakit, BasePenyakit.nama_penyakit, BasePenyakit.gambar, BasePenyakit.definisi, func.count(RiwayatDiagnosa.kode_penyakit)).join(RiwayatDiagnosa, BasePenyakit.kode_penyakit == RiwayatDiagnosa.kode_penyakit).filter(BasePenyakit.kode_penyakit!='00').group_by(RiwayatDiagnosa.kode_penyakit, BasePenyakit.kode_penyakit).order_by(func.count(BasePenyakit.kode_penyakit).desc()).limit(3).all()
        return data