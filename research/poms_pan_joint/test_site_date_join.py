import unittest
import pandas as pd

from site_date_join import (
    build_pan_environment, match_pan_fit, nearest_site_date, taxon_id, parse_original_dates
)

class CrossSourceJoinTests(unittest.TestCase):
    def stations(self):
        return pd.DataFrame([
          {"sample_id":"P1","location_code":"C1","x1km_square":"SQ1","pan_trap_station":"1","date":"2022-06-10","year":2022},
          {"sample_id":"P2","location_code":"C1","x1km_square":"SQ1","pan_trap_station":"2","date":"2022-06-10","year":2022},
          {"sample_id":"P3","location_code":"C1","x1km_square":"SQ1","pan_trap_station":"1","date":"2022-06-16","year":2022},
          {"sample_id":"P4","location_code":"C2","x1km_square":"SQ2","pan_trap_station":"1","date":"2022-06-10","year":2022},
        ])
    def flowers(self):
        return pd.DataFrame([
          {"sample_id":"P1","occurrence_id":"o1","taxon_source":"Rosa canina","source_taxon_version_key":"R1","total_floral_units":10},
          {"sample_id":"P1","occurrence_id":"o2","taxon_source":"Rosa canina","source_taxon_version_key":"R1","total_floral_units":3},
          {"sample_id":"P2","occurrence_id":"o3","taxon_source":"Trifolium repens","source_taxon_version_key":"T1","total_floral_units":5},
          {"sample_id":"P3","occurrence_id":"o4","taxon_source":"Cirsium vulgare","source_taxon_version_key":"C1","total_floral_units":5},
          {"sample_id":"P4","occurrence_id":"o5","taxon_source":"Bellis perennis","source_taxon_version_key":"B1","total_floral_units":9},
        ])
    def fit(self):
        return pd.DataFrame([
          {"sample_id":"F1","location_code":"C1","x1km_square":"SQ1","date":"2022-06-10","year":2022,"bumblebees":3,"other_flies":4},
          {"sample_id":"F2","location_code":"C1","x1km_square":"SQ1","date":"2022-06-13","year":2022,"bumblebees":1,"other_flies":1},
          {"sample_id":"F3","location_code":"C2","x1km_square":"SQ2","date":"2022-06-10","year":2022,"bumblebees":0,"other_flies":0},
          {"sample_id":"F4","location_code":"C1","x1km_square":"SQ9","date":"2022-06-10","year":2022,"bumblebees":4,"other_flies":2},
        ])
    def test_iso_dates_do_not_swap_day_and_month(self):
        values=pd.Series(["2022-06-10","2022-06-16","16/06/2022"])
        v=parse_original_dates(values)
        self.assertEqual(str(v.iloc[0].date()),"2022-06-10")
        self.assertEqual(str(v.iloc[1].date()),"2022-06-16")
        self.assertEqual(str(v.iloc[2].date()),"2022-06-16")

    def test_pan_foreign_key_and_richness_not_multiplying_census(self):
        pan,receipt,station=build_pan_environment(self.stations(),self.flowers())
        self.assertEqual(receipt["unique_pan_station_sample_ids"],4)
        self.assertEqual(len(pan),3)
        self.assertEqual(receipt["original_flower_occurrence_rows"],5)
        a=pan[(pan.location_code=="C1")&(pan.date==pd.Timestamp("2022-06-10"))].iloc[0]
        self.assertEqual(a.stations,2)
        self.assertEqual(a.pan_recorded_flowering_taxa,2)  # do NOT count duplicate Rosa twice
        evidence=match_pan_fit(self.fit(),pan,receipt)
        self.assertEqual(evidence["original_fit_surveys"],4)
        self.assertEqual(evidence["exact_site_grid_date_fit_surveys"],2)
        self.assertEqual(evidence["exact_with_recorded_flower_taxa_pair_positive_fit"],1)
        self.assertEqual(evidence["exact_unique_sites"],2)
        self.assertEqual(evidence["next_model_gate"],"NO_GO_INSUFFICIENT_EXACT_MATCHED_FLOWER_CONTEXT")
    def test_nearest_day_tie_goes_to_earlier_original_pan_date(self):
        pan,_,_=build_pan_environment(self.stations(),self.flowers())
        df=self.fit().iloc[[1]].copy()
        df["date"]=pd.to_datetime(df.date)
        df["year_from_date"]=df.date.dt.year
        joined=nearest_site_date(df,pan)
        self.assertEqual(joined.iloc[0].near_pan_date,"2022-06-10")
        self.assertEqual(joined.iloc[0].near_day_difference,-3)
        self.assertEqual(joined.iloc[0].near_pan_flower_richness,2)
    def test_grid_collision_does_not_pass_full_join(self):
        pan,receipt,_=build_pan_environment(self.stations(),self.flowers())
        evidence=match_pan_fit(self.fit(),pan,receipt)
        self.assertEqual(evidence["grid_date_only_matches"],2)
        self.assertEqual(evidence["same_site_grid_within_7_days_fit"],3)
    def test_orphan_flowers_quarantined_with_original_count_receipt(self):
        x=self.flowers().copy()
        x["year"]=2022
        x.loc[0,"sample_id"]="nonexistent"
        pan,receipt,stations=build_pan_environment(self.stations(),x)
        self.assertEqual(receipt["orphan_flower_occurrence_rows"],1)
        self.assertEqual(receipt["orphan_unique_station_ids"],1)
        self.assertEqual(receipt["original_flower_occurrence_rows"],5)
        self.assertEqual(receipt["floral_occurrence_rows_linkable"],4)
        self.assertEqual(len(pan),3)
        self.assertEqual(int(pan.pan_recorded_flowering_taxa.sum()),4)
    def test_taxon_version_key_wins_over_ambiguous_free_text(self):
        x={"source_taxon_version_key":"S1","taxon_source":"common name"}
        self.assertEqual(taxon_id(x),("key:S1","version_key"))
        y={"source_taxon_version_key":None,"taxon_source":"Rosa canina"}
        self.assertEqual(taxon_id(y),("source:rosa canina","taxon_source_fallback"))
    def test_duplicate_original_pan_sample_id_rejected(self):
        x=pd.concat([self.stations(),self.stations().iloc[[0]]],ignore_index=True)
        with self.assertRaisesRegex(ValueError,"not unique"):
            build_pan_environment(x,self.flowers())

if __name__=="__main__":unittest.main()
