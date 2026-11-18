"""Source-free Stage87F effort gates, no manufactured GBIF absence."""
import unittest
import numpy as np
import pandas as pd
from sensitivity_global_hue_Bombus_effort_wind import analysis_scenarios,STRICT,CELLS

class SpatialEffortGuards(unittest.TestCase):
    def sample(self):
        df=pd.DataFrame({CELLS:[20]*76+[10]*33+[5]*30,
             "n_source_single_explicit_hue":[100]*135+[50]*4,
             STRICT:[2]*139,
             "log_bombus_strict":[np.log1p(2)]*139})
        return df
    def test_source_quality_subsets_nested_without_imputed_absences(self):
        data=analysis_scenarios(self.sample())
        self.assertEqual({k:len(x) for k,x in data.items()},
          {"base_primary_5_1degree_cells":139,
           "GBIF_reporting_10_1degree_cells":109,
           "GBIF_reporting_20_1degree_cells":76,
           "NHM_source_at_least_100_exclusive_hue_taxa":135,
           "coordinate_uncertainty_le10km_recorded_richness":139})
    def test_stricter_coordinate_quality_not_a_confirmed_zero_species(self):
        df=self.sample()
        df.loc[4,STRICT]=0
        with self.assertRaises(ValueError):analysis_scenarios(df)
if __name__=="__main__":unittest.main()
