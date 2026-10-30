import hashlib, io, unittest, zipfile
from source_gate import verify, csv_profile, select_member

class SourceGateTests(unittest.TestCase):
    def test_provider_digest_enforced(self):
        data=b'a,b\n1,2\n'
        self.assertEqual(verify(data,hashlib.sha256(data).hexdigest(),'sha256'),hashlib.sha256(data).hexdigest())
        with self.assertRaises(ValueError): verify(data,'0'*64,'sha256')
    def test_csv_cr_grain_preserved(self):
        r=csv_profile(b'survey,value\r1,3\r1,4\r2,NA\r')
        self.assertEqual(r['rows'],3)
        self.assertEqual(r['unique_surveys'],2)
        self.assertEqual(r['missing']['value'],1)
    def test_duplicate_archive_names_rejected(self):
        b=io.BytesIO()
        with zipfile.ZipFile(b,'w') as z:
            z.writestr('x/forage.csv','a\n1')
            z.writestr('y/forage.csv','a\n2')
        with zipfile.ZipFile(io.BytesIO(b.getvalue())) as z:
            with self.assertRaises(ValueError): select_member(z,'forage.csv')
    def test_no_silent_csv_width_change(self):
        with self.assertRaises(ValueError): csv_profile(b'a,b\n1,2,3\n')

if __name__=='__main__': unittest.main()
