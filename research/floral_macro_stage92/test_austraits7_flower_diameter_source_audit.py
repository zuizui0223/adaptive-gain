"""Stage92 source-free guards; original numeric results require Zenodo SHA."""
import io,tempfile,unittest,zipfile
from pathlib import Path
from austraits7_flower_diameter_source_audit import (
    schema,choose_source_table,normalized_diameter,parse_original_austraits_zip,regional
)

class Stage92SourceIntegrity(unittest.TestCase):
    def test_numeric_mm_conversion_is_unit_explicit(self):
        self.assertEqual(normalized_diameter("2.5","cm"),(25.0,"valid_source_labeled_mm"))
        self.assertEqual(normalized_diameter("0.04","m"),(40.0,"valid_source_labeled_mm"))
        self.assertEqual(normalized_diameter("21","mm"),(21.0,"valid_source_labeled_mm"))
    def test_missing_unit_not_inferred(self):
        self.assertIsNone(normalized_diameter("4.2","")[0])
        self.assertEqual(normalized_diameter("4.2","")[1],"unit_unrecognized")
    def test_reject_ranges_and_non_numeric(self):
        for v in ("2-5","2 to 5","approx 3","<1","NaN",""):
            self.assertIsNone(normalized_diameter(v,"mm")[0])
    def test_reject_zero_negative_and_implausible(self):
        self.assertIsNone(normalized_diameter("0","mm")[0])
        self.assertIsNone(normalized_diameter("-1","mm")[0])
        self.assertIsNone(normalized_diameter("1001","mm")[0])
    def test_long_schema_does_not_impute_units(self):
        s=schema(["taxon_name","trait_name","trait_value","dataset_id"])
        self.assertEqual(s["taxon"],"taxon_name")
        self.assertIsNone(s["unit"])
    def test_only_valid_long_source_selected(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/"fake.zip"
            with zipfile.ZipFile(p,"w") as z:
                z.writestr("tiny.csv","x,y\nfoo,bar\n")
                z.writestr("long.csv","taxon_name,trait_name,trait_value,trait_unit,dataset_id\n"
                           "Plant alba,flower_diameter,2,cm,eFLOWER_Dun_2022\n")
            with zipfile.ZipFile(p) as z:
                _,member,col=choose_source_table(z)
                self.assertEqual(member,"long.csv")
                self.assertEqual(col["unit"],"trait_unit")
    def test_unverified_source_rejected_before_traits(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/"fabricated.zip"
            with zipfile.ZipFile(p,"w") as z:
                z.writestr("traits.csv","taxon_name,trait_name,trait_value\nPlant alba,flower_diameter,3\n")
            with self.assertRaisesRegex(ValueError,"SHA256"):
                parse_original_austraits_zip(p,{"plant alba"})
    def test_regional_counts_only_native_species(self):
        ids={"plant alba","plant rubra","sylva alba"}
        traits={"plant alba":22.0,"sylva alba":8.0,"outgroup major":200.0}
        row=regional(ids,traits,{"plant alba":"animal","sylva alba":"wind"},
              {"plant alba":"Testaceae","sylva alba":"Otheraceae"})
        self.assertEqual(row["n_original_AusTraits_flower_diameter_species"],2)
        self.assertEqual(row["diameter_median_mm_of_source_species"],15.0)
        self.assertEqual(row["n_diameter_species_GIFT_animal"],1)
        self.assertEqual(row["n_diameter_species_GIFT_wind"],1)
        self.assertEqual(row["wind_exposure_join_admissible"],"NO")
    def test_no_eligible_size_is_not_zero_mm(self):
        row=regional({"plant alba"},{},{},{})
        self.assertEqual(row["n_original_AusTraits_flower_diameter_species"],0)
        self.assertEqual(row["diameter_median_mm_of_source_species"],"")
    def test_no_source_diameter_is_not_petals(self):
        row=regional({"plant alba"},{"plant alba":24.0},{},{})
        self.assertNotIn("petal",str(row).casefold())

if __name__=="__main__":unittest.main()
