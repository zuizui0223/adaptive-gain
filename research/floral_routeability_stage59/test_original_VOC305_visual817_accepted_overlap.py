"""Only source-contract fixtures; synthetic species are not biological records."""
import io,unittest,zipfile
from original_VOC305_visual817_accepted_overlap import (
    colnum,source_binomial,verify_and_extract,accepted_crosswalk
)

def addr(n):
    n+=1
    s=""
    while n:
        n,x=divmod(n-1,26)
        s=chr(65+x)+s
    return s

def inline(col,row,val):
    return f'<c r="{addr(col)}{row}" t="inlineStr"><is><t>{val}</t></is></c>'

def fake_xlsx():
    headers=["Source article","Species","APG III synonims","wind"]
    cols=[inline(i,1,v) for i,v in enumerate(headers)]
    cols+=[inline(12,1,"Annual Mean Temperature (K)")]
    cols+=[inline(i,1,f"original_voc_column_{i}") for i in range(23,823)]
    one=[inline(0,2,"Original study A"),inline(1,2,"Acer negundo"),
         inline(3,2,"1"),inline(9,2,"1"),inline(23,2,"1"),
         inline(24,2,"0"),inline(12,2,"287.8")]
    two=[inline(0,3,"Original study B"),inline(1,3,"Potentilla erecta"),
         inline(23,3,"1")]
    xml=('<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">'
         '<sheetData>'
         f'<row r="1">{"".join(cols)}</row>'
         f'<row r="2">{"".join(one)}</row>'
         f'<row r="3">{"".join(two)}</row>'
         '<row r="4"></row></sheetData></worksheet>')
    f=io.BytesIO()
    with zipfile.ZipFile(f,"w") as z:z.writestr("xl/worksheets/sheet1.xml",xml)
    return f.getvalue()

def prior():
    out=[]
    for i in range(817):
        out.append({
          "gbif_accepted_species_key":str(1000+i),
          "source_UV_pattern_directly_measured_or_unknown":
             "1" if i==0 else "",
          "original_Oliveira2025_UV_mean_source":"True" if i==1 else "False",
          "original_Ohashi2015_spectral_taxon_source":"True" if i==0 else "False",
          "original_2025_literature_colour_change_reported":"True" if i==0 else "False"
        })
    return out

class OriginalVOC305StrictCrosswalkContracts(unittest.TestCase):
    def test_source_excel_AA_and_ZZ_indices(self):
        self.assertEqual(colnum("A2"),0)
        self.assertEqual(colnum("Z3"),25)
        self.assertEqual(colnum("AA101"),26)
        self.assertEqual(colnum("ZZ101"),701)
        self.assertEqual(colnum("AAA101"),702)

    def test_source_original_305_frame_parser_with_small_fixture(self):
        plants,receipt=verify_and_extract(fake_xlsx(),expected_named=2,expected_rows=4)
        self.assertEqual(len(plants),2)
        self.assertEqual(plants[0]["source_species_canonical_binomial_if_valid"],"Acer negundo")
        self.assertEqual(plants[0]["source_VOC_positive_presence_columns_in_original_full_bouquet"],1)
        self.assertEqual(plants[0]["source_VOC_explicit_numeric_zero_columns"],1)
        self.assertEqual(receipt["n_original_source_non_species_rows"],1)
        self.assertEqual(receipt["n_first_header_named_chemical_or_summary_columns"],800)
        self.assertEqual(receipt["n_original_source_wind_pollination_yes"],1)
        self.assertTrue(receipt["no_original_wind_speed_m_per_s"])

    def test_infra_or_generic_labels_not_false_species_binomial(self):
        self.assertEqual(source_binomial("Potentilla sp."),"")
        self.assertEqual(source_binomial("Potentilla × hybrida"),"")
        self.assertEqual(source_binomial("Acer negundo L."),"Acer negundo")

    def test_two_source_records_strict_accepted_species_and_modality_overlap(self):
        plants,_=verify_and_extract(fake_xlsx(),expected_named=2,expected_rows=4)
        gbif={
          "Acer negundo":{"taxonomy_status":"EXACT_CONFIDENT_SPECIES_MAPPED",
                          "gbif_accepted_usage_key":1000},
          "Potentilla erecta":{"taxonomy_status":"EXACT_CONFIDENT_SPECIES_MAPPED",
                              "gbif_accepted_usage_key":1001}
        }
        rows,stats=accepted_crosswalk(plants,gbif,prior())
        self.assertEqual(stats["n_source_VOC_accepted_also_in_visual817"],2)
        self.assertEqual(stats["n_source_VOC_accepted_also_direct_measured_UV_spatial_230"],1)
        self.assertEqual(stats["n_source_VOC_accepted_also_UVmean_Oliveira_243"],1)
        self.assertEqual(stats["n_distinct_accepted_source_union_817_plus_VOC"],817)
        self.assertEqual(rows[0]["also_source_measured_UV_pattern_or_unknown"],"1")
        self.assertTrue(rows[0]["wind_flag_is_wind_pollination_NOT_atmospheric_wind"])

    def test_unresolved_name_never_invents_scent_absent_or_visual_negative(self):
        plants,_=verify_and_extract(fake_xlsx(),expected_named=2,expected_rows=4)
        rows,stats=accepted_crosswalk(plants,{},prior())
        self.assertEqual(stats["n_distinct_strict_GBIF_accepted_VOC_species"],0)
        self.assertEqual(stats["n_source_VOC_accepted_also_in_visual817"],0)
        self.assertTrue(stats["unlisted_VOC_species_are_unknown_not_verified_scentless"])
        self.assertEqual(rows[0]["GBIF_strict_accepted_species_key_or_unknown"],"")

    def test_missing_sheet_or_source_305_count_is_hard_stop(self):
        with self.assertRaisesRegex(ValueError,"NAMED_SOURCE_SPECIES_CHANGED"):
            verify_and_extract(fake_xlsx(),expected_named=305,expected_rows=4)
        with self.assertRaisesRegex(ValueError,"SOURCE_XLSX_ROW_COUNT_CHANGED"):
            verify_and_extract(fake_xlsx(),expected_named=2,expected_rows=305)

if __name__=="__main__":
    unittest.main()
