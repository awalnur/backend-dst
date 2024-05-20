# ============================================
#                                           
#   Project Name :  be_sistem_pakar               
#   -------------------------------------   
#   Create by    : hexa at 28/04/24       
#   Copyright © 2024 Delameta Bilano     
#                                           
# ============================================
from sqlalchemy.orm import Session

from src.riwayat.repository import RepoRiwayat
from src.schema import RiwayatDiagnosa


class RiwayatService:

    def __init__(self, session: Session):
        self.session = session
        self.repo  = RepoRiwayat(self.session)

    async def get_all_riwayat(self, limit: int = 10, offset: int = 0, searchBy: str = "", search: str = "", order: str = "", by: str = "", user_id: str = None):
        try:
            data = []
            raw, total_data = await self.repo.get_all_riwayat(limit=limit, offset=offset, searchBy=searchBy, search=search, order=order, by=by, user_id=user_id)
            for raw_data in raw:
                data.append({
                    'number': (offset * limit) + raw.index(raw_data) + 1,
                    'kode_riwayat': raw_data.kode_riwayat,
                    'kode_penyakit': raw_data.kode_penyakit,
                    'total_gejala': len(raw_data.kode_gejala),
                    'kesimpulan': raw_data.kesimpulan,
                    'username': raw_data.username if raw_data.username is not None else "Anonymous",
                    'peternakan': raw_data.nama_peternakan,
                    'penyakit': raw_data.nama_penyakit,
                    'created_date': str(raw_data.created_at),
                    'persentase': f'{(raw_data.persentase*100):.2f}'
                })
            resp = {
                'entries': data,
                'entries_total': len(raw),
                'data_total': total_data,
                'total_page': int(total_data / limit) + 1 if total_data % limit != 0 else int(total_data / limit),

            }
            return resp
        except Exception as e:
            print(f"error when get all riwayat, detail{e}")
            return None

    async def get_last_riwayat(self, kode_user: str):
        try:
            data = await self.repo.get_last_riwayat(kode_user=kode_user)
            entries = []
            for raw_data in data:
                entries.append({
                    'kode_riwayat': raw_data.kode_riwayat,
                    'persentase': f'{(raw_data.persentase*100):.2f}',
                    'penyakit': raw_data.nama_penyakit,
                    'peternakan': raw_data.nama_peternakan,
                    'kesimpulan': raw_data.kesimpulan,
                    'created_date': raw_data.created_at.strftime("%d-%m-%Y %H:%M:%S")
                })
            res = {
                'entries': entries
            }
            print(res)
            return res
        except Exception as e:
            print(f"error when get last riwayat, detail {e}")
            return None


    async def delete_riwayat(self, kode_riwayat, kode_user: str):
        try:
            delete, message = await self.repo.delete_riwayat(kode_riwayat=kode_riwayat, kode_user=kode_user)
            return delete, message
        except Exception as e:
            print(e)
            return False, "Failed to delete riwayat"