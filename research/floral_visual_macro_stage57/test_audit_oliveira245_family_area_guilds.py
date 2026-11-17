"""Mock source records only; original DOI fields checked in live workflow."""
import unittest
from audit_oliveira245_family_area_guilds import collapse_species,contrasts

def sample(key,guild="bee",u=.05,family="Campanulaceae",area="EN",hue="UV+Blue"):
    return {
      "source_original_docx_tableS1_row_1_based":"3",
      "GBIF_accepted_species_key_or_unknown":str(key),
      "GBIF_strict_match_status":"EXACT_CONFIDENT_SPECIES_MAPPED",
      "source_average_UV_reflection_proportion_or_unknown":str(u),
      "source_pollination_system_literal":guild,
      "source_colour_hue_category_literal":hue,
      "source_family_literal":family,
      "source_geographic_area_category_literal":area,
    }

class NumericUVAggregateGuildQualities(unittest.TestCase):
    def test_same_taxon_source_pair_collapse_and_no_fake_bullseye(self):
        x=[sample(1,u=.05),sample(1,u=.17,hue="UV-Blue"),sample(2,"bird",.03)]
        rows=collapse_species(x,expected_source_n=3,strict=False)
        self.assertEqual(len(rows),2)
        uv=next(r for r in rows if r["accepted_GBIF_species_key"]=="1")
        self.assertAlmostEqual(uv["mean_original_source_UV_reflectance"],.11)
        self.assertEqual(uv["source_original_reflectance_range"],[.05,.17])
        self.assertEqual(uv["number_original_source_measurement_rows"],2)
        self.assertTrue(uv["NOT_spatial_UV_pattern"])
        self.assertFalse(uv["original_hue_UV_positive_all"])

    def test_family_guild_difference_and_lack_of_matched_stratum_are_distinct(self):
        x=[sample(1,"bee",.10,"Asteraceae","EN"),
           sample(2,"bird",.02,"Asteraceae","EN"),
           sample(3,"bird",.90,"Rosaceae","N")]
        rows=collapse_species(x,expected_source_n=3,strict=False)
        r=contrasts(rows)
        self.assertEqual(r["source_family_source_within_strata"]["n_with_both_guilds"],1)
        self.assertEqual(r["family_by_area_source_within_strata"]["n_with_both_guilds"],1)
        self.assertAlmostEqual(r["source_family_source_within_strata"][
            "equal_observed_stratum_weight_bee_minus_bird_mean_or_unknown"],.08)
        self.assertTrue(r["source_family_source_within_strata"][
            "no_shared_stratum_not_treated_as_zero"])

    def test_same_key_contradicting_guild_or_family_hard_stop(self):
        with self.assertRaisesRegex(ValueError,"MULTIPLE_ROW_FAMILY_AREA_GUILD_CONFLICT"):
            collapse_species([sample(1,"bee"),sample(1,"bird")],expected_source_n=2,strict=False)

    def test_unresolved_plant_must_not_be_assigned_accepted_id(self):
        u=sample(1);u["GBIF_strict_match_status"]="SOURCE_TAXON_NOT_LEXICAL_BINOMIAL"
        u["GBIF_accepted_species_key_or_unknown"]="5"
        with self.assertRaisesRegex(ValueError,"UNRESOLVED"):
            collapse_species([u],expected_source_n=1,strict=False)

    def test_outside_original_UV_fraction_or_nonoriginal_hue_hard_stop(self):
        with self.assertRaisesRegex(ValueError,"REFLECTION_RANGE"):
            collapse_species([sample(1,u=1.2)],expected_source_n=1,strict=False)
        with self.assertRaisesRegex(ValueError,"NOT_ORIGINAL_UV_CLASS"):
            collapse_species([sample(1,hue="Blue")],expected_source_n=1,strict=False)

if __name__=="__main__":
    unittest.main()
