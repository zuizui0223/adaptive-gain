"""Fully fabricated modelled bee taxa and original source trait fixtures."""
import unittest,json,tempfile,csv
from pathlib import Path
from audit_source_UV_Bombus_relative_guild import read_rows,summarize,contrast

def mock_rows():
    rows=[]
    for pat in (0,1):
        for tier in (1,2,3):
            for i in range(10):
                # Two N bins with positive values, S negative-control empty.
                n={"n_qualified_original_source_bee_HEX_records":12,
                   "n_distinct_visited_eligible_bee_hex_cells":3,
                   "modelled_Bombus_names_per_visited_bee_hex_equal_cell_mean_or_null":3+pat*2,
                   "modelled_all_bee_names_per_visited_bee_hex_equal_cell_mean_or_null":100-pat*15}
                s={"n_qualified_original_source_bee_HEX_records":0,
                   "n_distinct_visited_eligible_bee_hex_cells":0}
                rows.append({
                    "gbif_accepted_species_key":str(1000+pat*1000+tier*100+i),
                    "original_source_UV_pattern_binary":str(pat),
                    "original_latitude_tercile_within_pattern":str(tier),
                    "original_source_genus":"Potentilla",
                    "original_mean_published_latitude_positive_deg":"43",
                    "original_source_UVB":"2300",
                    "original_source_mean_temperature":"5",
                    "source_hemisphere_N_GBIF":json.dumps(n),
                    "source_hemisphere_S_GBIF":json.dumps(s)
                })
    return rows

class PublishedSourceGuildFractionTest(unittest.TestCase):
    def read_data(self,rows):
        with tempfile.TemporaryDirectory() as d:
            path=Path(d)/"sample.csv"
            with path.open("w",encoding="utf8",newline="") as f:
                w=csv.DictWriter(f,fieldnames=list(rows[0]))
                w.writeheader();w.writerows(rows)
            return read_rows(path)

    def test_original_richness_and_fraction_are_separate_phenotypes(self):
        data=self.read_data(mock_rows())
        r=summarize(data)
        self.assertEqual(r["n_prespecified_source_species"],60)
        self.assertEqual(r["n_viable_source_N"],60)
        self.assertEqual(r["n_viable_strict_source_N"],60)
        self.assertEqual(r["n_source_south_negative_control_viable"],0)
        metric=r["stratum_species_equal_descriptive_contrasts"][0]["metrics"]
        self.assertAlmostEqual(metric["source_modelled_Bombus_taxa_N"]["pattern_minus_uniform"],2)
        self.assertAlmostEqual(metric["source_modelled_all_bee_taxa_N"]["pattern_minus_uniform"],-15)
        self.assertTrue(metric["source_modelled_Bombus_share_proxy_N"]["pattern_minus_uniform"]>0)
        self.assertTrue(r["no_species_exchangeable_null_or_phylogeny_climate_adjustment"])
        self.assertTrue(r["original_2016_article_states_source_latitudes_21_07_to_76_49_N"])

    def test_source_first_page_unknown_not_implicitly_zero(self):
        rows=mock_rows()
        n=json.loads(rows[0]["source_hemisphere_N_GBIF"])
        n["n_qualified_original_source_bee_HEX_records"]=0
        n["n_distinct_visited_eligible_bee_hex_cells"]=0
        n["modelled_Bombus_names_per_visited_bee_hex_equal_cell_mean_or_null"]=None
        n["modelled_all_bee_names_per_visited_bee_hex_equal_cell_mean_or_null"]=None
        rows[0]["source_hemisphere_N_GBIF"]=json.dumps(n)
        q=self.read_data(rows)
        self.assertEqual(q[0]["viable_N_5records_2hex"],False)
        self.assertIsNone(q[0]["source_modelled_Bombus_share_proxy_N"])
        r=summarize(q)
        self.assertEqual(r["n_viable_source_N"],59)

    def test_original_source_60_and_latitude_tercile_balance(self):
        with self.assertRaisesRegex(ValueError,"NO_GO_PRESPECIFIED_60"):
            self.read_data(mock_rows()[:-1])
        x=mock_rows()
        x[0]["original_latitude_tercile_within_pattern"]="2"
        with self.assertRaisesRegex(ValueError,"NO_GO_ORIGINAL_UV_LATITUDINAL_BALANCE_CHANGED"):
            self.read_data(x)

    def test_nonfinite_source_modelled_richness_rejected(self):
        x=mock_rows()
        n=json.loads(x[0]["source_hemisphere_N_GBIF"])
        n["modelled_Bombus_names_per_visited_bee_hex_equal_cell_mean_or_null"]=120
        x[0]["source_hemisphere_N_GBIF"]=json.dumps(n)
        with self.assertRaisesRegex(ValueError,"NO_GO_BOMBUS_GUILD_NUMERIC_SOURCE"):
            self.read_data(x)

if __name__=="__main__":
    unittest.main()
