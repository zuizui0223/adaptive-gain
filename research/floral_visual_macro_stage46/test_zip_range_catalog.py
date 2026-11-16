"""Tiny synthetic zip with standard ZIP central directory; no modelled bees."""
import io
import unittest
import zipfile
from unittest.mock import patch
from zip_range_catalog import (
    central_directory_location,parse_central_directory,probe
)


def synthetic_zip():
    out=io.BytesIO()
    with zipfile.ZipFile(out,"w",compression=zipfile.ZIP_DEFLATED) as f:
        f.writestr("data/bee_presence_only_matrix_15deg.csv","cell,Bombus_ex\n1,1\n")
        f.writestr("data/other.txt","no biology")
    return out.getvalue()


class RemoteZipCatalogTests(unittest.TestCase):
    def test_source_CD_parse_matches_python_zipfile(self):
        blob=synthetic_zip()
        tail=blob[-262144:]
        offset,length,n=central_directory_location(tail,len(blob))
        result=parse_central_directory(blob[offset:offset+length],n)
        self.assertEqual(len(result),2)
        self.assertEqual(result[0]["filename"],"data/bee_presence_only_matrix_15deg.csv")
        self.assertGreater(result[0]["compressed_bytes"],0)

    def test_corrupt_cd_refused(self):
        with self.assertRaisesRegex(ValueError,"NO_GO_ZIP_CENTRAL_DIRECTORY_FILE_HEADER"):
            parse_central_directory(b"0"*46,1)
        with self.assertRaisesRegex(ValueError,"NO_GO_ZIP_END_OF_CENTRAL_DIRECTORY_MISSING"):
            central_directory_location(b"fake zip",100)

    def test_source_catalog_only_tiny_byte_ranges(self):
        blob=synthetic_zip()
        def source_chunk(url,total,start,end):
            self.assertEqual(total,len(blob))
            return blob[start:end+1]
        meta={"id":20525240,
              "files":[{"key":"data.zip","size":len(blob),
                 "checksum":"md5:mock_checksum",
                 "links":{"self":"https://zenodo.org/api/records/20525240/files/data.zip/content"}}]}
        with patch("zip_range_catalog._get_json",return_value=(meta,"meta")),patch(
             "zip_range_catalog.get_range",side_effect=source_chunk):
            a=probe()
        self.assertEqual(a["status"],"AUTHENTIC_ORIGINAL_GLOBAL_BEE_MODEL_ZIP_RANGE_DIRECTORY_READ")
        self.assertEqual(a["candidate_count"],1)
        self.assertTrue(a["bytes_read_source_index"]<=len(blob)*2)
        self.assertTrue(a["no_full_zip_or_21GB_raster_download"])

if __name__=="__main__":
    unittest.main()
