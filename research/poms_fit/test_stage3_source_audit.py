import json
import tempfile
import unittest
from pathlib import Path
from zipfile import ZipFile
from stage3_source_audit import audit_archive, inventory_csv, field_roles, download_verified

class SchemaAuditTests(unittest.TestCase):
    def test_columns_do_not_infer_individual_visitors(self):
        fields=['FIT Count ID','Count date','Target flower species','Total insects','Count of flowers','Wind category']
        roles=field_roles(fields)
        self.assertIn('Count date',roles['date'])
        self.assertIn('Target flower species',roles['target_flower'])
        self.assertIn('Count of flowers',roles['flowering_quantity'])
        self.assertIn('Wind category',roles['weather'])
    def test_archive_inventory_and_header_preserve_zeros(self):
        with tempfile.TemporaryDirectory() as d:
            path=Path(d)/'synthetic.zip'
            with ZipFile(path,'w') as z:
                z.writestr('data/FIT.csv','Survey ID,Count date,Target flower,Number of insects\n1,2020-06-01,Rose,0\n2,2020-06-02,Thistle,3\n')
                z.writestr('README.txt','synthetic')
            inv=audit_archive(path)
            self.assertEqual(inv['member_count'],2)
            s=inventory_csv(path,'data/FIT.csv')
            self.assertEqual(s['sample_rows'],2)
            self.assertIn('Number of insects',s['numeric_column_candidates'])
    def test_fail_closed_on_expansion_limit(self):
        with tempfile.TemporaryDirectory() as d:
            path=Path(d)/'synthetic.zip'
            with ZipFile(path,'w') as z:z.writestr('huge.csv','x'*100)
            with self.assertRaises(ValueError):audit_archive(path,max_uncompressed=1)
    def test_nonzip_rejected_without_retrieval(self):
        with tempfile.TemporaryDirectory() as d:
            path=Path(d)/'synthetic.zip'
            path.write_text('<html>not the data</html>')
            with self.assertRaises(ValueError):download_verified('https://example.invalid/file',path)

if __name__=='__main__':unittest.main()
