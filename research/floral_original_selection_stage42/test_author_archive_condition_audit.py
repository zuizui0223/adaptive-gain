"""Stage42 synthetic-only tests; no test row is from any observed bee."""
import unittest
from author_archive_condition_audit import (
   PAPER_PRIMARY_BY_P_W,publication_compatibility,
   author_script_semantics,_difference_stats
)


class OriginalSelectionContract(unittest.TestCase):
    def test_paper_archive_cell_lower_bound(self):
        x=publication_compatibility({
            'P0_W0':31,'P1_W0':25,'P0_W1':52,'P1_W1':49
        })
        self.assertEqual(x['minimum_missing_primary_files_if_one_to_one_and_labels_correct'],4)
        self.assertEqual(x['missing_primary_lower_bound_by_cell'],
                         {'P0_W0':0,'P1_W0':4,'P0_W1':0,'P1_W1':0})
        self.assertFalse(x['strict_source_subset_of_published_112_possible'])
        self.assertTrue(x['does_not_prove_original_author_error'])

    def test_extra_archive_records_do_not_make_biological_subset_identified(self):
        x=publication_compatibility({
            'P0_W0':31,'P1_W0':29,'P0_W1':60,'P1_W1':50
        })
        self.assertTrue(x['strict_source_subset_of_published_112_possible'])
        self.assertEqual(x['minimum_missing_primary_files_if_one_to_one_and_labels_correct'],0)
        self.assertTrue(x['does_not_prove_original_author_error'])

    def test_incomplete_cells_refused(self):
        with self.assertRaisesRegex(ValueError,'NO_GO_P_W_CELLS_INCOMPLETE'):
            publication_compatibility({'P0_W0':31})

    def test_invalid_cells_refused(self):
        x=dict(PAPER_PRIMARY_BY_P_W)
        x['P1_W0']=-3
        with self.assertRaisesRegex(ValueError,'NO_GO_INVALID_SOURCE_COUNTS'):
            publication_compatibility(x)

    def test_unauthenticated_matlab_never_accepted(self):
        with self.assertRaisesRegex(ValueError,'NO_GO_AUTHOR_MATLAB_ORIGINAL_HASH_CHANGED'):
            author_script_semantics(b'fake author code with guessed labels')

    def test_one_source_B_not_one_file_and_unmatched_S_P_discarded(self):
        key=(100,'three_tag_mean')
        rows=[]
        for b in ('01','02'):
            for w,v in [('W0',.1),('W1',.2)]:
                rows.append(dict(B=b,S='0',P='0',W=w,
                                 values={key:(.2,v,v-.2)}))
        # one extra S/P condition never paired with W0: no inflation
        rows.append(dict(B='01',S='0',P='1',W='W1',
                         values={key:(.2,99.,98.8)}))
        x=_difference_stats(rows,name={'S':'0'})
        v=x['matched_B_effects']['near_flower_speed']
        self.assertEqual(v['number_matched_B_codes'],2)
        self.assertAlmostEqual(v['mean_W1_minus_W0_m_s'],.1)
        self.assertEqual(v['positive_B_codes'],2)
        self.assertEqual(v['negative_B_codes'],0)
        self.assertAlmostEqual(v['leave_one_B_out_mean_min_max_m_s'][0],.1)
        self.assertEqual(x['source_tracks'],5)

    def test_no_matched_bees_is_explicit_no_go(self):
        key=(100,'three_tag_mean')
        rows=[dict(B='01',S='1',P='0',W='W0',
                   values={key:(.2,.1,-.1)})]
        x=_difference_stats(rows,name={'S':'1'})
        self.assertEqual(
            x['matched_B_effects']['near_flower_speed']['status'],
            'NO_GO_NO_MATCHED_B'
        )


if __name__=='__main__':
    unittest.main()
