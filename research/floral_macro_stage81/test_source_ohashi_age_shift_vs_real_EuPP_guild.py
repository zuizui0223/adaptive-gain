import unittest
import pandas as pd
import source_ohashi_age_shift_vs_real_EuPP_guild as m

class AuthenticNetworkEstimatorGuards(unittest.TestCase):
    def source(self,homogeneous=False):
        return pd.DataFrame([
          {"Study_id":"23_Holzschuh","Network_id":"A","Year_from_original_date":"2021",
           "Original_plant_accepted_name_literal":"x alpha","genus":"x","source_age_trait_std":-1.,
           "n_observed_Bombus":0,"n_observed_other_bee":4},
          {"Study_id":"23_Holzschuh","Network_id":"A","Year_from_original_date":"2021",
           "Original_plant_accepted_name_literal":"y beta","genus":"y","source_age_trait_std":1.,
           "n_observed_Bombus":0 if homogeneous else 4,
           "n_observed_other_bee":4 if homogeneous else 0},
        ])
    def test_publisher_habitat_ids_are_one_publication(self):
        self.assertEqual(m.publication("23_Holzschuh"),m.publication("25_Holzschuh"))
        self.assertNotEqual(m.publication("5_Marini"),m.publication("6_Marini"))
    def test_local_binomial_score_and_information(self):
        r=m.one_network_score(self.source())
        self.assertIsNotNone(r)
        self.assertAlmostEqual(r["source_U_local_score"],4)
        self.assertAlmostEqual(r["source_I_local_null_fisher_information"],2)
    def test_no_ghost_biological_absence_when_only_one_guild_recorded(self):
        self.assertIsNone(m.one_network_score(self.source(homogeneous=True)))
    def test_BH_false_discovery_rate(self):
        self.assertEqual(list(m.bh_fdr([.01,.04,.9])),[.03,.06,.9])
    def test_missing_replicated_publications_cannot_be_bootstrapped(self):
        with self.assertRaises(ValueError):
            m.publication_bootstrap(pd.DataFrame({"source_publication":["a"]*5,
              "source_U_local_score":[1.]*5,"source_I_local_null_fisher_information":[3.]*5}))

if __name__=="__main__":unittest.main()
