# ============================================
#                                           
#   Project Name :  be_sistem_pakar               
#   -------------------------------------   
#   Create by    : hexa at 17/03/24       
#   Copyright © 2024 Delameta Bilano     
#                                           
# ============================================
from sqlalchemy import func, and_
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from src.schema import Rule, BasePenyakit, BaseGejala


class RepoRule:
    def __init__(self, db: Session):
        self.db = db

    def cek_rule(self, kode_penyakit, kode_gejala):
        rule = self.db.query(Rule).filter(Rule.kode_penyakit == kode_penyakit, Rule.kode_gejala == kode_gejala).first()
        return rule

    def cek_rule_by_penyakit(self, kode_penyakit):
        rule = self.db.query(Rule).filter(Rule.kode_penyakit == kode_penyakit).count()
        return rule
    async def get_list_penyakit(self, baypass=None):
        if baypass:
            data = self.db.query(BasePenyakit.kode_penyakit, BasePenyakit.nama_penyakit).outerjoin(Rule, BasePenyakit.kode_penyakit == Rule.kode_penyakit).filter(BasePenyakit.kode_penyakit!='00').group_by(BasePenyakit.kode_penyakit, BasePenyakit.nama_penyakit)
        else:
            data = self.db.query(BasePenyakit.kode_penyakit, BasePenyakit.nama_penyakit).outerjoin(Rule, BasePenyakit.kode_penyakit == Rule.kode_penyakit).filter(and_(Rule.kode_penyakit==None, BasePenyakit.kode_penyakit!='00')).group_by(BasePenyakit.kode_penyakit, BasePenyakit.nama_penyakit)

        resdata ={}
        entry = []
        for row in data:
            entry.append({
                'kode_penyakit': row.kode_penyakit,
                'penyakit': row.nama_penyakit,
            })
        resdata['entries'] = entry
        resdata['entries_total'] =len(entry)
        return resdata
    async def get_all_rule(self, limit: int = 0, offset: int = 0, searchBy: str = "", search: str = "", order: str = None, by: str = ""):
        data = self.db.query(Rule.kode_penyakit, BasePenyakit.nama_penyakit).join(BasePenyakit, Rule.kode_penyakit == BasePenyakit.kode_penyakit).group_by(Rule.kode_penyakit, BasePenyakit.kode_penyakit).order_by(Rule.kode_penyakit.asc())
        total_data = data.count()
        if searchBy and search:
            data = data.filter(getattr(BasePenyakit, searchBy).ilike(f'%{search}%'))
        if order:
            if by == "asc":
                data = data.order_by(getattr(Rule, order).asc())
            else:
                data = data.order_by(getattr(Rule, order).desc())
        if limit:
            data = data.limit(limit)
        if offset:
            if offset > 0:
                offset = (offset - 1) * limit
            else:
                offset = 0
            data = data.offset(offset)
        resdata= {}
        entry = []
        for row in data:
            list_gejala = []
            gejala = self.db.query(Rule.kode_penyakit, Rule.kode_gejala, Rule.belief, BasePenyakit.nama_penyakit, BaseGejala.gejala).join(BasePenyakit, Rule.kode_penyakit == BasePenyakit.kode_penyakit).join(BaseGejala, Rule.kode_gejala == BaseGejala.kode_gejala).order_by(Rule.kode_penyakit.asc()).filter(Rule.kode_penyakit == row.kode_penyakit)
            for row_gejala in gejala:
                list_gejala.append({
                    'kode_gejala': row_gejala.kode_gejala,
                    'gejala': row_gejala.gejala,
                    'bobot': row_gejala.belief
                })
            entry.append({
                'kode_penyakit': row.kode_penyakit,
                'penyakit': row.nama_penyakit,
                'gejala': list_gejala,
            })
        resdata['entries'] = entry
        resdata['entries_total']  =len(entry)
        resdata['data_total'] = total_data
        resdata['total_page'] = int(total_data / limit) + 1 if total_data % limit != 0 else int(total_data / limit)
        return resdata
    async def create_rule(self, data):
        rule = self.cek_rule(data['kode_penyakit'], data['kode_gejala'])
        if rule is not None:
            return False, "Failed to create rule, rule already exist", 422
        try:
            rule = Rule(**data)
            self.db.add(rule)
            self.db.commit()
            return True, "Success to create rule", 201
        except SQLAlchemyError as err:
            self.db.rollback()
            return False, f"Failed to create rule {err}", 400

    async def update_rule(self, kode_penyakit, kode_gejala, bobot):
        rule = self.cek_rule(kode_penyakit, kode_gejala)
        if rule is None:
            return False, "Failed to update rule, rule not found", 422
        try:
            rule.belief = bobot
            self.db.commit()
            return True, "Success to update rule", 200
        except SQLAlchemyError as err:
            self.db.rollback()
            return False, f"Failed to update rule {err}", 400
    async def delete_rule(self, kode_penyakit, kode_gejala):
        rule = self.cek_rule(kode_penyakit, kode_gejala)
        if rule is None:
            return False, "Failed to delete rule, rule not found", 422
        try:
            self.db.query(Rule).filter(Rule.kode_penyakit == kode_penyakit, Rule.kode_gejala == kode_gejala).delete()
            self.db.commit()
            return True, "Success to delete rule", 200
        except SQLAlchemyError as err:
            self.db.rollback()
            return False, f"Failed to delete rule {err}", 400

    async def delete_rule_by_penyakit(self, kode_penyakit):
        rule = self.cek_rule_by_penyakit(kode_penyakit)
        if rule < 1:
            return False, "Failed to delete rule, rule not found", 422
        try:
            self.db.query(Rule).filter(Rule.kode_penyakit == kode_penyakit).delete()
            self.db.commit()
            return True, "Success to delete rule", 200
        except SQLAlchemyError as err:
            self.db.rollback()
            return False, f"Failed to delete rule {err}", 400


    async def get_rule_by_id(self, kode_penyakit):
        rule = self.db.query(Rule).filter(Rule.kode_penyakit == kode_penyakit).all()
        if rule is None:
            return None
        return rule