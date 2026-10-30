"""Synthetic original-grain tests. Not empirical Stage12 evidence."""
import unittest
import pandas as pd
from source_qa import assemble, count_categories

def fixture():
    f=pd.DataFrame([
        {"survey":"C1","date":"08/04/2024","site":"Brighton","location":"Falmer","plant":"Brassica napus","number of flights":3,"number of walks":1,"flowers probed ":5,"approx flower density (flowers / m2)":50},
        {"survey":"C1","date":"08/04/2024","site":"Brighton","location":"Falmer","plant":"Brassica napus","number of flights":0,"number of walks":2,"flowers probed ":3,"approx flower density (flowers / m2)":50},
        {"survey":"C2","date":"09/04/2024","site":"Brighton","location":"Falmer","plant":"Brassica napus","number of flights":1,"number of walks":1,"flowers probed ":3,"approx flower density (flowers / m2)":50}])
    w=pd.DataFrame([
        {"survey":"C1","date":"08/04/2024","site":"Brighton","location":"Falmer","temperature":13,"blue_sky":30,"beaufort":1},
        {"survey":"C1","date":"08/04/2024","site":"Brighton","location":"Falmer","temperature":14,"blue_sky":40,"beaufort":2},
        {"survey":"C2","date":"09/04/2024","site":"Brighton","location":"Falmer","temperature":15,"blue_sky":50,"beaufort":2}])
    i=pd.DataFrame([
        {"survey":"C1","date":"08/04/2024","site":"Falmer","plant":"Brassica napus","honeybees":12,"b.terrestris":3,"small fly":5},
        {"survey":"C2","date":"09/04/2024","site":"Falmer","plant":"Brassica napus","honeybees":10,"b.terrestris":2,"small fly":3}])
    return f,w,i

class Stage12SourceTests(unittest.TestCase):
    def test_source_weather_repeats_do_not_multiply_foraging(self):
        d,q=assemble(*fixture())
        self.assertEqual(len(d),2)
        r=d.set_index("survey").loc["C1"]
        self.assertEqual(r["flights"],3)
        self.assertEqual(r["walks"],3)
        self.assertEqual(r["movement_events"],6)
        self.assertEqual(r["behavior_rows"],2)
        self.assertEqual(r["weather_records"],2)
        self.assertAlmostEqual(r["beaufort"],1.5)
        self.assertAlmostEqual(r["other_share"],8/20)
    def test_insect_taxa_are_categories_not_species_richness(self):
        f,w,i=fixture()
        taxa=count_categories(i)
        self.assertEqual(set(taxa),{"b.terrestris","small fly"})
        d,_=assemble(f,w,i)
        self.assertEqual(d.iloc[0]["other_nonzero_categories"],2)
    def test_duplicate_insect_source_key_never_joins_many_to_many(self):
        f,w,i=fixture()
        i=pd.concat([i,i.iloc[[0]]],ignore_index=True)
        d,q=assemble(f,w,i)
        self.assertEqual(len(d),1)
        self.assertEqual(q["excluded"][0]["reason"],"nonunique_or_absent_insect_survey")
    def test_zero_movement_observations_are_not_fabricated_choices(self):
        f,w,i=fixture()
        f.loc[f.survey=="C2","number of flights"]=0
        f.loc[f.survey=="C2","number of walks"]=0
        d,q=assemble(f,w,i)
        self.assertEqual(list(d.survey),["C1"])
        self.assertEqual(q["excluded"][0]["reason"],"no_recorded_flight_or_walk")
    def test_invalid_original_count_quarantines_entire_survey(self):
        f,w,i=fixture()
        f.loc[0,"number of walks"]=-1
        d,q=assemble(f,w,i)
        self.assertEqual(list(d.survey),["C2"])
        self.assertEqual(q["excluded"][0]["survey"],"C1")
        self.assertEqual(q["excluded"][0]["reason"],"original_count_semantic_invalid")
        self.assertEqual(q["excluded"][0]["foraging_rows"],2)
        self.assertEqual(q["excluded"][0]["invalid_native_records"][0]["field"],"number of walks")
    def test_metadata_change_not_silently_harmonized(self):
        f,w,i=fixture()
        i.loc[0,"plant"]="Brassica species"
        d,q=assemble(f,w,i)
        self.assertEqual(list(d.survey),["C2"])
        self.assertEqual(q["excluded"][0]["reason"],"insect_source_metadata_mismatch")

if __name__=="__main__":unittest.main()
