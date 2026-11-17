"""Mock bytes and IDs only: no invented species pattern annotations."""
import io,unittest
from PIL import Image
from retrieve_CC_photo_pixels_for_human_review import (
    N_PER_TAXON,TARGET_TAXA,uri_medium,select,
    original_medium_image,contact_sheet)

def row(taxon="Dianthus deltoides",num=1,license="cc-by"):
    return {
        "source_original_iNat_species":taxon,
        "fresh_2026_original_iNaturalist_photo_id":str(num),
        "fresh_2026_original_iNaturalist_observation_id":str(num+100),
        "original_photo_url_as_source_returned":f"https://inaturalist-open-data.s3.amazonaws.com/photos/{num}/square.jpg",
        "original_photo_licence_code":license,
        "photo_is_open_flower_verified":"UNKNOWN_UNREAD_IMAGE",
        "source_photo_attribution_as_returned":"© Source example photographer",
    }

def jpeg():
    img=Image.new("RGB",(320,260),"white")
    out=io.BytesIO();img.save(out,format="JPEG");return out.getvalue()

class Response:
    def __init__(self,url,data):
        self.url=url;self.b=data
    def geturl(self):return self.url
    def read(self,n):return self.b[:n]
    def __enter__(self):return self
    def __exit__(self,*args):pass

class OriginalSourceCCPhotoPixelContracts(unittest.TestCase):
    def test_legit_iNat_medium_photo_derived_only_by_official_size_qualifier(self):
        q=row(num=123)
        self.assertEqual(uri_medium(q),
            "https://inaturalist-open-data.s3.amazonaws.com/photos/123/medium.jpg")
        q["fresh_2026_original_iNaturalist_photo_id"]="124"
        with self.assertRaisesRegex(ValueError,"ID_URL_MISMATCH"):
            uri_medium(q)
        q=row(num=123)
        q["original_photo_url_as_source_returned"]="https://unknown.host/photos/123/square.jpg"
        with self.assertRaisesRegex(ValueError,"NOT_AN_OPEN_DATA"):
            uri_medium(q)

    def test_select_blind_ID_prefrozen_two_per_taxon_and_exclude_SA(self):
        rows=[row(taxon=taxon,num=1000+i*10+j)
              for i,taxon in enumerate(TARGET_TAXA) for j in range(3)]
        rows[0]["original_photo_licence_code"]="cc-by-sa"
        selected=select(rows)
        self.assertEqual(len(selected),8)
        self.assertEqual(len({x["fresh_2026_original_iNaturalist_photo_id"] for x in selected}),8)
        self.assertNotIn("cc-by-sa",[x["original_photo_licence_code"] for x in selected])
        self.assertEqual(selected,select(list(reversed(rows))))
        self.assertTrue(all(x["photo_is_open_flower_verified"]=="UNKNOWN_UNREAD_IMAGE" for x in selected))

    def test_successfully_parse_source_JPEG_not_a_morphology_label(self):
        q=row(num=101)
        src=uri_medium(q)
        img,sha,url=original_medium_image(q,opener=lambda req,timeout:
                       Response(src,jpeg()))
        self.assertEqual(img.size,(320,260))
        self.assertEqual(len(sha),64)
        self.assertEqual(url,src)
        montage=contact_sheet([q],[(q,img,sha,url)])
        self.assertEqual(montage.size,(840,355))

    def test_reject_wrong_host_redirect_or_fake_source_dimensions(self):
        q=row(num=101)
        with self.assertRaisesRegex(ValueError,"DIFFERENT_OR_UNLICENSED"):
            original_medium_image(q,opener=lambda req,timeout:
                Response("https://evil.invalid/photo.jpg",jpeg()))
        with self.assertRaisesRegex(ValueError,"CANNOT_BE_READ"):
            original_medium_image(q,opener=lambda req,timeout:
                Response(uri_medium(q),b"not original image"))
if __name__=="__main__":unittest.main()
