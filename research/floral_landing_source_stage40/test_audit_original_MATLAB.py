"""Stage40 mocks author-code hints without copying original source code."""
import io
import zipfile
import unittest
from audit_original_MATLAB import source_script_inventory


def mock_matlab_zip(two_primary=False):
    out=io.BytesIO()
    with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED) as a:
        a.writestr('original_code/analyzeTrackingData.m',
                   'fps=1000;\n'
                   'xyz=csvread(fileName);\n'
                   'filtered=filtfilt(butter(5,0.2),xyz);\n'
                   'goodTracks=~isnan(xyz(:,1));\n'
                   '% test comments with impossible statements\n')
        a.writestr('original_code/trackBEEtagForDLT.m',
                   'pt=xyzpts(:,1:9); % BEEtag pt 1..3\n')
        if two_primary:
            a.writestr('copy/analyzeTrackingData.m','not a unique code identity\n')
    return out.getvalue()


class Stage40OriginalCodeSourceAudit(unittest.TestCase):
    def test_only_original_source_pointers_in_receipt(self):
        x=source_script_inventory(mock_matlab_zip())
        self.assertEqual(x['status'],'ORIGINAL_AUTHOR_MATLAB_SOURCE_POINTERS_ONLY')
        self.assertEqual(x['source_code_debug_hints'],[])
        self.assertEqual(len(x['script_inventory']),2)
        self.assertTrue(x['no_source_MATLAB_code_or_raw_data_redistributed'])
        self.assertFalse(x['physical_m_per_s_difference_estimated'])
        self.assertFalse(x['author_published_112_tracks_selection_recovered'])

    def test_limited_debug_pointers_not_authentication_of_units(self):
        x=source_script_inventory(mock_matlab_zip(),include_excerpt=True)
        hints=x['source_code_debug_hints']
        self.assertTrue(any('fps=1000' in h['excerpt_debug_ONLY'] for h in hints))
        self.assertTrue(any('isnan' in h['excerpt_debug_ONLY'] for h in hints))
        self.assertTrue(all(len(h['excerpt_debug_ONLY'])<=190 for h in hints))
        self.assertFalse(x['original_meter_per_native_unit_recovered'])

    def test_primary_script_missing_fail_closed(self):
        buf=io.BytesIO()
        with zipfile.ZipFile(buf,'w') as z:
            z.writestr('other/file.m','no analysis')
        with self.assertRaisesRegex(ValueError,'PRIMARY_ANALYSIS_SCRIPT_MISSING'):
            source_script_inventory(buf.getvalue())

    def test_duplicate_primary_script_names_fail_closed(self):
        with self.assertRaisesRegex(ValueError,'AMBIGUOUS_AUTHOR_SCRIPT_PATH'):
            source_script_inventory(mock_matlab_zip(two_primary=True))

    def test_nonarchive_input_never_looks_like_author_code(self):
        with self.assertRaisesRegex(ValueError,'SOURCE_NOT_VERIFIED_ZIP_BYTES'):
            source_script_inventory(b'MATLAB text not a ZIP')


if __name__=='__main__':
    unittest.main()
