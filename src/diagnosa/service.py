# ============================================
#                                           
#   Project Name :  be_sistem_pakar               
#   -------------------------------------   
#   Create by    : hexa at 02/04/24       
#   Copyright © 2024 Delameta Bilano     
#                                           
# ============================================
import json

from sqlalchemy import and_
from sqlalchemy.orm import Session

from src.diagnosa.repository import RepoDempsterShafer
from src.penyakit.repository import RepoPenyakit
from src.schema import Rule, RiwayatDiagnosa, BasePenyakit, BaseGejala, Users, DetailPengguna


class DempsterShafer:

    def __init__(self, session: Session):
        self.session = session
        self.repo = RepoDempsterShafer(session)
        self.penyakit = RepoPenyakit(session)

    def calculate_dempster_shafer(self, observations, belief_dict):
        # TODO
        m = []
        for keys in belief_dict:
            m3 = []
            m4 = []
            if len(m) == 0:
                m.append({'himpunan': belief_dict[keys]['m'], 'bel': belief_dict[keys]['bel']})
                theta = round(1 - belief_dict[keys]['bel'], 2)
                m.append({'himpunan': {'0'}, 'bel': theta})
            else:
                new_theta = round(1 - belief_dict[keys]['bel'], 2)
                for i in range(len(m)):
                    intersect = m[i]['himpunan'].intersection(belief_dict[keys]['m'])
                    if len(intersect) != 0 and m[i]['himpunan'] != {'0'}:
                        if m[i]['himpunan'] == m[i]['himpunan'].intersection(belief_dict[keys]['m']):
                            m3.append({'himpunan': m[i]['himpunan'], 'bel': m[i]['bel'] * belief_dict[keys]['bel']})
                            m3.append({'himpunan': m[i]['himpunan'], 'bel': m[i]['bel'] * new_theta})
                        else:
                            m3.append({'himpunan': intersect, 'bel': m[i]['bel'] * belief_dict[keys]['bel']})
                            m3.append({'himpunan': m[i]['himpunan'], 'bel': m[i]['bel'] * new_theta})
                    elif m[i]['himpunan'] == {'0'}:
                        m3.append({'himpunan': m[i]['himpunan'], 'bel': m[i]['bel'] * new_theta})
                        m3.append({'himpunan': belief_dict[keys]['m'], 'bel': m[i]['bel'] * belief_dict[keys]['bel']})
                    else:
                        m4.append({'himpunan': belief_dict[keys]['m'], 'bel': m[i]['bel'] * belief_dict[keys]['bel']})
                        m3.append({'himpunan': m[i]['himpunan'], 'bel': m[i]['bel'] * new_theta})
                sums = {}
                div = 1 - sum(entry['bel'] for entry in m4)

                # Aggregate sums
                for entry in m3:
                    himpunan = tuple(sorted(entry['himpunan']))
                    if himpunan in sums:
                        sums[himpunan] += entry['bel']
                    else:
                        sums[himpunan] = entry['bel']
                # Convert aggregated sums to list of dictionaries
                if div == 0:
                    result = [{'himpunan': set(himpunan), 'bel': 0} for himpunan, bel in sums.items()]
                    m = result
                else:
                    result = [{'himpunan': set(himpunan), 'bel': bel / div} for himpunan, bel in sums.items()]
                    m = result

        result = max(m, key=lambda x: x['bel'])
        res_m = sorted(m, key=lambda x: x['bel'], reverse=True)
        return result, res_m

    async def dempster_shafer(self, data: dict, user_id: str = None, farm_id: str = None):
        # TODO
        evidence = {}

        if len(data['gejala']) < 2:
            return 'Failed to calculate dempster shafer, data must be more than 1'
        for gejala in data['gejala']:
            rules = self.session.query(Rule).filter(Rule.kode_gejala == gejala).all()
            evidence[gejala] = {
                'm': {rule.kode_penyakit for rule in rules},
                'bel': round(sum([rule.belief for rule in rules]) / len(rules) if len(rules) > 0 else 1, 2)
            }

        sorted_evidence = dict(sorted(evidence.items(), key=lambda item: item[1]['m'], reverse=True))
        res, all = self.calculate_dempster_shafer(data, sorted_evidence)
        result = {'penyakit': '00', 'kesimpulan': 'Sistem tidak dapat mendeteksi jenis penyakit', 'bel': 0}

        # print(all, sorted_evidence)
        other = []
        for x in all:
            # print(len(x['himpunan']))
            if len(x['himpunan']) == 1:
                if list(x['himpunan'])[0]!='0':
                    res_penyakit = await self.penyakit.get_penyakit_by_id(kode_penyakit=list(x['himpunan'])[0])
                    other_item = {'penyakit':res_penyakit[1], 'bel': round(x['bel'],4)}
                    if list(res['himpunan'])[0] != list(x['himpunan'])[0]:
                        other.append(other_item)
                else:
                    other_item = {'penyakit':'Tidak ada penyakit', 'bel': round(x['bel'],4)}
                    if res['bel'] > 0.5:
                        other.append(other_item)
        if res['bel'] > 0.5:
            res_penyakit = await self.penyakit.get_penyakit_by_id(kode_penyakit=list(res['himpunan'])[0])
            result['penyakit'] = list(res['himpunan'])[0]
            result['bel'] = res['bel']
            result['kesimpulan'] = res_penyakit[1]

        if user_id is not None:
            data = {
                'kode_penyakit': result['penyakit'],
                'kode_gejala': data['gejala'],
                'kode_pengguna': user_id,
                'kode_peternakan': data['kode_peternakan'],
                'persentase': result['bel'],
                'kesimpulan': result['kesimpulan'],
                'other': json.dumps(other, default=list)
            }

        else:
            data = {
                'kode_penyakit': result['penyakit'],
                'kode_gejala': data['gejala'],
                'kode_pengguna': None,
                'kode_peternakan': None,
                'persentase': result['bel'],
                'kesimpulan': result['kesimpulan'],
                'other': json.dumps(other, default=list)
            }

        success, message, id = await self.save_diagnose(data=data)
        return success, message, id

    async def save_diagnose(self, data: dict):
        # TODO
        insert_data = {
            'kode_penyakit': data['kode_penyakit'],
            'kode_gejala': data['kode_gejala'],
            'kode_user': data['kode_pengguna'],
            'kode_peternakan': data['kode_peternakan'],
            'persentase': data['persentase'],
            'kesimpulan': data['kesimpulan'],
            'other': data['other'] if 'other' in data else ''
        }

        success, message, id = await self.repo.save_diagnose(data=insert_data)
        print(success, message)
        return success, message, id

    async def get_diagnose_by_id(self, id: int, kode_user: str = None, admin=False):
        if admin is True:
            filter = and_(RiwayatDiagnosa.kode_riwayat == id)
        else:
            if kode_user is not None:
                filter = and_(RiwayatDiagnosa.kode_riwayat == id, RiwayatDiagnosa.kode_user == kode_user)
            else:
                filter = and_(RiwayatDiagnosa.kode_riwayat == id, RiwayatDiagnosa.kode_user == None)
        data = self.session.query(
            RiwayatDiagnosa.kode_riwayat,
            RiwayatDiagnosa.kode_user,
            RiwayatDiagnosa.kode_peternakan,
            RiwayatDiagnosa.kode_gejala,
            RiwayatDiagnosa.persentase,
            RiwayatDiagnosa.kesimpulan,
            RiwayatDiagnosa.kode_penyakit,
            RiwayatDiagnosa.other,
            BasePenyakit
        ).join(BasePenyakit, BasePenyakit.kode_penyakit == RiwayatDiagnosa.kode_penyakit).filter(filter).first()
        if data:
            # Extract the fields from the query result
            (kode_riwayat, kode_user, kode_peternakan, kode_gejala, persentase, kesimpulan, kode_penyakit, other,
             base_penyakit) = data

            # Convert the BasePenyakit object to a dictionary
            base_penyakit_dict = base_penyakit.__dict__

            # Remove the "_sa_instance_state" key from the dictionary
            base_penyakit_dict.pop('_sa_instance_state', None)
            base_penyakit_dict.pop('created_at', None)
            base_penyakit_dict.pop('updated_at', None)
            data_gejala = self.session.query(BaseGejala.gejala).filter(
                BaseGejala.kode_gejala.in_(data.kode_gejala)).all()
            if admin:
                user_data = self.session.query(Users.username, Users.nama_depan, Users.nama_belakang).filter(
                    Users.kode_user == data.kode_user).first()
                farm_data = self.session.query(DetailPengguna.nama_peternakan, DetailPengguna.alamat_peternakan).filter(
                    DetailPengguna.kode_peternakan == data.kode_peternakan).first()

                if user_data:
                    nama_pengguna = f"{user_data.nama_depan} {user_data.nama_belakang}"
                else:
                    nama_pengguna = 'Anonim'
                if farm_data:
                    farm_nama = farm_data.nama_peternakan
                    farm_address = farm_data.alamat_peternakan
                else:
                    farm_nama = ''
                    farm_address = ''
                res_data = {
                    'kode_riwayat': data.kode_riwayat,
                    'kode_user': data.kode_user,
                    'peternakan': farm_nama,
                    'alamat_peternakan': farm_address,
                    'peternak': nama_pengguna,
                    'kode_peternakan': data.kode_peternakan,
                    'kode_penyakit': data.kode_penyakit,
                    'gejala': [gejala.gejala for gejala in data_gejala],
                    'persentase': f'{(data.persentase * 100):.2f}',
                    'kesimpulan': data.kesimpulan,
                    'other': data.other,
                    'penyakit': base_penyakit_dict
                }
            else:
                res_data = {
                    'kode_riwayat': data.kode_riwayat,
                    'kode_user': data.kode_user,
                    'kode_peternakan': data.kode_peternakan,
                    'kode_penyakit': data.kode_penyakit,
                    'gejala': [gejala.gejala for gejala in data_gejala],
                    'persentase': f'{(data.persentase * 100):.2f}',
                    'kesimpulan': data.kesimpulan,
                    'other': data.other,
                    'penyakit': base_penyakit_dict
                }
        if data is None:
            return False, 'Diagnose not found', None

        if data.kode_user != kode_user:
            return False, 'Diagnose not found', None
        return True, 'Success get Diagnose data', res_data
