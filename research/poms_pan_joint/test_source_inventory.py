import tempfile
import unittest
import zipfile
from pathlib import Path
from source_inventory import csv_preview, inspect_archive, zip_guard

class OriginalPanSourceInventoryTests(unittest.TestCase):
    def test_plant_and_site_columns_discovered_without_exposing_identifiers(self):
        with tempfile.TemporaryDirectory() as td:
            path=Path(td)/"test.zip"
            with zipfile.ZipFile(path,"w") as z:
                z.writestr("data/flower_records.csv",
                    "sample_id,location_code,flowering_plant,date,record_type\n"
                    "1,SiteA,Trifolium,2022-06-21,flower\n"
                    "2,SiteA,Cirsium,2022-06-21,flower\n")
            with zipfile.ZipFile(path) as z:
                audit=csv_preview(z,"data/flower_records.csv")
                self.assertIn("location_code",audit["columns"])
                profile={x["column"]:x for x in audit["key_field_profiles"]}
                self.assertEqual(profile["flowering_plant"]["sample_unique"],2)
                self.assertNotIn("category_levels",profile["sample_id"])
                self.assertNotIn("category_levels",profile["location_code"])
                self.assertEqual(profile["record_type"]["category_levels"],{"flower":2})
    def test_full_member_hash_and_grain_inventory(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/"dataset.zip"
            with zipfile.ZipFile(p,"w") as z:
                z.writestr("data/a.csv","site,date,flowers\nA,2022-06-05,3\n")
                z.writestr("readme.txt","original archive")
            result=inspect_archive(p)
            self.assertEqual(result["csv_members"],1)
            self.assertEqual(len(result["members"]),2)
            self.assertEqual(len(result["members"][0]["sha256_uncompressed_member"]),64)
    def test_duplicate_archive_names_are_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/"duplicate.zip"
            with zipfile.ZipFile(p,"w") as z:
                z.writestr("a.csv","x\n1\n")
                z.writestr("a.csv","x\n2\n")
            with zipfile.ZipFile(p) as z:
                with self.assertRaises(ValueError):zip_guard(z)
    def test_no_guessing_missing_plant_absence(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/"only_positive.zip"
            with zipfile.ZipFile(p,"w") as z:
                z.writestr("flower.csv","sample_id,flower_name\n1,Rosa\n2,Cirsium\n")
            result=inspect_archive(p)
            self.assertEqual(result["members"][0]["csv"]["sample_rows"],2)
            # Inventory must not manufacture a missing plant for any date.
            self.assertNotIn("inferred_absence",result["members"][0]["csv"])

if __name__=="__main__":unittest.main()
