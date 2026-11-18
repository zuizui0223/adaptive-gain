from pathlib import Path
import csv,unittest
from audit_stage_identifiability import audit

class AuditTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with Path(__file__).with_name('source_stage_ledger.csv').open(newline='',encoding='utf-8') as f:
            cls.rows=list(csv.DictReader(f))
    def test_no_full_stage_source(self):
        data=audit(self.rows)
        self.assertEqual(data['full_cue_route_and_fitness']['original_source_count'],0)
        self.assertEqual(data['scent_plume_with_wind_and_field_visits']['original_source_count'],0)
        self.assertEqual(data['wind_visual_guide_landing']['original_source_count'],0)
    def test_cognition_field_source_raw_unverified(self):
        data=audit(self.rows)
        c=data['learning_vs_visual_field_visits']
        self.assertEqual(c['original_source_count'],1)
        self.assertEqual(c['raw_currently_verified_source_count'],0)
    def test_no_missing_as_negative(self):
        rows=[dict(x) for x in self.rows]
        rows[0]['wind_exposure_same_source']='UNKNOWN'
        with self.assertRaises(ValueError):audit(rows)
    def test_duplicate_id_detected(self):
        with self.assertRaises(ValueError):audit(self.rows+[self.rows[0]])

if __name__=='__main__':unittest.main()
