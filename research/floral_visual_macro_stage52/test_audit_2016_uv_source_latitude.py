"""Mock-only original 177-row to 159 accepted species source latitude audit."""
import unittest
from audit_2016_uv_source_latitude import audit


def fake_rows():
    rows=[]
    for i in range(159):
        rows.append({
            "source_measured_UV_pattern_present":str(i%2),
            "accepted_GBIF_species_match_status":"EXACT_CONFIDENT_SPECIES_MAPPED",
            "accepted_GBIF_taxon_key_or_empty":str(10000+i),
            "original_S1_author_full_binomial_candidate":"Potentilla mockus",
            "source_mean_latitude_deg":str(42+i/40),
            "source_mean_UVB_J_per_m2_per_day":str(2000+i),
            "source_mean_annual_temp_C":str(11+i/100),
            "source_mean_annual_precip_mm":"400",
            "source_mean_altitude_m":"600"
        })
    for i in range(5):
        rows.append(dict(rows[i],source_mean_latitude_deg=str(47+i)))
    for i in range(13):
        rows.append({
            "source_measured_UV_pattern_present":"1",
            "accepted_GBIF_species_match_status":"NO_SOURCE_AUTHOR_FULL_NAME",
            "accepted_GBIF_taxon_key_or_empty":"",
        })
    return rows


class SourceOnly2016LatitudeQA(unittest.TestCase):
    def test_source_177_164_159_identity_and_no_occurrence_confusion(self):
        rows,res=audit(fake_rows())
        self.assertEqual(len(rows),159)
        self.assertEqual(res["accepted_source_taxon_rows"],164)
        self.assertEqual(res["accepted_distinct_GBIF_species"],159)
        self.assertEqual(res["source_latitude_sign_counts"]["positive"],159)
        self.assertTrue(res["published_latitude_as_signed_or_unsigned_still_requires_author_source_interpretation"])
        self.assertTrue(res["no_Bombus_or_other_pollinator_fitness_or_richness_effect"])

    def test_infraspecific_conflict_cannot_be_silently_pooled(self):
        rows=fake_rows()
        rows[159]["source_measured_UV_pattern_present"]="1"
        with self.assertRaisesRegex(ValueError,"NO_GO_SOURCE_INFRASPECIFIC_UV_STATE_CONFLICT"):
            audit(rows)

    def test_source_177_is_not_a_populated_GBIF_species_count(self):
        with self.assertRaisesRegex(ValueError,"NO_GO_PUBLISHED_177_ORIGINAL_SOURCE_ROWS"):
            audit(fake_rows()[:-1])

    def test_bad_source_environment_numeric_refused(self):
        rows=fake_rows()
        rows[0]["source_mean_latitude_deg"]="not a latitude"
        with self.assertRaisesRegex(ValueError,"NO_GO_SOURCE_PUBLISHED_FIELD_NONNUMERIC"):
            audit(rows)

if __name__=="__main__":
    unittest.main()
