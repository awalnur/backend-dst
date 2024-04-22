# ============================================
#                                           
#   Project Name :  be_sistem_pakar               
#   -------------------------------------   
#   Create by    : hexa at 10/03/24       
#   Copyright © 2024 Delameta Bilano     
#                                           
# ============================================
from pydantic import BaseModel, Field


class ModelGejala(BaseModel):
    kode_gejala: str =Field(max_length=3)
    gejala: str


class ModelUpdateGejala(BaseModel):
    gejala: str