"""Invented IDs demonstrate overlap dedup and visual phenotype unknowns."""
import unittest
from merge_original_multimodal_visual_accepted_species import combine

def data():
    uv=[]
    for i in range(1,263):
        state=("1" if i<=101 else "0" if i<=230 else "")
        uv.append({
            "gbif_accepted_species_key":str(i),
            "source_measured_UV_spatial_pattern_or_missing":state,
            "source_study_DOIs":"doi:mock_direct" if state else "doi:mock_temporal"
        })
    ohashi=[]
    ids=list(range(100,307))+list(range(100,112))
    for i,key in enumerate(ids):
        ohashi.append({
           "gbif_accepted_species_key_or_missing":str(key),
           "gbif_name_taxonomic_mapping_status":"EXACT_CONFIDENT_SPECIES_MAPPED",
           "original_2015_spectral_taxon_folder":f"Mockus_sp_{i}"
        })
    review=[]
    ids=list(range(200,324))+[None]*12
    for key in ids:
        review.append({
           "gbif_accepted_key_or_unresolved":str(key) if key is not None else "",
           "gbif_exact_species_match_status":(
              "EXACT_CONFIDENT_SPECIES_MAPPED" if key else "SOURCE_REVIEW_NAME_NOT_RESOLVED"
           )
        })
    return uv,ohashi,review

class MultimodalSourceExactUnion(unittest.TestCase):
    def test_same_accepted_key_not_counted_three_times(self):
        out,res=combine(*data())
        self.assertEqual(len(out),323)
        self.assertEqual(res['n_total_unique_accepted_species_all_3_modalities'],323)
        self.assertEqual(res['n_accepted_species_in_all_3_sources'],63)
        self.assertEqual(res['overlap_UV_Ohashi'],163)
        self.assertEqual(res['overlap_UV_review'],63)
        self.assertEqual(res['overlap_Ohashi_review'],107)
        self.assertTrue(res['original_review_positive_only_no_nonchanging_negative_comparators'])
        self.assertTrue(res['original_2016_UV_uniform_not_entire_visual_signal_absence'])

    def test_unmeasured_direct_UV_and_undetermined_age_perceptibility_are_unknown(self):
        out,res=combine(*data())
        a=next(x for x in out if x['gbif_accepted_species_key']=='300')
        self.assertEqual(a['direct_UV_2016_2021_pattern_or_missing'],"")
        self.assertEqual(a['Ohashi_bee_perceptible_age_colour_change'],
                         "NOT_CLASSIFIED_FROM_ORIGINAL_SPECTRA_DIRECTORY")
        self.assertTrue(a['no_all_modality_signal_absence_inferred'])

    def test_source_262_denominator_guard(self):
        uv,ohashi,review=data()
        with self.assertRaisesRegex(ValueError,"NO_GO_ORIGINAL_MODALITY_SOURCE_DENOMINATOR"):
            combine(uv[:-1],ohashi,review)

if __name__=="__main__":unittest.main()
