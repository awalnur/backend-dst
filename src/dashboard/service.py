# ============================================
#                                           
#   Project Name :  be_sistem_pakar               
#   -------------------------------------   
#   Create by    : hexa at 19/05/24       
#   Copyright © 2024 Delameta Bilano     
#                                           
# ============================================
import random
from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from src.riwayat.repository import RepoRiwayat
from src.schema import Users, BasePenyakit, BaseGejala


class AdminService:

    def __init__(self, db: Session):
        self.db = db

    async def get_dashboard(self):

        repoRiwayat = RepoRiwayat(self.db)
        total_diagnosa = await repoRiwayat.get_count_all()
        penyakit, data_riwayat = await repoRiwayat.get_penyakit_by_riwayat()


        total_pengguna = self.db.query(Users).count()
        total_penyakit = self.db.query(BasePenyakit).filter(BasePenyakit.kode_penyakit!='00').count()
        total_gejala = self.db.query(BaseGejala).count()
        # Get today's date
        today = datetime.today()

        # List the date 30 days ago
        date_list = [(today - timedelta(days=x)).strftime('%Y-%m-%d') for x in range(30, -1, -1)]

            # for data in penyakit:
        entry = []
        for dpenyakit in penyakit:
            hue = random.randint(0, 360)
            saturation = random.randint(0, 100)
            lightness = random.randint(0, 100)

            # Format as an HSL string
            random_hsl_color = f'hsl({hue}, {saturation}%, {lightness}%)'

            data_pnyakit = {
                    "id": dpenyakit.nama_penyakit,
                    "color": random_hsl_color,
                    "data": []
                    }
            for date in date_list:
                data = {
                    "x": date,
                    "y": 0
                }
                for riwayat in data_riwayat:
                    if riwayat.tanggal == str(date) and riwayat.kode_penyakit == dpenyakit.kode_penyakit:
                        data["y"]= riwayat.total_data

                data_pnyakit['data'].append(data)


            entry.append(data_pnyakit)


        res = {
            'entries': entry,
            'total_diagnosa': total_diagnosa,
            'total_pengguna':total_pengguna,
            'total_penyakit':total_penyakit,
            'total_gejala':total_gejala
        }
        return res

