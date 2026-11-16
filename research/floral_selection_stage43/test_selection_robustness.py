"""Stage43 pure synthetic and arithmetic tests; no invented rows are animals."""
import unittest
from selection_robustness import (
   PUB_PROSE,PUB_FIG1_CAPTION_FIRST_CLAUSE,
   publication_denominator_audit,robust_adversarial_removals,
   source_paired_differences
)


class SelectionAndDenominator(unittest.TestCase):
    def test_literal_publication_condition_reads_both_conflicts(self):
        x=publication_denominator_audit(
            {'P0_W0':31,'P1_W0':25,'P0_W1':52,'P1_W1':49},
            {'W0':56,'W1':101}
        )
        self.assertEqual(x['publication_Fig1_main_prose_P_W']
                         ['conditional_minimum_unavailable_paper_paths'],4)
        self.assertEqual(x['publication_Fig1_caption_first_clause_P_W']
                         ['conditional_minimum_unavailable_paper_paths'],2)
        self.assertTrue(x['paper_fig1_first_clause_and_main_prose_differ'])
        self.assertTrue(x['standard_t_implied_n_differs_from_main_W_n'])
        self.assertEqual(x['sample_n_if_ordinary_one_sample_or_paired_t'],
                         {'W0':55,'W1':55})
        self.assertTrue(x['paper_notes_are_an_identification_warning_not_proof_author_mistake'])

    def test_paper_literal_original_counts_total_are_112(self):
        self.assertEqual(sum(PUB_PROSE.values()),112)
        self.assertEqual(sum(PUB_FIG1_CAPTION_FIRST_CLAUSE.values()),112)

    def test_wrong_source_grain_rejected(self):
        with self.assertRaisesRegex(ValueError,'NO_GO_SOURCE_PW_W_GRAIN_MISMATCH'):
            publication_denominator_audit(
                {'P0_W0':31,'P1_W0':25,'P0_W1':52,'P1_W1':49},
                {'W0':57,'W1':101}
            )

    def test_exact_worst_case_removals_not_monte_carlo(self):
        a=robust_adversarial_removals([-.1,.2,.3,.4])
        self.assertEqual(a['n_unique_matched_B_codes'],4)
        self.assertAlmostEqual(a['original_equal_B_mean_m_s'],.2)
        self.assertAlmostEqual(a['worst_mean_delete_1_m_s'],(.2+.3-.1)/3)
        self.assertAlmostEqual(a['worst_mean_delete_2_m_s'],(.2-.1)/2)
        self.assertEqual(a['minimum_adversarial_whole_B_deletions_to_nonpositive_mean'],3)
        self.assertEqual(a['largest_k_all_k_deletions_preserve_positive_mean'],2)

    def test_all_positive_b_removal_sign_never_flips(self):
        a=robust_adversarial_removals([.01,.02,.03,.05])
        self.assertIsNone(a['minimum_adversarial_whole_B_deletions_to_nonpositive_mean'])
        self.assertEqual(a['largest_k_all_k_deletions_preserve_positive_mean'],3)

    def test_already_nonpositive_is_zero_deletion(self):
        a=robust_adversarial_removals([-.61,.1,.2,.3])
        self.assertEqual(a['minimum_adversarial_whole_B_deletions_to_nonpositive_mean'],0)
        self.assertEqual(a['largest_k_all_k_deletions_preserve_positive_mean'],-1)

    def test_no_paired_data_is_no_go(self):
        self.assertEqual(robust_adversarial_removals([])['status'],'NO_GO_NO_PAIRED_B')

    def test_nonfinite_data_refused(self):
        with self.assertRaisesRegex(ValueError,'NO_GO_NONFINITE_INDIVIDUAL_CONTRAST'):
            robust_adversarial_removals([.1,float('nan')])

    def test_exact_B_S_P_controls_repeats_and_unmatched(self):
        key=(100,'three_tag_mean')
        rows=[]
        for B in ('01','02'):
            for W,n in [('W0',.1),('W1',.3)]:
                rows.append({'B':B,'S':'0','P':'0','W':W,
                             'values':{key:(.5,n,n-.5)}})
        # Under a new P cell with W1 only: ignore, no biased mean
        rows.append({'B':'01','S':'0','P':'1','W':'W1',
                     'values':{key:(.5,100.,99.5)}})
        # Another bee with just wind, not matched: ignore.
        rows.append({'B':'03','S':'0','P':'0','W':'W1',
                     'values':{key:(.5,100.,99.5)}})
        d=source_paired_differences(rows,100,'three_tag_mean',1,{'S':'0'})
        self.assertEqual(len(d),2)
        for v in d:self.assertAlmostEqual(v,.2)
        a=robust_adversarial_removals(d)
        self.assertEqual(a['positive_B'],2)

    def test_invalid_subset_field_is_blocked(self):
        with self.assertRaisesRegex(ValueError,'NO_GO_SUBSET_INVALID_FIELDS'):
            source_paired_differences([],subset={'flower_species':'fake'})


if __name__=='__main__':
    unittest.main()
