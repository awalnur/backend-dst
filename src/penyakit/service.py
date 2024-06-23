# ============================================
#                                           
#   Project Name :  be_sistem_pakar               
#   -------------------------------------   
#   Create by    : hexa at 10/03/24       
#   Copyright © 2024 Delameta Bilano     
#                                           
# ============================================
import os
import shutil

from fastapi import HTTPException, UploadFile
from redis import Redis
from sqlalchemy.orm import Session

from src.penyakit.model import ModelPenyakit, UpdatePenyakit
from src.penyakit.repository import RepoPenyakit
from src.schema import BasePenyakit


class Penyakit:
    def __init__(self, db: Session, redis:Redis=None):
        self.db = db
        self.redis = redis
        self.upload_folder = "uploads"


    async def get_data_penyakit_by_id(self, kode_penyakit: str):
        repo = RepoPenyakit(db=self.db, redis=self.redis)
        try:
            data = await repo.get_penyakit_by_id(kode_penyakit=kode_penyakit)
        except Exception as e:
            print(f"error when get penyakit by id, detail{e}")
            data = None

        return data

    async def get_option_penyakit(self):
        repo = RepoPenyakit(db=self.db, redis=self.redis)
        option_list = await repo.option()
        list_option = []
        for option in option_list:
            list_option.append({'id':option.kode_penyakit, 'value':option.nama_penyakit})
        return list_option
    async def get_all_penyakit(self, limit: int = 10, offset: int = 0, searchBy: str = "", search: str = "", order: str = "", by: str = ""):
        repo = RepoPenyakit(db=self.db, redis=self.redis)
        # try:
        data,total_data  = await repo.get_all_penyakit(limit=limit, offset=offset, searchBy=searchBy, search=search, order=order, by=by)
        # except Exception as e:
        #     print(f"error when get all penyakit, detail{e}")
        #     data = None
        return {
            'entries':data,
            'entries_total': len(data),
            'data_total': total_data,
            'total_page': int(total_data / limit) + 1 if total_data % limit != 0 else int(total_data / limit),
        }

    async def add_penyakit(self, gambar: UploadFile, **kwargs):
        repo = RepoPenyakit(db=self.db, redis=self.redis)
        check_penyakit = await repo.get_penyakit_by_id(kode_penyakit=kwargs['kode_penyakit'])
        if check_penyakit is not None:
            raise HTTPException(status_code=400, detail="Penyakit already exist")
        upload_folder = self.upload_folder

        # Create the upload folder if it doesn't exist
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)
        if gambar is not None:
            try:
                # Save the uploaded file
                filenames = gambar.filename.replace(' ', '_')
                file_path = os.path.join(kwargs['kode_penyakit']+filenames)
                with open(file_path, "wb") as buffer:
                    shutil.copyfileobj(gambar.file, buffer)
                    kwargs['gambar'] = file_path
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))
        try:
            data, m = await repo.create_penyakit(data=BasePenyakit(**kwargs))
            if data:
                return data
            raise HTTPException(status_code=400, detail=m)
        except Exception as e:
            print(f"error when add penyakit, detail{e}")
            raise HTTPException(status_code=400, detail='m')

    async def update_penyakit(self, kode_penyakit: str, **kwargs):
        repo = RepoPenyakit(db=self.db, redis=self.redis)
        cek_penyakit = await repo.get_penyakit_by_id(kode_penyakit=kode_penyakit)

        if cek_penyakit is None:
            raise HTTPException(status_code=404, detail="Penyakit not found")
        if kwargs.get('gambar') is not None:
            gambar= kwargs.get('gambar')
            try:
                # Save the uploaded file
                file_path = os.path.join(self.upload_folder, kode_penyakit+gambar.filename)
                with open(file_path, "wb") as buffer:
                    shutil.copyfileobj(gambar.file, buffer)
                    kwargs['gambar'] = kode_penyakit+gambar.filename
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))
        try:

            data, m = await repo.update_penyakit_by_id(kode_penyakit=kode_penyakit, **kwargs)

            print(m)
        except Exception as e:
            print(f"error when update penyakit, detail{e}")
            data = None
            # raise HTTPException(status_code=400, detail=m)
        return data

    async def delete_penyakit(self, kode_penyakit: str):
        repo = RepoPenyakit(db=self.db, redis=self.redis)
        try:
            data, m = await repo.delete_penyakit_by_id(kode_penyakit=kode_penyakit)
            return data
        except Exception as e:
            print(f"error when delete penyakit, detail{e}")
            raise HTTPException(status_code=400, detail=f"error when delete penyakit, detail{e}")
    async def most_desease(self):
        repo = RepoPenyakit(db=self.db, redis=self.redis)
        data = await repo.most_desease()
        if data is None:
            raise HTTPException(status_code=404, detail="Penyakit not found")

        entries = []
        for raw_data in data:
            entries.append({
                'kode_penyakit': raw_data.kode_penyakit,
                'nama_penyakit': raw_data.nama_penyakit,
                'definisi': raw_data.definisi,
                'gambar': raw_data.gambar
            })
        data = {
            'entries': entries,
            'total': len(entries)
        }
        return data
