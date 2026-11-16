"""Offline original Dryad CSV source and no UV phenotype imputation QA."""
import unittest,hashlib,urllib.error
from unittest.mock import patch
from probe_2960_clade_and_727_taiwan_original_csvs import (
    _summarize_rows,_file_source,_get
)

class BroadVisualColourSource(unittest.TestCase):
    def test_source_csv_human_colour_not_UV_guide(self):
        body=b'clade,species,flower_color,fruit_color\nA,Mockus_alba,red,blue/purple\n'
        rows,summary=_summarize_rows(body)
        self.assertEqual(len(rows),1)
        self.assertEqual(summary['source_columns'],['clade','species','flower_color','fruit_color'])
        self.assertTrue(summary['not_confirmed_UV_or_nectar_guide_traits'])

    def test_bad_source_host_is_blocked(self):
        with self.assertRaisesRegex(ValueError,"NO_GO_UNTRUSTED_ORIGINAL_DRYAD_HOST"):
            _get("https://evil.invalid/record")

    def test_download_failed_not_a_negative_flower_colour(self):
        x={"path":"final_dataset.csv","digest":"a"*64,
           "_links":{"stash:download":{"href":"/api/v2/files/1/download"}}}
        with patch("probe_2960_clade_and_727_taiwan_original_csvs._get",
                   side_effect=urllib.error.HTTPError("test",403,"denied",{},None)):
            raw,report=_file_source(x)
        self.assertIsNone(raw)
        self.assertEqual(report['source_fetch_status'],'NOT_RETRIEVED_NOT_A_NEGATIVE_TRAIT')

if __name__=='__main__':unittest.main()
