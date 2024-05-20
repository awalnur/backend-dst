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
from api.v1.farm import farm_api as router_farm
from api.v1.riwayat import router as router_riwayat
from api.v1.assets import assets as router_assets
from api.v1.admin import admin as router_admin

v1_router = APIRouter(prefix='/api/v1')
v1_router.include_router(auth)
v1_router.include_router(router_user)
v1_router.include_router(diagnose)
v1_router.include_router(router_riwayat)

v1_router.include_router(router_penyakit)

v1_router.include_router(router_gejala)
v1_router.include_router(router_rule)

v1_router.include_router(router_farm)
v1_router.include_router(router_admin)

v1_router.include_router(router_assets)