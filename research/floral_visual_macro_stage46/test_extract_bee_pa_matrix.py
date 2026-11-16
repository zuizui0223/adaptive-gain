"""Offline exact ZIP member CRC and rectangular CSV tests."""
import io
import unittest
from unittest.mock import patch
import zipfile
import zlib
from extract_bee_pa_matrix import (
    decompress_original_member,source_matrix_schema
)
from zip_range_catalog import central_directory_location,parse_central_directory

class VerifyArchiveSourceMember(unittest.TestCase):
    def make_zip(self):
        b=io.BytesIO()
        with zipfile.ZipFile(b,"w",compression=zipfile.ZIP_DEFLATED) as z:
            z.writestr("data/bee_presence_only_matrix_15deg.csv",
                       "cell,Bombus_test,Apis_test\nA,1,0\nB,0,1\n")
        raw=b.getvalue()
        off,size,n=central_directory_location(raw[-262144:],len(raw))
        entry=parse_central_directory(raw[off:off+size],n)[0]
        return raw,entry

    def test_verify_crc_and_species_orientation_mock(self):
        raw,entry=self.make_zip()
        def r(url,total,start,end):return raw[start:end+1]
        with patch("extract_bee_pa_matrix.get_range",side_effect=r):
            source=decompress_original_member(
                "https://zenodo.org/api/records/20525240/files/data.zip/content",
                len(raw),entry)
        x=source_matrix_schema(source)
        self.assertEqual(x["Bombus_named_columns"],1)
        self.assertEqual(x["n_data_rows"],2)
        self.assertEqual(x["n_header_columns"],3)
        self.assertTrue(x["no_Bombus_richness_or_species_distributions_calculated_yet"])

    def test_corrupt_compressed_bytes_detected(self):
        raw,entry=self.make_zip()
        mutated=bytearray(raw)
        first=entry["local_header_offset"]+30+len(entry["filename"])
        mutated[first+2]^=1
        def r(url,total,start,end):return bytes(mutated[start:end+1])
        with patch("extract_bee_pa_matrix.get_range",side_effect=r):
            with self.assertRaises((ValueError,zlib.error)):
                decompress_original_member("https://zenodo.org/api/x",len(raw),entry)

    def test_unrectangular_matrix_does_not_get_called_predicted_presence(self):
        with self.assertRaisesRegex(ValueError,"NO_GO_SOURCE_MATRIX_NONRECTANGULAR"):
            source_matrix_schema(b"cell,Bombus test\nA,1\nB\n")

    def test_absent_csv_hard_stop(self):
        with self.assertRaisesRegex(ValueError,"NO_GO_SOURCE_MATRIX"):
            source_matrix_schema(b"bad")

if __name__=="__main__":
    unittest.main()
