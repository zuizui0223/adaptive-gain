"""Stage71B mock controls: visitor outcomes cannot influence sample entry."""
import importlib.util, unittest
from collections import defaultdict,Counter
from pathlib import Path
from unittest.mock import patch
from shapely.geometry import box
p=Path(__file__).with_name("build_outcome_blind_native_visitation_cohort.py")
spec=importlib.util.spec_from_file_location("st71b_blind",p)
m=importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

class OutcomeBlindSourceFrameTests(unittest.TestCase):
    def samples(self, bombus):
        names=("bellis perennis","daucus carota")
        spectra={
          names[0]:{"uv":2.3,"visible":55,"nhm":True,"accepted_spectra_GBIF":True},
          names[1]:{"uv":8.4,"visible":43,"nhm":True,"accepted_spectra_GBIF":True}}
        rows=[]
        for study,net,year in (("A","net1","2018"),("B","net2","2019")):
            for name in names:
                rows.append({
                  "Stage67_direct_petal_spectra_name_match":"1",
                  "Study_id":study,"Network_id":net,"Year_from_original_date":year,
                  "Original_plant_accepted_name_literal":name,
                  "Author_study_sampling_method":"Transect",
                  "Author_study_taxa_recorded":"all bees",
                  "Author_study_DOI":"NA",
                  "n_observed_Bombus":str(bombus),
                  "n_observed_other_bee":"100",
                })
        acc={n:{str(i)} for i,n in enumerate(names)}
        states=defaultdict(lambda:defaultdict(set))
        for n in names:states[n]["FRA"]={"native"}
        coords={("A","net1","2018"):{(5,5)},("B","net2","2019"):{(5,5)}}
        polygons=[("FRA",box(0,0,10,10))]
        with (patch.object(m,"SOURCE_SPECTRAL_PLANT_NETWORK_UNITS",4),
              patch.object(m,"SOURCE_VISITOR_NETWORKS_WITH_AT_LEAST_TWO_OPTICAL_SPECIES",2)):
            return m.freeze_before_outcome(rows,spectra,acc,states,coords,polygons,polygons)

    def test_zero_vs_many_bombus_yields_identical_frozen_frame(self):
        a=self.samples(0)
        b=self.samples(1000)
        self.assertEqual(a,b)
        self.assertEqual(a[2]["source_original_networks_native_area_primary_without_guild_outcome_filter"],2)
        self.assertFalse(a[2]["source_guild_information_used_in_cohort_selection"])

    def test_strict_species_bee_reporting_missing_bombus_not_absence(self):
        frozen,networks,_=self.samples(0)
        events=defaultdict(Counter)
        events[("A","net1","2018","bellis perennis")]["other_bee"]=3
        out,receipt=m.attach_outcomes(frozen,networks,events)
        target=[r for r in out if r["Study_id"]=="A" and r["original_plant_species"]=="bellis perennis"][0]
        self.assertEqual(target["source_bumblebee_species_rank_records"],0)
        self.assertEqual(target["source_bee_recorded_share_if_denominator_positive"],0.0)
        no=[r for r in out if r["Study_id"]=="B" and r["original_plant_species"]=="bellis perennis"][0]
        self.assertEqual(no["source_bee_recorded_share_if_denominator_positive"],"")
        self.assertEqual(receipt["primary"]["outcome_blind_source_networks"],2)
        self.assertEqual(receipt["primary"]["networks_with_two_or_more_native_spectral_species_each_at_least_3_strict_bee"],0)

    def test_visitation_guild_does_not_define_original_uv_measurement(self):
        with self.assertRaisesRegex(ValueError,"NOT_73"):
            m.original_spectra([])
        self.assertEqual(m.SOURCE_VISITOR_NETWORKS_WITH_AT_LEAST_TWO_OPTICAL_SPECIES,685)

if __name__=="__main__":unittest.main()
