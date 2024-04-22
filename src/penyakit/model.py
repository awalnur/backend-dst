# ============================================
#                                           
#   Project Name :  be_sistem_pakar               
#   -------------------------------------   
#   Create by    : hexa at 10/03/24       
#   Copyright © 2024 Delameta Bilano     
#                                           
# ============================================
from typing import List

from pydantic import BaseModel, Field


class ModelPenyakit(BaseModel):
    kode_penyakit: str = Field(max_length=3)
    nama_penyakit: str
    definisi: str
    penyebab: str
    penularan: str
    pencegahan: str
    penanganan: str
    gambar: str | None = None

class UpdatePenyakit(BaseModel):
    nama_penyakit: str= Field(default=None)
    definisi: str= Field(default=None)
    penyebab: str= Field(default=None)
    penularan: str= Field(default=None)
    pencegahan: str= Field(default=None)
    penanganan: str= Field(default=None)
    gambar: str= Field(default=None)


class AllPenyakit(BaseModel):
    data: List[ModelPenyakit]