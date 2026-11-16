"""Mock only source grain and identity contract tests."""
import csv
import io
import unittest
from probe_fcp_photo_species_frame import _sha1_blob,profile

class SourceProbeFixture(unittest.TestCase):
    def make(self,rows):
        out=io.StringIO()
        w=csv.DictWriter(out,fieldnames=['scientific_name','n_photos','n_classifiable'])
        w.writeheader()
        w.writerows(rows)
        return out.getvalue().encode('utf8')

    def test_valid_source_schema_returns_taxon_and_photo_column_names(self):
        data=self.make([
           {'scientific_name':'Mockus a','n_photos':'100','n_classifiable':'40'},
           {'scientific_name':'Mockus b','n_photos':'100','n_classifiable':'20'}])
        d=profile(data,expected_rows=2)
        self.assertEqual(d['species_ledger_rows'],2)
        self.assertIn('n_photos',d['candidate_species_and_photo_fields'])
        self.assertTrue(d['not_measured_uv_or_visible_guide_presence'])

    def test_missing_real_4475_count_is_no_go(self):
        with self.assertRaisesRegex(ValueError,'NO_GO_FCP_SPECIES_COUNT_CHANGED'):
            profile(self.make([{'scientific_name':'Mockus a','n_photos':'100',
                               'n_classifiable':'40'}]))

    def test_wrong_input_type_no_go(self):
        with self.assertRaisesRegex(ValueError,'NO_GO_NOT_FCP_SOURCE_BYTES'):
            profile("not bytes",expected_rows=1)

    def test_git_blob_hash_changes_when_any_source_byte_changes(self):
        self.assertNotEqual(_sha1_blob(b'a'),_sha1_blob(b'b'))


if __name__=='__main__':
    unittest.main()
