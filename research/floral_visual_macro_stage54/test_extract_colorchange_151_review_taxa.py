"""Only invented rotated-page spans; validates extraction, not biology."""
import unittest
from extract_colorchange_151_review_taxa import group_italic_taxa,match_original_colour
def span(text,x,y,font="PalatinoLinotype,Italic",size=9):
    return {"value":text,"x0":x,"y0":y,"font":font,"size":size}
class SourceRotatedPaperColumnParser(unittest.TestCase):
    def test_original_species_single_span_and_split_binomial_as_two(self):
        src=[
          span("Weigela decora",180,612),
          span("Epidendrum",110,640),span("stamfordianum",122,630),
          span("Vanda",224,650),
          span("Plants",38,751),
          span("Eastern Asia",180,260),
          span("White to yellow",180,500,"PalatinoLinotype")
        ]
        groups=group_italic_taxa(src)
        self.assertEqual(len(groups),3)
        self.assertEqual([g["binomial_candidate"] for g in groups],
                         ["Epidendrum stamfordianum","Weigela decora",""])
        self.assertEqual(groups[2]["taxonomy_resolution"],"GENUS_ONLY_OR_UNRESOLVED_SOURCE_TABLE")
        match_original_colour(groups,src)
        self.assertEqual(groups[1]["original_source_colour_transition_text"],"White to yellow")

    def test_do_not_infer_guide_use_or_absence_from_2025_review(self):
        rows=group_italic_taxa([
            span("Mockus visualis",80,610),
            span("Mockus uniformis",110,610)
        ])
        self.assertEqual(len(rows),2)
        self.assertTrue(all(r["taxonomy_resolution"]==
                            "ORIGINAL_REVIEW_BINOMIAL_UNRECONCILED" for r in rows))

if __name__=="__main__":unittest.main()
