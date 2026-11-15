"""Stage36 unit tests: invented source archive, no real orchid bee raw rows."""
import csv
import io
import json
import unittest
import zipfile

from audit_original_session_design import (
 _read_rows,_range_by,_categories,_source_r_analysis_markers,
 audit_archive,ALLOWED_COLUMNS
)


def _csv_export(fieldnames, rows):
    stream=io.StringIO()
    writer=csv.DictWriter(stream,fieldnames=fieldnames,lineterminator='\n')
    writer.writeheader()
    writer.writerows(rows)
    return stream.getvalue().encode('utf8')

def _fake_archive():
    f=['_original_row_index',*ALLOWED_COLUMNS['collectionMetadata.csv']]
    cm=[dict.fromkeys(f,'') for _ in range(2)]
    for i,row in enumerate(cm):
        row.update({'_original_row_index':str(i+1),'site':f'MOCK_SITE_{i+1}',
            'date':'2020-01-01','start.time':'09:00','scent':'cineole',
            'count':str(2+i),'wind.mean':str(.1+i*.05),'rel.wind.KE':str(.02+i*.01)})
    fields=['_original_row_index',*ALLOWED_COLUMNS['integratedSpatialWindData.csv']]
    dw=[dict.fromkeys(fields,'') for _ in range(2)]
    for i,row in enumerate(dw):
        row.update({'_original_row_index':str(i+1),'site':f'MOCK_SITE_{i+1}',
            'coll.id':f'MOCK_{i+1}','date':'2020-01-01','start.time':'09:00',
            'scent':'cineole','count':str(2+i),
            'wind.mean':str(.1+i*.05),'wind.KE':str(.2+i*.01),
            'rel.bee.count':str(.8+i*.1),'cover200m':'.5',
            'keep':'TRUE'})
    bees=[
      {'number':str(i+1),'date':'2020-01-01','site':'MOCK_SITE_1',
       'time':'09:00','scent':'cineole','genus':'MOCK_G','species':'MOCK_sp'}
      for i in range(2)]
    data={
      'Zenodo/collectionMetadata.csv':_csv_export(f,cm),
      'Zenodo/integratedSpatialWindData.csv':_csv_export(fields,dw),
      'Zenodo/beedata.csv':_csv_export(
        ['number','date','site','time','scent','genus','species'],bees),
      'Zenodo/GenerateFiguresAndAnalyses_CrallEtAl_OrchidBeeWindEcology.R':
        b'model <- glmer(count ~ wind.mean + rel.wind.KE + (1 | site), family=poisson)\n'
    }
    buf=io.BytesIO()
    with zipfile.ZipFile(buf,'w',compression=zipfile.ZIP_DEFLATED) as z:
        for path,raw in data.items():z.writestr(path,raw)
    return buf.getvalue()


class CrallSourceStructureTest(unittest.TestCase):
    def test_fake_original_session_units_separate_from_individual_bees(self):
        receipt=audit_archive(_fake_archive(),{'doi':'10.5281/zenodo.FAKE'})
        self.assertEqual(receipt['status'],
                         'ORIGINAL_AUTHOR_SESSION_DESIGN_AUDITED_NOT_STATISTICAL_REFIT')
        self.assertEqual(receipt['files']['collectionMetadata.csv']['n_rows'],2)
        self.assertEqual(receipt['files']['integratedSpatialWindData.csv']['n_rows'],2)
        self.assertEqual(receipt['files']['beedata.csv']['n_rows'],2)
        self.assertTrue(receipt['session_is_primary_analysis_unit_not_bee_row'])
        self.assertFalse(receipt['visitation_effect_estimated'])
        self.assertTrue(receipt['no_raw_author_rows_or_code_uploaded'])

    def test_original_export_blank_row_index_is_not_missing(self):
        h,rows=_read_rows(b',site,wind.mean\n1,A,0.1\n2,B,0.2\n')
        self.assertEqual(h[0],'_original_row_index')
        self.assertEqual(len(rows),2)
        self.assertEqual(rows[1]['site'],'B')

    def test_numeric_missingness_and_categories(self):
        rows=[{'a':'0.1','b':'TRUE'}, {'a':'','b':'FALSE'}, {'a':'NaN','b':'TRUE'}]
        x=_range_by(rows,'a')
        self.assertEqual(x['n_numeric'],1)
        self.assertEqual(x['n_missing'],2)
        self.assertAlmostEqual(x['mean'],.1)
        self.assertEqual(_categories(rows,'b'),{'FALSE':1,'TRUE':2})

    def test_original_R_formula_is_not_used_as_new_result(self):
        x=_source_r_analysis_markers(
            b'model <- glmer(count ~ wind.mean + rel.wind.KE+(1|site),family=poisson)\n'
            b'model2 <- glm(count ~ cover200m,family=poisson)\n')
        self.assertEqual(x['selected_identifier_counts']['glmer('],1)
        self.assertEqual(len(x['model_call_openers']),2)
        self.assertFalse(x['complete_original_model_formula_verified'])

    def test_missing_author_session_source_fails_closed(self):
        with zipfile.ZipFile(io.BytesIO(_fake_archive())) as z:
            data={k:z.read(k) for k in z.namelist()
                  if not k.endswith('beedata.csv')}
        buf=io.BytesIO()
        with zipfile.ZipFile(buf,'w') as z:
            for k,v in data.items():z.writestr(k,v)
        with self.assertRaisesRegex(ValueError,'EXPECTED_ORIGINAL_SESSION_SOURCE_MISSING'):
            audit_archive(buf.getvalue(),{'doi':'FAKE'})

    def test_csv_row_arity_fail_closed(self):
        with self.assertRaisesRegex(ValueError,'ROW_FIELD_COUNT'):
            _read_rows(b'a,b\n1\n')

if __name__=='__main__':
    unittest.main()
