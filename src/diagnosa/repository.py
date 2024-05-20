# ============================================
#                                           
#   Project Name :  be_sistem_pakar               
#   -------------------------------------   
#   Create by    : hexa at 27/04/24       
#   Copyright © 2024 Delameta Bilano     
#                                           
# ============================================
from sqlalchemy.orm import Session

from src.schema import RiwayatDiagnosa


class RepoDempsterShafer:

    def __init__(self, db: Session):
        self.db = db


    async def save_diagnose(self, data: dict):
        # TODO
        data = RiwayatDiagnosa(**data)
        try:
            self.db.add(data)
            self.db.flush()
            self.db.commit()
            return True, "Success to create diagnose", data.kode_riwayat
        except Exception as e:
            self.db.rollback()
            return False, f"Failed to save diagnose {e}", None

