"""Stage26: only invented in-memory CSV fixtures; external original is not vendored."""
import csv
import io
import tempfile
import unittest
from pathlib import Path

from audit_author_request_semantics import (
    AUTHOR_COMMIT, SOURCE_BLOB_SHA1, SOURCE_PATH,
    COLUMNS, audit_csv_bytes, main
)


def make_row(tid,bee,n,typ,d,request,land,correct=1):
    r=dict.fromkeys(COLUMNS,'')
    r.update({
        'Trial_ID':str(tid),'Bee_ID':bee,'Trial_Number':str(n),
        'Difficulty':d,'Trial_Type':typ,
        'Info_Requested':str(request),
        'Actually_Landed_On_Platform':str(land),
    })
    if request:
        r.update({'Post_Request_Accuracy':str(float(correct)),
                  'Is_Post_Request_Correct':str(float(correct)).removesuffix('.0')})
    else:
        r.update({'Non_Request_Accuracy':str(float(correct)),
                  'Is_Post_Non_Request_Correct':str(float(correct)).removesuffix('.0')})
    return r


def encode(rows):
    s=io.StringIO()
    w=csv.DictWriter(s,fieldnames=COLUMNS,lineterminator='\n')
    w.writeheader()
    w.writerows(rows)
    return s.getvalue().encode('utf-8')


class Stage26AuthorSourceTests(unittest.TestCase):
    def test_locked_author_source_identity(self):
        self.assertEqual(AUTHOR_COMMIT,'7f886394b4de872ecdb19ca4ea214ec321d5dce9')
        self.assertEqual(SOURCE_PATH,'data/4_active_information_seeking_trials.csv')
        self.assertEqual(SOURCE_BLOB_SHA1,'26259c9071c6d73141d56b9bedd396cab1a04491')

    def test_mock_semantics_separate_auto_exposure_and_paid_action(self):
        data=encode([
            make_row(1,'MOCK_B1',1,'Regular','Easy',0,0),
            make_row(2,'MOCK_B1',2,'Random_Free_Cue','Easy',1,0),
            make_row(3,'MOCK_B1',3,'Regular','Hard',1,1),
            make_row(4,'MOCK_B1',4,'Random_Free_Cue','Hard',1,1),
            make_row(5,'MOCK_B2',1,'Random_Free_Cue','Impossible',1,0),
            make_row(6,'MOCK_B2',2,'Regular','Impossible',1,1),
        ])
        x=audit_csv_bytes(data,verify_source=False)
        self.assertEqual(x['source_trial_rows'],6)
        self.assertEqual(x['strict_regular_paid_animal_initiated_landings'],2)
        self.assertEqual(x['free_cue_flag_without_landing_total'],2)
        self.assertEqual(x['naive_cross_treatment_request_flag_total'],5)
        self.assertEqual(x['all_platform_landings_total'],3)
        self.assertFalse(x['stage25_eight_parameter_empirical_ci_ready'])
        self.assertTrue(x['no_new_animals'])

    def test_public_source_verified_mode_rejects_any_mock_byte(self):
        with self.assertRaisesRegex(ValueError,'BLOB_SHA_MISMATCH'):
            audit_csv_bytes(encode([make_row(1,'FAKE',1,'Regular','Easy',1,1)]))

    def test_duplicate_trial_id_fails_closed(self):
        data=encode([make_row(1,'FAKE_1',1,'Regular','Easy',1,1),
                     make_row(1,'FAKE_2',1,'Regular','Hard',1,1)])
        with self.assertRaisesRegex(ValueError,'DUPLICATED_TRIAL'):
            audit_csv_bytes(data,verify_source=False)

    def test_duplicate_bee_trial_number_fails_closed(self):
        data=encode([make_row(1,'FAKE_1',1,'Regular','Easy',1,1),
                     make_row(2,'FAKE_1',1,'Regular','Hard',1,1)])
        with self.assertRaisesRegex(ValueError,'DUPLICATED_TRIAL'):
            audit_csv_bytes(data,verify_source=False)

    def test_regular_flag_must_equal_real_landing(self):
        data=encode([make_row(1,'FAKE',1,'Regular','Easy',1,0)])
        with self.assertRaisesRegex(ValueError,'REGULAR_REQUEST_NOT_ACTUAL_LANDING'):
            audit_csv_bytes(data,verify_source=False)

    def test_free_cue_flag_is_not_optional(self):
        data=encode([make_row(1,'FAKE',1,'Random_Free_Cue','Easy',0,0)])
        with self.assertRaisesRegex(ValueError,'FREE_CUE_FLAG_NOT_EXPOSURE'):
            audit_csv_bytes(data,verify_source=False)

    def test_outcome_leakage_fails_closed(self):
        r=make_row(1,'FAKE',1,'Regular','Easy',0,0)
        r['Is_Post_Request_Correct']='1'
        with self.assertRaisesRegex(ValueError,'OUTCOME_BRANCH_LEAKAGE'):
            audit_csv_bytes(encode([r]),verify_source=False)

    def test_no_input_is_source_no_go(self):
        with tempfile.TemporaryDirectory() as folder:
            main(['--out',folder])
            text=Path(folder,'stage26_request_semantics_audit.json').read_text()
            self.assertIn('NO_GO_PUBLIC_AUTHOR_CSV_NOT_PROVIDED',text)
            self.assertIn('"no_new_animals": true',text)


if __name__=='__main__':
    unittest.main()
