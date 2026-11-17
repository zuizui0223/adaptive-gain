"""Synthetic archive-file schemas only, not measured floral VOC absence."""
import io, unittest, zipfile
from probe_original_305_VOC_scent_tables import unpack_original_source

def create_zip(members):
    target=io.BytesIO()
    with zipfile.ZipFile(target,"w",compression=zipfile.ZIP_DEFLATED) as z:
        for path,data in members.items():
            z.writestr(path,data)
    return target.getvalue()

class OriginalPublishedVOC305Provenance(unittest.TestCase):
    def test_author_source_csv_and_supplement_metadata_not_species_labels(self):
        raw=create_zip({"study/Table S1.csv":b"Species,VOC_count,Guild\nA b,12,bee\n",
                        "study/figureS1.pdf":b"%PDF-1.0 mock"})
        d=unpack_original_source(raw)
        self.assertEqual(d["n_original_source_supplement_members"],2)
        self.assertTrue(d["source_paper_305_species_not_yet_imported"])
        self.assertTrue(d["source_odour_unknown_not_absent"])
        self.assertIn("TEXT_SOURCE_HEADER_AUDIT_ONLY",
                      [x["status"] for x in d["original_members"]])
        self.assertIn("PDF_SOURCE_MEMBER_IDENTIFIED_NOT_SPECIES_EXTRACTED",
                      [x["status"] for x in d["original_members"]])

    def test_outer_archived_directory_and_duplicate_sidecars_not_biological_data(self):
        data=create_zip({"__MACOSX/._table.csv":b"binary sidecar",
                         "docs/a.tsv":b"Species\tVOC\nx\tk"})
        d=unpack_original_source(data)
        self.assertEqual(d["n_original_source_supplement_members"],1)
        self.assertEqual(d["original_members"][0]["source_line_count"],2)
        self.assertEqual(len(d["original_members"][0]["sha256"]),64)

    def test_unreadable_source_not_false_zero(self):
        with self.assertRaisesRegex(ValueError,"SUPPLEMENT_NOT_ZIP"):
            unpack_original_source(b"not-original-source")

if __name__=="__main__":
    unittest.main()
