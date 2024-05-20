# ============================================
#                                           
#   Project Name :  be_sistem_pakar               
#   -------------------------------------   
#   Create by    : hexa at 17/03/24       
#   Copyright © 2024 Delameta Bilano     
#                                           
# ============================================
from sqlalchemy.orm import Session

from src.penyakit.repository import RepoPenyakit
from src.rule.model import addRule, updateRule
from src.rule.repository import RepoRule


class RuleService:
    def __init__(self, db: Session):
        self.db = db

    async def create_new_rule(self, data:addRule):
        repo = RepoRule(db=self.db)
        kode_penyakit= data.kode_penyakit.upper()
        fail = []
        success = []
        for gejala in data.gejala:
            kode_gejala = gejala.kode_gejala
            create, message, code = await repo.create_rule(data={'kode_penyakit':kode_penyakit, 'kode_gejala':kode_gejala.upper(), 'belief': gejala.bobot})
            if not create:
                fail.append({'kode_gejala': kode_gejala, 'message': message})
            if create:
                success.append({'kode_gejala': kode_gejala, 'message': message})
        return {'success': success, 'fail': fail}, 'rule created'

    async def update_rule(self, kode_penyakit, data:updateRule):
        repo = RepoRule(db=self.db)

        all_rule = await repo.get_rule_by_id(kode_penyakit)
        x = []
        success = []
        fail = []
        for data_db in all_rule:
            if data_db.kode_gejala not in [gejala.kode_gejala for gejala in data.gejala]:
                deleted, message, code = await repo.delete_rule(kode_penyakit, data_db.kode_gejala)
                if not deleted:
                    fail.append({'kode_gejala': data_db.kode_gejala, 'message': message})
                if deleted:
                    success.append({'kode_gejala': data_db.kode_gejala, 'message': message})

        for gejala in data.gejala:
            check = repo.cek_rule(kode_penyakit, gejala.kode_gejala)
            if check is None:
                create, message, code = await repo.create_rule(data={'kode_penyakit':kode_penyakit, 'kode_gejala':gejala.kode_gejala.upper(), 'belief': gejala.bobot})
                if not create:
                    fail.append({'kode_gejala': gejala.kode_gejala, 'message': message})
                if create:
                    success.append({'kode_gejala': gejala.kode_gejala, 'message': message})
            else:
                updated, message, code = await repo.update_rule(kode_penyakit, gejala.kode_gejala, gejala.bobot)
                if not updated:
                    fail.append({'kode_gejala': gejala.kode_gejala, 'message': message})
                if updated:
                    success.append({'kode_gejala': gejala.kode_gejala, 'message': message})
        #     updated, deleted, message, code = await repo.update_rule(kode_penyakit, kode_gejala, **gejala.bobot)
        updated_resp = {'success': success, 'fail': fail}
        return updated_resp,'Updated Success', 200


    async def delete_rule(self, kode_penyakit: str):
        repo = RepoRule(db=self.db)
        delete, message, code = await repo.delete_rule_by_penyakit(kode_penyakit)
        return delete, message, code


    async def get_all_rule(self, limit: int = 0, offset: int = 0, searchBy: str = "", search: str = "", order: str = None, by: str = ""):
        repo = RepoRule(db=self.db)
        return await repo.get_all_rule(limit, offset, searchBy, search, order, by)

    async def get_rule_by_id(self, kode_penyakit: str):
        repo = RepoRule(db=self.db)
        rule= await repo.get_rule_by_id(kode_penyakit)

        getdata= await RepoPenyakit(db=self.db).get_penyakit_by_id(kode_penyakit.upper())
        if rule:
            gejala = {}
            bobot = {}
            i=0
            for row in rule:
                gejala[i] = row.kode_gejala
                bobot[f'bobot[{i}]'] = row.belief
                i+=1
            data = {'kode_penyakit': kode_penyakit, 'nama_penyakit':getdata.nama_penyakit,'gejala': gejala, 'bobot': bobot }
            return data

    async def get_list_penyakit(self, baypass=None):
        repo = RepoRule(db=self.db)
        return await repo.get_list_penyakit(baypass=baypass)