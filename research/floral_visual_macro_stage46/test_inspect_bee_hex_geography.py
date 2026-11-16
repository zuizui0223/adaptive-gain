import unittest
from inspect_bee_hex_geography import _dbf_header

class OriginalShapefileSourceTests(unittest.TestCase):
    def test_parse_dbase_field_descriptor(self):
        b=bytearray(66)
        b[0]=3
        b[4:8]=(2).to_bytes(4,'little')
        b[8:10]=(65).to_bytes(2,'little')
        b[10:12]=(10).to_bytes(2,'little')
        b[32:38]=b"siteid"
        b[43]=ord("C");b[48]=9;b[64]=13
        d=_dbf_header(bytes(b))
        self.assertEqual(d["records"],2)
        self.assertEqual(d["field_schema"][0]["name"],"siteid")

    def test_short_dbf_fails(self):
        with self.assertRaisesRegex(ValueError,"NO_GO_SHAPE_DBF_SHORT"):
            _dbf_header(b"abc")

if __name__=="__main__":
    unittest.main()
