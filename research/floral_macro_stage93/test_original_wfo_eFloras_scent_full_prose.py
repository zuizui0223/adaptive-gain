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
