# ============================================
#                                           
#   Project Name :  be_sistem_pakar               
#   -------------------------------------   
#   Create by    : hexa at 28/04/24       
#   Copyright © 2024 Delameta Bilano     
#                                           
# ============================================
from sqlalchemy import and_, func

from src.schema import RiwayatDiagnosa, DetailPengguna, BasePenyakit, Users


class RepoRiwayat:
    def __init__(self, db):
        self.db = db

    async def get_all_riwayat(self, limit: int = 10, offset: int = 0, searchBy: str = "", search: str = "",
                              order: str = "", by: str = "DESC", user_id: str = None):
        query = self.db.query(RiwayatDiagnosa.kode_riwayat, RiwayatDiagnosa.persentase, RiwayatDiagnosa.kode_gejala,
                              RiwayatDiagnosa.kode_penyakit, RiwayatDiagnosa.kesimpulan, DetailPengguna.nama_peternakan,
                              RiwayatDiagnosa.created_at, BasePenyakit.nama_penyakit, BasePenyakit.kode_penyakit,
                              Users.username).join(Users, Users.kode_user == RiwayatDiagnosa.kode_user,
                                                   isouter=True).join(DetailPengguna,
                                                                      DetailPengguna.kode_peternakan == RiwayatDiagnosa.kode_peternakan,
                                                                      isouter=True).join(BasePenyakit,
                                                                                         BasePenyakit.kode_penyakit == RiwayatDiagnosa.kode_penyakit,
                                                                                         isouter=True)
        if searchBy and search:
            if searchBy == "kode_penyakit":
                query = query.filter(RiwayatDiagnosa.kode_penyakit.ilike(f"%{search}%"))
            if searchBy == "nama_penyakit":
                query = query.filter(BasePenyakit.nama_penyakit.ilike(f"%{search}%"))
            if searchBy == "kode_user":
                query = query.filter(RiwayatDiagnosa.kode_user.ilike(f"%{search}%"))
            if searchBy == "username":
                query = query.filter(Users.username.ilike(f"%{search}%"))

            if searchBy == "kesimpulan":
                query = query.filter(RiwayatDiagnosa.kesimpulan.ilike(f"%{search}%"))
        if order == "":
            query = query.order_by(RiwayatDiagnosa.created_at.desc())
        if order and by:
            if order == "":
                query = query.order_by(RiwayatDiagnosa.created_at.desc())
            else:

                if by.lower() == "desc":
                    by = "desc"
                else:
                    by = "asc"
                query = query.order_by(
                    getattr(RiwayatDiagnosa, order).asc() if by == "asc" else getattr(RiwayatDiagnosa, order).desc())

        if user_id is not None:
            query = query.filter(RiwayatDiagnosa.kode_user == user_id)
        total_data = query.count()
        res = query.offset(offset * limit).limit(limit).all()
        return res, total_data

    async def get_last_riwayat(self, kode_user: str):
        data = self.db.query(
            RiwayatDiagnosa.kode_riwayat,
            RiwayatDiagnosa.persentase,
            RiwayatDiagnosa.kesimpulan,
            DetailPengguna.nama_peternakan,
            RiwayatDiagnosa.created_at,
            BasePenyakit.nama_penyakit,
        ).join(DetailPengguna, DetailPengguna.kode_peternakan == RiwayatDiagnosa.kode_peternakan).join(BasePenyakit,
                                                                                                       BasePenyakit.kode_penyakit == RiwayatDiagnosa.kode_penyakit).filter(
            RiwayatDiagnosa.kode_user == kode_user).order_by(RiwayatDiagnosa.created_at.desc()).offset(0).limit(3).all()
        return data

    async def check_riwayat(self, kode_riwayat, kode_user: str):
        data = self.db.query(RiwayatDiagnosa).filter(
            and_(RiwayatDiagnosa.kode_riwayat == kode_riwayat, RiwayatDiagnosa.kode_user == kode_user)).first()
        return data

    async def delete_riwayat(self, kode_riwayat, kode_user: str):
        riwayat = self.check_riwayat(kode_riwayat, kode_user)
        if riwayat is None:
            return False, "Failed to delete riwayat or Riwayat not found"
        try:
            delete = self.db.query(RiwayatDiagnosa).filter(
                and_(RiwayatDiagnosa.kode_riwayat == kode_riwayat, RiwayatDiagnosa.kode_user == kode_user)).delete()
            self.db.commit()
            return True, "Success to delete riwayat"
        except Exception as e:
            print(e)
            return False, "Failed to delete riwayat"

    async def delete_by_userid(self, kode_user: str):
        try:
            self.db.query(RiwayatDiagnosa).filter(and_(RiwayatDiagnosa.kode_user == kode_user)).delete()
            self.db.commit()
            return True, "Success to delete riwayat"
        except Exception as e:
            print(e)
            return False, "Failed to delete riwayat"

    async def get_penyakit_by_riwayat(self):
        penyakit = self.db.query(RiwayatDiagnosa.kode_penyakit, BasePenyakit.nama_penyakit).join(BasePenyakit,
                                                                                                 BasePenyakit.kode_penyakit == RiwayatDiagnosa.kode_penyakit).group_by(
            RiwayatDiagnosa.kode_penyakit, BasePenyakit.nama_penyakit).filter(
            RiwayatDiagnosa.kode_penyakit != '00').all()
        data = self.db.query(RiwayatDiagnosa.kode_penyakit, BasePenyakit.nama_penyakit,
                             func.to_char(RiwayatDiagnosa.created_at, 'YYYY-MM-DD').label('tanggal'),
                             func.count(RiwayatDiagnosa.kode_penyakit).label('total_data')).join(BasePenyakit,
                                                                             BasePenyakit.kode_penyakit == RiwayatDiagnosa.kode_penyakit).group_by(
            RiwayatDiagnosa.kode_penyakit, func.to_char(RiwayatDiagnosa.created_at, 'YYYY-MM-DD').label('tanggal'),
            BasePenyakit.nama_penyakit).filter(RiwayatDiagnosa.kode_penyakit != '00').all()
        return penyakit, data
    async def get_count_all(self):
        count = self.db.query(func.count(RiwayatDiagnosa.kode_riwayat).label('total_diagnosa')).first()
        return count.total_diagnosa