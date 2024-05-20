# ============================================
#                                           
#   Project Name :  be_sistem_pakar               
#   -------------------------------------   
#   Create by    : hexa at 23/04/24       
#   Copyright © 2024 Delameta Bilano     
#                                           
# ============================================
import uuid

from pydantic import BaseModel


class FarmData(BaseModel):
    nama_peternakan: str
    alamat_peternakan: str

class FarmAll(BaseModel):
    kode_peternakan: int
    nama_peternakan: str
    alamat_peternakan: str
    user_id: str