"""Only constructed paper rows and GBIF names. Not real floral outcomes."""
import unittest
from match_2025_review_colorchange_taxa_gbif_uv import validate,merge,PDF_SHA,REVIEW_DOI

def row(name):
    return {"binomial_candidate":name,"column_x":"110",
            "source_pdf_page_1_based":"5",
            "full_original_italic_taxon_text":name or "Vanda sp.",
            "original_source_colour_transition_text":"white to red",
            "source_original_pdf_sha256":PDF_SHA,
            "source_paper_doi":REVIEW_DOI}

def tax(key):
    return {"taxonomy_status":"EXACT_CONFIDENT_SPECIES_MAPPED",
            "gbif_accepted_usage_key":key}

class OriginalReviewPositiveOnly(unittest.TestCase):
    def test_accepted_review_name_not_a_primary_age_spectrum(self):
        review=[row("Weigela coraeensis"),row("")]
        uv={"42":{"source_measured_UV_spatial_pattern_or_missing":"1"}}
        rows,stats=merge(review,{"Weigela coraeensis":tax(42)},uv)
        self.assertEqual(stats["n_distinct_GBIF_accepted_reviewed_colour_changers"],1)
        self.assertEqual(stats["n_accepted_review_taxa_also_in_original_UV262"],1)
        self.assertEqual(rows[1]["review_negative_species_comparator"],
                         "NOT_SAMPLED_IN_POSITIVE_ONLY_REVIEW")
        self.assertEqual(rows[0]["bee_perceptible_colour_change_status"],
                         "NOT_MEASURED_FROM_REVIEW_TEXT")
        self.assertTrue(stats["positive_only_secondary_literature_source_no_measured_negative"])

    def test_source_136_columns_not_invented_151(self):
        with self.assertRaisesRegex(ValueError,"NO_GO_SOURCE_REVIEW_136_COLS_CHANGED"):
            validate([row("Weigela coraeensis")],[])

if __name__=="__main__":unittest.main()
