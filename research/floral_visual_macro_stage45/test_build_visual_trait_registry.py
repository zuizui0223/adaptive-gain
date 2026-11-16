"""Stage45 original-CSV transformation safety tests, all synthetic."""
import csv
import io
import unittest
from unittest.mock import patch
from build_visual_trait_registry import (
    COLOUR_FIELDS,SELECTED_FIELDS,SOURCE_ROW_COUNT,
    summarize_and_extract,_get_source_bytes
)

def original_like_csv(rows):
    fields=['taxon','wfo',*SELECTED_FIELDS]
    out=io.StringIO()
    writer=csv.DictWriter(out,fieldnames=fields)
    writer.writeheader()
    writer.writerows(rows)
    return out.getvalue().encode('utf-8')

def newrow(name,**kw):
    out={'taxon':name,'wfo':'wfo-'+name.replace(' ','-')}
    out.update({k:'' for k in SELECTED_FIELDS})
    out.update(kw)
    return out

class BotanicalTraitRegistry(unittest.TestCase):
    def test_colour_morphology_not_a_confirmed_nectar_guide(self):
        b=original_like_csv([
          newrow("Mockus patterned",**{
             'flower colour':'white with purple stripes',
             'flower symmetry':'bilateral','pollination':'bees'}),
          newrow("Mockus plain",**{
             'flower colour':'white','flower symmetry':'radial'})
        ])
        r,p,s=summarize_and_extract(b,expected_rows=2)
        self.assertEqual(s['species_rows'],2)
        self.assertEqual(s['field_nonempty_counts']['any_flower_color'],2)
        self.assertEqual(s['field_nonempty_counts']['color_morphology_pollination'],1)
        self.assertEqual(s['unconfirmed_marking_candidates'],1)
        self.assertEqual(len(p),1)
        self.assertEqual(p[0]['taxon'],'Mockus patterned')
        self.assertEqual(p[0]['uv_guide_status'],'not_measured')
        self.assertEqual(r[0]['nectar_guide_presence'],'not_measured')
        self.assertEqual(r[1]['nectar_guide_presence'],'not_measured')
        self.assertEqual(r[1]['marking_text_review_candidate'],0)

    def test_missing_color_is_unknown_never_negative_guide(self):
        b=original_like_csv([
          newrow("Mockus empty",**{'pollination':'bee'}),
        ])
        r,p,s=summarize_and_extract(b,expected_rows=1)
        self.assertEqual(s['field_nonempty_counts']['any_flower_color'],0)
        self.assertEqual(r[0]['floral_colour_reported'],0)
        self.assertEqual(r[0]['nectar_guide_presence'],'not_measured')
        self.assertTrue(s['no_missing_trait_as_confirmed_absence'])

    def test_source_row_count_fails_closed(self):
        b=original_like_csv([newrow("Mockus only")])
        with self.assertRaisesRegex(ValueError,'NO_GO_NHM_SOURCE_ROW_COUNT_CHANGED'):
            summarize_and_extract(b)

    def test_source_schema_must_include_true_floral_columns(self):
        x=b'taxon,wfo\nMockus one,wfo-a\n'
        with self.assertRaisesRegex(ValueError,'NO_GO_SOURCE_SCHEMA_MISSING'):
            summarize_and_extract(x,expected_rows=1)

    def test_no_blank_taxon_allowed(self):
        x=original_like_csv([newrow("")])
        with self.assertRaisesRegex(ValueError,'NO_GO_EMPTY_SOURCE_TAXON'):
            summarize_and_extract(x,expected_rows=1)

    def test_original_source_bytes_gate_blocks_truncated(self):
        import io
        with patch('build_visual_trait_registry.SOURCE_FILE_SIZE',100):
            with patch('build_visual_trait_registry.urllib.request.urlopen',
                       return_value=io.BytesIO(b'abc')):
                with self.assertRaisesRegex(ValueError,'NO_GO_NHM_OFFICIAL_GIT_FILE_SIZE'):
                    _get_source_bytes()

    def test_immutable_official_git_blob_identity(self):
        import io
        from build_visual_trait_registry import _git_blob_hash
        data=b'abc'
        with patch('build_visual_trait_registry.SOURCE_FILE_SIZE',len(data)), \
             patch('build_visual_trait_registry.SOURCE_GIT_BLOB_SHA1',_git_blob_hash(data)), \
             patch('build_visual_trait_registry.urllib.request.urlopen',
                   return_value=io.BytesIO(data)):
            observed,prov=_get_source_bytes()
        self.assertEqual(observed,data)
        self.assertEqual(prov['source_endpoint'],
                         'OFFICIAL_NHM_UPSTREAM_GITHUB_PINNED_GIT_BLOB')
        self.assertFalse(prov['original_csv_bytes_not_authenticated'])

    def test_official_git_blob_digest_mismatch_is_no_go(self):
        import io
        with patch('build_visual_trait_registry.SOURCE_FILE_SIZE',3), \
             patch('build_visual_trait_registry.SOURCE_GIT_BLOB_SHA1','a'*40), \
             patch('build_visual_trait_registry.urllib.request.urlopen',
                   return_value=io.BytesIO(b'abc')):
            with self.assertRaisesRegex(ValueError,'NO_GO_NHM_ORIGINAL_SOURCE_GIT_BLOB_MISMATCH'):
                _get_source_bytes()

if __name__=='__main__':
    unittest.main()
