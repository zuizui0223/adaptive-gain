"""Source-free guards; only the workflows with pinned original sources fit data."""
from __future__ import annotations
import tempfile,unittest
from pathlib import Path
import pandas as pd
from source_age_wind_join_gate import join,read_file
from source_trait_independence_test import (
    score_with_exclusions,study_equal_weight_and_bootstrap
)


class Stage82Tests(unittest.TestCase):
    def test_two_fake_data_frames_cannot_be_used_as_field_data(self):
        with self.assertRaises(ValueError):
            join(pd.DataFrame(),pd.DataFrame())

    def test_modified_source_file_digest_is_rejected(self):
        with tempfile.TemporaryDirectory() as t:
            p=Path(t)/'fake.csv'
            p.write_text('one,two\n1,2\n')
            with self.assertRaises(ValueError):
                read_file(p,'bad_digest')

    def test_equal_original_publication_keeps_original_papers_one_each(self):
        rows=[]
        for i in range(10):
            rows.append({'source_publication':f'p{i}',
                'source_U_local_score':float(i+1),
                'source_I_local_null_fisher_information':1.0})
        x=study_equal_weight_and_bootstrap(pd.DataFrame(rows),reps=50)
        self.assertEqual(x['distinct_original_publications'],10)
        self.assertAlmostEqual(x['source_equal_publication_mean_U_over_I'],5.5)

    def test_after_species_removed_a_pair_is_no_longer_testable(self):
        g=pd.DataFrame([
          {'Study_id':'a','Network_id':'n','Year_from_original_date':2020,
           'Original_plant_accepted_name_literal':'a a','genus':'a',
           'n_observed_Bombus':10,'n_observed_other_bee':1,'source_age_trait_std':-1.},
          {'Study_id':'a','Network_id':'n','Year_from_original_date':2020,
           'Original_plant_accepted_name_literal':'b b','genus':'b',
           'n_observed_Bombus':1,'n_observed_other_bee':10,'source_age_trait_std':1.}
        ])
        self.assertEqual(len(score_with_exclusions(g)),1)
        self.assertEqual(len(score_with_exclusions(g,exclude_genus='a')),0)


if __name__=='__main__':unittest.main()
