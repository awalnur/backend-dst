# ============================================
#                                           
#   Project Name :  be_sistem_pakar               
#   -------------------------------------   
#   Create by    : hexa at 02/04/24       
#   Copyright © 2024 Delameta Bilano     
#                                           
# ============================================
from sqlalchemy.orm import Session

from src.schema import Rule


class DempsterShafer:

    def __init__(self, session: Session):
        self.session = session

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
                result = [{'himpunan': set(himpunan), 'bel': bel / div} for himpunan, bel in sums.items()]
                m = result

        result = max(m, key=lambda x: x['bel'])
        return result

    def dempster_shafer(self, data: dict):
        # TODO
        evidence = {}
        print(len(data) )
        if len(data['gejala']) < 2:
            return 'Failed to calculate dempster shafer, data must be more than 1'
        for gejala in data['gejala']:
            rules = self.session.query(Rule).filter(Rule.kode_gejala == gejala).all()
            evidence[gejala] = {
                'm': {rule.kode_penyakit for rule in rules},
                'bel': round(sum([rule.belief for rule in rules]) / len(rules) if len(rules) > 0 else 1, 2)
            }

        sorted_evidence = dict(sorted(evidence.items(), key=lambda item: item[1]['m'], reverse=True))
        # print(sorted_evidence)

        res = self.calculate_dempster_shafer(data, sorted_evidence)
        result={'penyakit': 'Penyakit Tidak terdeteksi', 'bel': 0}
        if res['bel'] > 0.5:
            result['penyakit']= res['himpunan']
            result['bel'] = res['bel']
        return result
