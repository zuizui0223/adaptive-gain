"""Stage93 WFO DwC-A and lexical floral scent source-free guards."""
import io,tempfile,unittest,zipfile
from pathlib import Path
from original_wfo_eFloras_scent_full_prose import (
    canon_source_binomial,cleaned,scent_class,parse_meta,source_raw_flora
)
META='''<?xml version="1.0" encoding="UTF-8"?>
<archive xmlns="http://rs.tdwg.org/dwc/text/" metadata="eml.xml">
  <core encoding="UTF-8" fieldsTerminatedBy="\\t" fieldsEnclosedBy="&quot;" ignoreHeaderLines="1"
        rowType="http://rs.tdwg.org/dwc/terms/Taxon">
   <files><location>taxon.txt</location></files><id index="0"/>
   <field index="1" term="http://rs.tdwg.org/dwc/terms/scientificName"/>
   <field index="2" term="http://rs.tdwg.org/dwc/terms/taxonRank"/>
  </core>
  <extension encoding="UTF-8" fieldsTerminatedBy="\\t" fieldsEnclosedBy="&quot;" ignoreHeaderLines="1"
        rowType="http://rs.gbif.org/terms/1.0/Description">
   <files><location>description.txt</location></files><coreid index="0"/>
   <field index="1" term="http://purl.org/dc/terms/description"/>
  </extension>
</archive>'''

