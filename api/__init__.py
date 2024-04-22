# ============================================
#                                           
#   Project Name :  be_sistem_pakar               
#   -------------------------------------   
#   Create by    : hexa at 26/02/24       
#   Copyright © 2024 Delameta Bilano     
#                                           
# ============================================
from fastapi import APIRouter

from api.v1.authentication import auth
from api.v1.diagnose import diagnose
from api.v1.gejala import router_gejala
from api.v1.penyakit import router_penyakit
from api.v1.user import router as router_user
from api.v1.rule import router_rule

v1_router = APIRouter(prefix='/api/v1')
v1_router.include_router(auth)
v1_router.include_router(router_user)
v1_router.include_router(diagnose)

v1_router.include_router(router_penyakit)

v1_router.include_router(router_gejala)
v1_router.include_router(router_rule)