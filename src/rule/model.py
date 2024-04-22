# ============================================
#                                           
#   Project Name :  be_sistem_pakar               
#   -------------------------------------   
#   Create by    : hexa at 17/03/24       
#   Copyright © 2024 Delameta Bilano     
#                                           
# ============================================
from pydantic import BaseModel


class kodeGejala(BaseModel):
    kode_gejala: str

class ruleGejala(kodeGejala):
    bobot: float


class addRule(BaseModel):
    kode_penyakit: str
    gejala: list[ruleGejala]


class updateRule(BaseModel):
    update: list[ruleGejala]
    delete: list[kodeGejala]
