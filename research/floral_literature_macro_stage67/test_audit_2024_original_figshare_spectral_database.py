"""Stage67 primary-source petal reflectance data tests (synthetic only)."""
from __future__ import annotations
import importlib.util,unittest,io,zipfile,json,hashlib
from pathlib import Path
HERE=Path(__file__).parent
spec=importlib.util.spec_from_file_location("spectra67",HERE/"audit_original_2024_shrestha_figshare_petal_spectral_database.py")
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)

def fixture_zip():
    a=io.BytesIO()
    with zipfile.ZipFile(a,"w") as z:
        lines=["wavelength,Species alpha,Species beta"]
        for wl in range(300,701):
            lines.append(f"{wl},0.2,0.3")
        z.writestr("data_&_rcode_Shrestha_et_al/petals/blue.csv","\n".join(lines))
        z.writestr("data_&_rcode_Shrestha_et_al/lvs/leaves.csv","\n".join(lines))
    return a.getvalue()

class Source2024SpectralTests(unittest.TestCase):
    def test_published_73_vs_83_categories_not_silently_corrected(self):
        rows,r=m.scan_authentic_zip(fixture_zip())
        self.assertEqual(r["original_published_claim_species"],73)
        self.assertEqual(r["paper_7_colour_groups_sum_11_10_10_17_10_11_14"],83)
        self.assertEqual(r["n_original_petal_spectral_columns_NOT_SPECIES"],2)
        self.assertEqual(r["n_source_columns_with_complete_UV_and_visible"],2)

    def test_uv_spectrum_not_false_binary_guide(self):
        rows,r=m.scan_authentic_zip(fixture_zip())
        self.assertEqual(rows[0]["UV_spatial_guide_status"],
                         "NOT_OBSERVABLE_FROM_ONE_PETAL_MEAN_SPECTRUM")
        self.assertTrue(r["no_FCP_or_iNaturalist_photographs_or_colour_labels"])
        self.assertTrue(rows[0]["not_GBIF_accepted_taxonomy_or_verified_negative"])

    def test_source_metadata_wrong_version_is_no_go(self):
        d={"id":21081025,"version":3,"doi":"10.6084/m9.figshare.21081025.v3",
           "files":[{"name":"data_Shrestha.zip","id":12,"size":13}]}
        class Dummy(io.BytesIO):pass
        def opener(*a,**k):return Dummy(json.dumps(d).encode())
        with self.assertRaisesRegex(ValueError,"VERSION_NOT_V2"):
            m.fetch_metadata(opener=opener)

    def test_source_bytes_MD5_and_length(self):
        raw=fixture_zip()
        meta={"id":5001,"name":"data_Shrestha.zip","size":len(raw),
              "computed_md5":hashlib.md5(raw).hexdigest()}
        def opener(*a,**k):return io.BytesIO(raw)
        b,receipt=m.download_exact_file(meta,opener=opener)
        self.assertEqual(b,raw)
        self.assertEqual(receipt["original_source_sha256"],hashlib.sha256(raw).hexdigest())
        meta["computed_md5"]="0"*32
        with self.assertRaisesRegex(ValueError,"MD5_CHANGED"):
            m.download_exact_file(meta,opener=opener)

    def test_no_petal_data_never_substitutes_leaf_data(self):
        b=io.BytesIO()
        with zipfile.ZipFile(b,"w") as z:
            lines="wavelength,species\n"+"\n".join(f"{i},0.1" for i in range(300,701))
            z.writestr("lvs/leaves.csv",lines)
        with self.assertRaisesRegex(ValueError,"NO_REAL_SOURCE_PETAL"):
            m.scan_authentic_zip(b.getvalue())

if __name__=="__main__":unittest.main()
