"""Stage38 synthetic-only source and rate-grain regression checks."""
from __future__ import annotations
import hashlib
import io
import unittest
import zipfile
from unittest.mock import patch
from urllib.error import HTTPError

from landing_original_sources import (
   ZENODO_RECORD,ZENODO_FILE,ZENODO_MD5,
   _zip_inventory,inspect_zenodo,read_mendeley_metadata,
   author_published_landing_rate_benchmark,separate_noncombinable_stages,
   _fetch,run
)

def mock_zip():
    o=io.BytesIO()
    with zipfile.ZipFile(o,"w",compression=zipfile.ZIP_DEFLATED) as z:
        z.writestr("MOCK/landing_track.csv","wind,landing_x\n0,1\n3.4,2\n")
        z.writestr("MOCK/landing_code.m","%synthetic only")
    return o.getvalue()

def mock_meta(blob):
    return {'id':ZENODO_RECORD,
        'metadata':{'title':'Wind alters landing dynamics in bumblebees',
          'creators':[{'name':'Chang, Jeremy J'},{'name':'Crall, James'}]},
        'files':[{'key':ZENODO_FILE,
                   'size':len(blob),
                   'checksum':'md5:'+ZENODO_MD5}]}


class WindLandingSourceTests(unittest.TestCase):
    def test_original_archive_file_grain_mock(self):
        x=_zip_inventory(mock_zip())
        self.assertEqual(x['file_count'],2)
        self.assertEqual(x['entries'][0]['type'],'.csv')
        self.assertEqual(x['raw_data_rows_disclosed'],0)
        self.assertTrue(x['no_flight_or_person_data_redistributed'])

    def test_source_filename_wind_codes_not_assumed_trial_success_denominator(self):
        mem=io.BytesIO()
        with zipfile.ZipFile(mem,'w',zipfile.ZIP_DEFLATED) as z:
            z.writestr('kinematic data/B01_F01_T01_W0_samplexyzpts.csv',
                       'frame,x,y,z\n1,0.0,0.2,0.1\n')
            z.writestr('kinematic data/B01_F01_T02_W1_samplexyzpts.csv',
                       'frame,x,y,z\n2,0.0,0.1,0.1\n')
            z.writestr('__MACOSX/kinematic data/._B01_F01_T01_W0_samplexyzpts.csv',
                       b'not original data')
        d=_zip_inventory(mem.getvalue())
        self.assertEqual(d['kinematic_source_B_label_count'],1)
        self.assertEqual(d['filename_W0_W1_trajectory_counts'],
                         {'W0':1,'W1':1})
        self.assertTrue(d['filename_W_codes_not_authentic_wind_metadata'])
        self.assertEqual(d['one_original_trajectory_header_profile'][0]
                         ['first_row_column_names_if_not_numeric'],
                         ['frame','x','y','z'])
        self.assertTrue(d['one_original_trajectory_header_profile'][0]
                        ['no_original_numeric_rows_reported'])

    def test_fake_bytes_never_claim_original_zenodo_sha(self):
        with self.assertRaisesRegex(ValueError,'ZIP_CHECKSUM'):
            inspect_zenodo(mock_meta(mock_zip()),mock_zip())

    def test_unrelated_source_rejected_by_authors_and_title(self):
        m=mock_meta(mock_zip())
        m['metadata']['title']='not about landing or wind'
        with self.assertRaisesRegex(ValueError,'TITLE_MISMATCH'):
            inspect_zenodo(m,mock_zip())
        m=mock_meta(mock_zip())
        m['metadata']['creators']=[{'name':'Unknown author'}]
        with self.assertRaisesRegex(ValueError,'CHANG_AUTHOR_MISSING'):
            inspect_zenodo(m,mock_zip())

    def test_landing_rate_not_success_probability_from_paper(self):
        p=author_published_landing_rate_benchmark()
        self.assertAlmostEqual(p['free_flight_high_vs_calm_rate_ratio'],
                               112.2/280.8)
        self.assertAlmostEqual(p['free_flight_drop_fraction'],.6004273504273504)
        self.assertAlmostEqual(p['post_takeoff_high_vs_calm_rate_ratio'],
                               16.5/56.)
        self.assertEqual(p['published_tracked_successful_landings'],19421)
        self.assertEqual(p['published_free_flight_tracks']+
                         p['published_post_takeoff_tracks'],19421)
        self.assertTrue(p['cannot_infer_landing_success_probability'])
        self.assertTrue(p['not_original_raw_reanalysis'])

    def test_no_cross_source_pollen_fitness_multiplication(self):
        p=separate_noncombinable_stages()
        self.assertEqual(p['status'],'NO_GO_CROSS_SYSTEM_STAGE_MULTIPLICATION')
        self.assertTrue(p['no_same_bee_or_plant_or_site_cohort'])
        self.assertTrue(p['do_not_multiply_source_effects_into_plant_fitness'])
        self.assertTrue(p['no_wind_by_floral_odor_interaction_estimated'])

    def test_mendeley_source_metadata_only_if_title_and_version_match(self):
        obj={'short_id':'mww9m8r3dk',
             'version':1,'name':'Landing manoeuvres of bumblebees in steady sidewind',
             'doi':{'id':'10.17632/mww9m8r3dk.1'}}
        z=read_mendeley_metadata(obj)
        self.assertEqual(z['status'],'MENDELEY_PUBLIC_METADATA_CONFIRMED')
        self.assertTrue(z['no_original_mat_trajectory_rows_extracted'])
        with self.assertRaisesRegex(ValueError,'UNVERIFIED_MENDELEY_DATASET_ID'):
            read_mendeley_metadata(dict(obj,version=2))
        with self.assertRaisesRegex(ValueError,'UNRELATED_MENDELEY_TITLE'):
            read_mendeley_metadata(dict(obj,name='Wind technology manual'))

    def test_fake_archive_no_zip_or_traversal(self):
        with self.assertRaisesRegex(ValueError,'VALID_ZIP'):
            _zip_inventory(b'not zip')
        o=io.BytesIO()
        with zipfile.ZipFile(o,"w") as f:
            f.writestr("../sensitive.csv","fake\n")
        with self.assertRaisesRegex(ValueError,'UNSAFE_ZIP'):
            _zip_inventory(o.getvalue())

    def test_host_whitelist(self):
        with self.assertRaisesRegex(ValueError,'UNTRUSTED_PUBLIC_ARCHIVE_HOST'):
            _fetch('https://example.invalid/secret')

    def test_unavailable_original_is_reported_as_no_go(self):
        err=HTTPError("https://zenodo.org/api/records/60234",503,
                      'Unavailable',None,None)
        with patch('landing_original_sources._fetch',side_effect=err):
            x=run()
        self.assertEqual(x['zenodo2016']['status'],
                         'NO_GO_ZENODO_ORIGINAL_ARCHIVE_NOT_VERIFIED')
        self.assertEqual(x['mendeley2024']['status'],
                         'NO_GO_MENDELEY_PUBLIC_API_OR_IDENTITY')
        self.assertTrue(x['cross_source_identifiability']
                        ['no_same_bee_or_plant_or_site_cohort'])
        self.assertTrue(x['no_new_pollinator_data_collected'])


if __name__=='__main__':
    unittest.main()
