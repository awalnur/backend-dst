# ============================================
#                                           
#   Project Name :  be_sistem_pakar               
#   -------------------------------------   
#   Create by    : hexa at 17/03/24       
#   Copyright © 2024 Delameta Bilano     
#                                           
# ============================================
from sqlalchemy.orm import Session

from src.rule.model import addRule, updateRule
from src.rule.repository import RepoRule


class RuleService:
    def __init__(self, db: Session):
        self.db = db

    async def create_new_rule(self, data:addRule):
        repo = RepoRule(db=self.db)
        kode_penyakit= data.kode_penyakit
        fail = []
        success = []
        for gejala in data.gejala:
            kode_gejala = gejala.kode_gejala
            create, message, code = await repo.create_rule(data={'kode_penyakit':kode_penyakit, 'kode_gejala':kode_gejala, 'belief': gejala.bobot})
            if not create:
                fail.append({'kode_gejala': kode_gejala, 'message': message})
            if create:
                success.append({'kode_gejala': kode_gejala, 'message': message})
        return {'success': success, 'fail': fail}, 'rule created'

    async def update_rule(self, kode_penyakit, data:updateRule):
        repo = RepoRule(db=self.db)
        updated = []
        deleted = []
        for update_data in data.update:
            update, message, code = await repo.update_rule(kode_penyakit, update_data.kode_gejala, bobot=update_data.bobot)
            if update:
                updated.append({'kode_gejala': update_data.kode_gejala, 'message': message, 'status': 'update successfully'})
            else:
                updated.append(
                    {'kode_gejala': update_data.kode_gejala, 'message': message, 'status': 'update failed'})
        for delete_data in data.delete:
            delete, message, code = await repo.delete_rule(kode_penyakit, delete_data.kode_gejala)
            if delete:
                deleted.append({'kode_gejala': delete_data.kode_gejala, 'message': message, 'status': 'delete successfully'})
            else:
                deleted.append(
                    {'kode_gejala': delete_data.kode_gejala, 'message': message, 'status': 'delete failed'})
        updated_resp = {'updated': updated, 'deleted': deleted}
        return updated_resp,'Updated Success', 200


    async def delete_rule(self, kode_penyakit: str):
        repo = RepoRule(db=self.db)
        delete, message, code = await repo.delete_rule_by_penyakit(kode_penyakit)
        return delete, message, code


    async def get_all_rule(self, limit: int = 0, offset: int = 0, searchBy: str = "", search: str = "", order: str = None, by: str = ""):
        repo = RepoRule(db=self.db)
        return await repo.get_all_rule(limit, offset, searchBy, search, order, by)