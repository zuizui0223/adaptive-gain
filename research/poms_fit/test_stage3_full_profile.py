import unittest
import pandas as pd
from stage3_full_profile import GROUPS, profile_table, read_original_csv_bytes

class FullProfileTests(unittest.TestCase):
    def _test_rows(self):
        data={'sample_id':[1,2,3], 'date':['2021-05-01','2021-06-01','2021-07-01'],
              'year':[2021]*3, 'target_flower':['A','B','A'],
              'target_flower_corrected':['A','B','A'],'floral_unit_count':[20,30,40],
              'wind_speed':['calm','breezy','calm'],'sunshine':['sun','sun','cloud'],
              'cloud_cover':['low','low','high'],'flower_cover':['low','medium','high'],
              'floral_unit':['head']*3,'country':['England']*3,
              'recorder_type':['site']*3,'count_start_time':['10:00']*3,
              'location_code':['one']*3,'x1km_square':['grid']*3}
        data.update({group:[0,0,0] for group in GROUPS})
        data['bumblebees']=[0,1,2]
        data['all_insects_total']=[0,1,2]
        return pd.DataFrame(data)
    def test_legacy_windows_text_is_not_silently_replaced(self):
        source=b'target_flower,all_insects_total\n' + bytes([0x93]) + b'Flower' + bytes([0x94])+b',0\n'
        df, codec = read_original_csv_bytes(source)
        self.assertEqual(codec,'cp1252')
        self.assertEqual(len(df),1)
        self.assertIn('Flower',df.loc[0,'target_flower'])
        self.assertEqual(df.loc[0,'all_insects_total'],0)

    def test_true_zero_census_retained(self):
        d=profile_table(self._test_rows(),'one_km')
        self.assertEqual(d['rows'],3)
        self.assertEqual(d['zero_total_insect_rows'],1)
        self.assertEqual(d['site_year_with_ge3_dates'],1)
        self.assertEqual(d['total_insect_group_sum_mismatches'],0)
    def test_inconsistent_group_totals_detected(self):
        x=self._test_rows()
        x.loc[1,'all_insects_total']=4
        self.assertEqual(profile_table(x,'one_km')['total_insect_group_sum_mismatches'],1)
    def test_bad_negative_count_fails_closed(self):
        x=self._test_rows()
        x.loc[0,'bumblebees']=-1
        with self.assertRaises(ValueError):profile_table(x,'public')
    def test_duplicated_sample_id_is_reported(self):
        x=self._test_rows()
        x.loc[1,'sample_id']=1
        self.assertEqual(profile_table(x,'one_km')['sample_id_duplicated_rows'],2)

if __name__=='__main__':unittest.main()
