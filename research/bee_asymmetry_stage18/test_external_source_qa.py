"""Read-only original author-source record semantics: synthetic unit tests."""
import unittest
from external_source_qa import audit_rows, git_blob_sha1

FIELDS=['Trial_ID','Bee_ID','Trial_Number','Difficulty','Trial_Type',
        'Info_Requested','Actually_Landed_On_Platform',
        'Post_Request_Accuracy','Is_Post_Request_Correct',
        'Non_Request_Accuracy','Is_Post_Non_Request_Correct']

def row(i,bee,difficulty,trial,requested,landed):
    return dict(Trial_ID=str(i),Bee_ID=bee,Trial_Number=str(i),
           Difficulty=difficulty,Trial_Type=trial,
           Info_Requested=str(requested),
           Actually_Landed_On_Platform=str(landed),
           Post_Request_Accuracy='',
           Is_Post_Request_Correct='',
           Non_Request_Accuracy='',
           Is_Post_Non_Request_Correct='')

def fixture():
    return [
        row(1,'b1','Easy','Regular',0,0),
        row(2,'b1','Hard','Regular',1,1),
        row(3,'b1','Impossible','Regular',1,1),
        row(4,'b1','Easy','Random_Free_Cue',1,0),
        row(5,'b2','Easy','Regular',0,0),
        row(6,'b2','Hard','Regular',0,0),
        row(7,'b2','Impossible','Regular',1,1),
        row(8,'b2','Hard','Random_Free_Cue',1,1),
    ]

class SourceAuditTests(unittest.TestCase):
    def test_distinguishes_auto_info_flag_from_animal_request(self):
        result=audit_rows(fixture(),strict_original=False)
        self.assertEqual(result['total_rows'],8)
        self.assertEqual(result['source_bees'],2)
        self.assertEqual(result['free_cue_info_requested_unconditional'],2)
        self.assertEqual(result['free_cue_actual_landed'],1)
        self.assertEqual(result['auto_info_vs_platform_mismatch'],1)
        self.assertEqual(result['regular_flag_vs_actual_landing_mismatch'],0)
        self.assertEqual(result['n_bees_hard_request_gt_easy'],1)
        self.assertEqual(result['n_bees_easy_lt_hard_lt_impossible'],1)
    def test_source_original_trial_ids_must_be_unique(self):
        d=fixture();d[1]['Trial_ID']=d[0]['Trial_ID']
        with self.assertRaisesRegex(ValueError,'DUPLICATE_SOURCE_TRIAL_ID'):
            audit_rows(d,strict_original=False)
    def test_bad_original_binary_flags_fail_closed(self):
        d=fixture();d[1]['Actually_Landed_On_Platform']='3'
        with self.assertRaisesRegex(ValueError,'INVALID_ORIGINAL_SOURCE_BINARY'):
            audit_rows(d,strict_original=False)
    def test_git_blob_hash_is_over_header_and_exact_original_bytes(self):
        blob=b'x,y\\n1,2\\n'
        self.assertEqual(len(git_blob_sha1(blob)),40)
        self.assertNotEqual(git_blob_sha1(blob),git_blob_sha1(blob+b'\\n'))
if __name__=='__main__':unittest.main()
