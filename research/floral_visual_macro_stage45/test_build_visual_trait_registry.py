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
        x=original_like_csv([{'taxon':'Mockus one','wfo':'wfo-a'}])
        with self.assertRaisesRegex(ValueError,'NO_GO_SOURCE_SCHEMA_MISSING'):
            summarize_and_extract(x,expected_rows=1)

    def test_no_blank_taxon_allowed(self):
        x=original_like_csv([newrow("")])
        with self.assertRaisesRegex(ValueError,'NO_GO_EMPTY_SOURCE_TAXON'):
            summarize_and_extract(x,expected_rows=1)

    def test_original_source_bytes_gate_blocks_truncated(self):
        with patch('build_visual_trait_registry._ckan',return_value={
            'id':'2552d157-9519-476c-995d-906e2433cc19',
            'size':100
        }):
            with self.assertRaisesRegex(ValueError,'NO_GO_RESOURCE_UNEXPECTED_SIZE'):
                _get_source_bytes()

if __name__=='__main__':
    unittest.main()
