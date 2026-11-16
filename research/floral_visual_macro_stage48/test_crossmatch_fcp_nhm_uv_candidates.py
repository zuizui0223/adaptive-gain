"""Independent mock-only cross-database species-review queue tests.

The value "0" from a source lexical search is NEVER negative botanical
evidence for a guide. No test specimen, bee or flower is real.
"""
import unittest
from crossmatch_fcp_nhm_uv_candidates import compose_review_registry

def fcp(species,i,n=100,k=60):
    return {'species':species,'inat_taxon_id':str(i),
            'n_source_photo':str(n),'n_classified_photo':str(k)}
def nhm(species,mark):
    return {'taxon':species,'marking_text_review_candidate':int(mark),
            'floral_colour_reported':1}
def uv(species,pattern,cat):
    return {'taxon_as_published':species,'uv_pattern_present':int(pattern),
            'uv_category':cat}

class GlobalOriginalPhotoReviewQueue(unittest.TestCase):
    def test_three_evidence_states_not_conflated(self):
        obs=[fcp('Mockus alpha',1),fcp('Mockus beta',2),
             fcp('Mockus gamma',3,k=5)]
        botanical=[nhm('Mockus alpha',1),nhm('Mockus beta',0),nhm('Mockus delta',1)]
        uvsource=[uv('Mockus beta',1,'BE')]
        q,s=compose_review_registry(obs,botanical,uvsource,
                       expected_source_counts=(3,3,1))
        self.assertEqual(len(q),3)
        self.assertEqual(s['n_NHM_unconfirmed_marking_TEXT_candidates_with_FCP'],1)
        self.assertEqual(s['n_source_UV_measured_name_matches_with_FCP'],1)
        self.assertEqual(q[0]['review_priority'],
                         '2_NHM_VISIBLE_MARKING_TEXT_PLUS_CLASSIFIABLE_PHOTO_REVIEW')
        self.assertEqual(q[1]['review_priority'],
                         '1_ORIGINAL_UV_PHENOTYPE_REFERENCE_AND_PHOTO')
        self.assertEqual(q[1]['uv_original_direct_measured_pattern_or_missing'],1)
        self.assertEqual(q[2]['review_priority'],
                         '4_LOW_CLASSIFIABILITY_OR_OPPORTUNITY_NOT_NEGATIVE')
        for x in q:
            self.assertEqual(x['actual_visible_guide_phenotype'],
                             'NOT_MEASURED_FROM_FCP_PHOTO')
            self.assertEqual(x['actual_UV_guide_phenotype'],
                             'NOT_MEASURED_FROM_FCP_PHOTO')
            self.assertEqual(x['source_pollinator_use_of_pattern'],'NOT_MEASURED')
            self.assertNotEqual(x['flower_guide_survey_inclusion'],'CONFIRMED')

    def test_duplicate_NHM_name_not_silently_overwritten(self):
        q,s=compose_review_registry([fcp('Mockus alpha',1)],
                 [nhm('Mockus alpha',1),nhm('Mockus alpha',0)],[],
                 expected_source_counts=(1,2,0))
        self.assertEqual(q[0]['nhm_exact_name_join_status'],
                         'AMBIGUOUS_NHM_SOURCE_NAME')
        self.assertEqual(q[0]['nhm_visible_marking_TEXT_candidate_or_missing'],'')

    def test_no_source_name_is_not_absence(self):
        q,s=compose_review_registry([fcp('Mockus alpha',1)],[],[],
                              expected_source_counts=(1,0,0))
        self.assertEqual(q[0]['nhm_visible_marking_TEXT_candidate_or_missing'],'')
        self.assertEqual(q[0]['uv_original_direct_measured_pattern_or_missing'],'')
        self.assertTrue(s['all_unobserved_pattern_states_explicitly_NOT_MEASURED'])

    def test_classifiable_count_higher_than_original_rejected(self):
        with self.assertRaisesRegex(ValueError,'NO_GO_CLASSIFIED_GREATER'):
            compose_review_registry([fcp('Mockus alpha',1,n=10,k=90)],[],[],
                                    expected_source_counts=(1,0,0))

    def test_duplicate_fcp_photo_species_id_rejected(self):
        with self.assertRaisesRegex(ValueError,'NO_GO_FCP_SPECIES_OR_TAXON_ID_NOT_UNIQUE'):
            compose_review_registry([fcp('Mockus alpha',1),fcp('Mockus beta',1)],[],[],
                                    expected_source_counts=(2,0,0))

    def test_production_4475_59369_80_source_denominators_required(self):
        with self.assertRaisesRegex(ValueError,'NO_GO_INCORRECT_ORIGINAL_SOURCE_DENOMINATOR'):
            compose_review_registry([fcp('Mockus alpha',1)],[],[])

if __name__=='__main__':
    unittest.main()