class Stage93SourceProseTests(unittest.TestCase):
    def test_explicit_fragrant_flower(self):
        self.assertEqual(scent_class("Flowers fragrant, calyx small."),"positive_candidate")
        self.assertEqual(scent_class("Strongly scented flowers. Shrub 2m tall."),"positive_candidate")
    def test_explicit_unscented_flower(self):
        self.assertEqual(scent_class("Flowers scentless, blue."),"explicit_negative_candidate")
        self.assertEqual(scent_class("Flowers not fragrant. Leaves glabrous."),"explicit_negative_candidate")
    def test_nonflower_odor_not_a_floral_positive(self):
        self.assertEqual(scent_class("Leaves fragrant. Flowers white."),"unmentioned_or_uncertain")
        self.assertEqual(scent_class("Aromatic bark; showy flowers."),"unmentioned_or_uncertain")
    def test_cross_organ_fragrance_not_flower_fragrance(self):
        for text in (
            "Leaves fragrant, flowers white and small.",
            "Flowers white, leaves fragrant and shiny.",
            "Flowers blue, stems strongly scented.",
            "Fragrant bark, flowers white.",
            "Flowers white, fruits fragrant."
        ):
            self.assertEqual(scent_class(text),"unmentioned_or_uncertain",text)
    def test_cross_organ_scentless_not_flower_scentless(self):
        for text in (
            "Leaves scentless, flowers white.",
            "Flowers white, leaves scentless.",
            "Odorless stems, flowers yellow.",
            "Flowers red, bark odorless."
        ):
            self.assertEqual(scent_class(text),"unmentioned_or_uncertain",text)
    def test_true_flower_fragrance_survives_nearby_nonfloral_other_clause(self):
        self.assertEqual(scent_class("Flowers fragrant, leaves green."),"positive_candidate")
        self.assertEqual(scent_class("Flowers fragrant; leaves scentless."),"positive_candidate")
        self.assertEqual(scent_class("Leaves green; flowers not fragrant."),"explicit_negative_candidate")

    def test_no_description_not_scentless(self):
        self.assertEqual(scent_class("Flowers purple."),"unmentioned_or_uncertain")
        self.assertEqual(scent_class(""),"empty_description")
    def test_conflict_not_assign_binary(self):
        self.assertEqual(scent_class("Flowers fragrant. Other flowers odorless."),"conflict_positive_negative")
    def test_uncertain_sign_not_positive(self):
        self.assertEqual(scent_class("Flowers possibly fragrant."),"unmentioned_or_uncertain")
    def test_html_to_visible_botanical_description(self):
        self.assertEqual(cleaned("<p>Flowers &amp; petals fragrant.</p>"),"Flowers & petals fragrant.")
    def test_only_species_rank_not_infraspecies(self):
        self.assertEqual(canon_source_binomial("Campanula punctata Lam.","species"),"campanula punctata")
        self.assertIsNone(canon_source_binomial("Campanula punctata var. alba","variety"))
    def test_stable_WFO_taxon_name_id_accepts_version_and_URI(self):
        from original_wfo_eFloras_scent_full_prose import stable_wfo_name_id
        self.assertEqual(stable_wfo_name_id("wfo-0000615907-2026-06"),"wfo-0000615907")
        self.assertEqual(stable_wfo_name_id("https://www.worldfloraonline.org/taxon/wfo-0000615907"),"wfo-0000615907")
        self.assertIsNone(stable_wfo_name_id("123456"))
    def test_original_taxonID_source_scan_requires_no_guessed_scientific_name(self):
        from original_wfo_eFloras_scent_full_prose import source_legacy_wfo_ids
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/"fake-source.zip"
            with zipfile.ZipFile(p,"w") as z:
                z.writestr("meta.xml",META.replace("scientificName","taxonID"))
                z.writestr("taxon.txt","id\ttaxonID\ttaxonRank\n"+
                    "".join(f"{i}\twfo-{i:010d}\tspecies\n" for i in range(1,105)))
                z.writestr("description.txt","id\tdescription\n")
            names,counts=source_legacy_wfo_ids(p)
            self.assertEqual(len(names),104)
            self.assertEqual(counts["source_core_rows"],104)
    def test_real_WFO_backbone_plain_tsv_classification_csv_contract(self):
        import hashlib
        from unittest.mock import patch
        import original_wfo_eFloras_scent_full_prose as mod
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/"dummy_backbone.zip"
            header="taxonID\tscientificName\ttaxonRank\ttaxonomicStatus\n"
            target="wfo-0000615907\tCampanula punctata\tspecies\taccepted\n"
            filler="wfo-9999999999\tOtherium unknownium\tspecies\taccepted\n"
            with zipfile.ZipFile(p,"w",compression=zipfile.ZIP_DEFLATED) as z:
                z.writestr("classification.csv",header+target+filler*100000)
            md5=hashlib.md5(p.read_bytes()).hexdigest()
            with patch.object(mod,"WFO_BACKBONE_202606_MD5",md5):
                names,meta=mod.WFO_backbone_202606_crosswalk(
                    p,{"wfo-0000615907"},{"campanula punctata"})
            self.assertEqual(names,{"wfo-0000615907":"campanula punctata"})
            self.assertEqual(meta["source_counts"]["original_backbone_core_rows"],100001)
            self.assertTrue(meta["no_synonym_or_fuzzy_matching_performed"])

    def test_modified_backbone_is_rejected_by_author_md5(self):
        from original_wfo_eFloras_scent_full_prose import WFO_backbone_202606_crosswalk
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/"fake-backbone.zip"
            with zipfile.ZipFile(p,"w") as z:z.writestr("README","fake")
            with self.assertRaisesRegex(ValueError,"MD5_MISMATCH"):
                WFO_backbone_202606_crosswalk(p,{"wfo-0000000001"},{"campanula punctata"})

    def test_xml_original_dwca_schema(self):
        with tempfile.TemporaryDirectory() as td:
            path=Path(td)/"source.zip"
            with zipfile.ZipFile(path,"w") as z:
                z.writestr("meta.xml",META)
                z.writestr("taxon.txt","id\tscientificName\ttaxonRank\n1\tCampanula punctata\tspecies\n")
                z.writestr("description.txt","id\tdescription\n1\tFlowers fragrant.\n")
            with zipfile.ZipFile(path) as z:
                met=parse_meta(z)
            self.assertEqual(len(met),2)
            self.assertEqual(met[0]["fields"]["scientificname"],1)
            self.assertEqual(met[1]["fields"]["description"],1)
    def test_taxon_id_only_core_is_unevaluated_not_negative(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/"FNA_taxonID_only.zip"
            with zipfile.ZipFile(p,"w") as z:
                z.writestr("meta.xml",META.replace("scientificName","taxonID"))
                z.writestr("taxon.txt","id\ttaxonID\ttaxonRank\n1\twfo-0123456789\tspecies\n")
                z.writestr("description.txt","id\tdescription\n1\tFlowers fragrant.\n")
            data,qc=source_raw_flora(p,{"campanula punctata"})
            self.assertEqual(data,{})
            self.assertFalse(qc["source_taxonomy_join_admissible"])
            self.assertTrue(qc["not_evaluated_not_zero_scent_species"])

    def test_unauthentic_small_archive_does_not_get_used_as_real_flora(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/"dummy.zip"
            with zipfile.ZipFile(p,"w") as z:
                z.writestr("meta.xml",META)
                z.writestr("taxon.txt","id\tscientificName\ttaxonRank\n1\tCampanula punctata\tspecies\n")
                z.writestr("description.txt","id\tdescription\n1\tFlowers fragrant.\n")
            with self.assertRaisesRegex(ValueError,"NOT_AUTHENTIC_DESCRIPTION_COVERAGE"):
                source_raw_flora(p,{"campanula punctata"})

if __name__=="__main__":unittest.main()
