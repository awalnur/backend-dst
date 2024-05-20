# ============================================
#                                           
#   Project Name :  be_sistem_pakar               
#   -------------------------------------   
#   Create by    : hexa at 23/04/24       
#   Copyright © 2024 Delameta Bilano     
#                                           
# ============================================
from sqlalchemy import and_

from src.schema import DetailPengguna


class RepoFarm:

    def __init__(self, db):
        self.db = db

    async def get_all_farm(self, kode_pengguna: str = None, limit: int = 110, offset: int = 0, searchBy: str = "", search: str = "",
                           order: str = "nama_peternakan", by: str = "asc"):
        query = self.db.query(DetailPengguna).filter(DetailPengguna.kode_user == kode_pengguna)
        #
        # if searchBy and search:
        #     if searchBy == "kode_peternakan":
        #         query = query.filter(DetailPengguna.id == search)
        #     elif searchBy == "name":
        #         query = query.filter(DetailPengguna.name.like(f"%{search}%"))
        #     elif searchBy == "email":
        #         query = query.filter(DetailPengguna.email.like(f"%{search}%"))
        #     elif searchBy == "phone":
        #         query = query.filter(DetailPengguna.phone.like(f"%{search}%"))
        #     elif searchBy == "address":
        #         query = query.filter(DetailPengguna.address.like(f"%{search}%"))
        if by == "desc":
            by = "desc"
        else:
            by = "asc"
        print(order)

        res = query.order_by(
            getattr(DetailPengguna, order).asc() if by == "asc" else getattr(DetailPengguna, order).desc()).all()

        return res

    async def option_farm(self, kode_user: str):
        res = self.db.query(DetailPengguna.kode_peternakan, DetailPengguna.nama_peternakan).filter(
            DetailPengguna.kode_user == kode_user).all()
        return res

    async def create_farm(self, data):
        farm_data = DetailPengguna(**data)
        check_data = self.db.query(DetailPengguna).filter(and_(DetailPengguna.kode_user == farm_data.kode_user, DetailPengguna.nama_peternakan==farm_data.nama_peternakan, DetailPengguna.alamat_peternakan==farm_data.alamat_peternakan)).first()
        if check_data is not None:
            return False, "Farm data already exist"

        try:
            query = self.db.add(farm_data)
            self.db.flush()
            self.db.commit()
            return True, "Success to create farm"
        except Exception as e:
            self.db.rollback()
            print(e)
            return False, f"Failed to create farm {e}"
        # return 0

    async def update_farm(self, id, data, kode_user):
        farm_data = self.db.query(DetailPengguna).filter(and_(DetailPengguna.kode_peternakan == id, DetailPengguna.kode_user == kode_user)).first()
        if farm_data is None:
            return False, "Farm data not found", None

        farm_data.nama_peternakan=data['nama_peternakan']
        farm_data.alamat_peternakan=data['alamat_peternakan']
        try:
            self.db.commit()
            return True, "Farm data has been updated", data
        except Exception as e:
            self.db.rollback()
            print(e)
            return False, f"Failed to create farm {e}", None



        # return 0

    async def delete_farm(self, id, kode_user):
        farm_data = self.db.query(DetailPengguna).filter(and_(DetailPengguna.kode_peternakan == id, DetailPengguna.kode_user == kode_user)).first()
        if farm_data is None:
            return False, "Farm data not found"
        try:
            self.db.delete(farm_data)
            self.db.commit()
            return True, "Success to delete farm"
        except Exception as e:
            self.db.rollback()
            print(e)
            return False, f"Failed to delete farm {e}"
        return 0
