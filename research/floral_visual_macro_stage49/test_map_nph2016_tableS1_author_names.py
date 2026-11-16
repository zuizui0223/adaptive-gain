"""Original study S1/S2 botanical taxonomy mapping: synthetic tests."""
import unittest
from map_nph2016_tableS1_author_names import (
 s1_author_name_index,source_match_rows
)

def row(code):
    return {"original_taxon_code":code}

class Original2016Names(unittest.TestCase):
    def test_original_S1_full_genus_authoritative_namespace(self):
        names={3:"Table S1\nPotentilla adscharica \nIvesia lycopodioides var. foo\n",
               4:"Duchesnea indica \nDrymocallis glandulosa\n"}
        ids,full=s1_author_name_index(names)
        self.assertEqual(ids[("P","adscharica")],{"Potentilla"})
        self.assertEqual(ids[("I","lycopodioides")],{"Ivesia"})
        out,r=source_match_rows([
            row("P_adscharica"),
            row("I_lycopodioides_megalopetala"),
            row("D_indica"),
            row("D_glandulosa")],ids)
        self.assertEqual(r["n_full_author_binomial_lexical_candidates"],4)
        self.assertEqual(out[0]["original_S1_author_full_binomial_candidate"],
                         "Potentilla adscharica")
        self.assertEqual(out[1]["original_S1_author_full_binomial_candidate"],
                         "Ivesia lycopodioides")
        self.assertEqual(out[1]["S1_multiple_source_infraspecific_tokens"],1)

    def test_ambiguous_D_genus_never_guessed(self):
        idx={("D","test"):{"Duchesnea","Drymocallis"}}
        out,r=source_match_rows([row("D_test")],idx)
        self.assertEqual(r["n_S1_ambiguous_genus_candidates"],1)
        self.assertEqual(out[0]["original_S1_author_full_binomial_candidate"],"")

    def test_no_source_S1_name_not_trait_absence(self):
        out,r=source_match_rows([row("H_unknown")],{})
        self.assertEqual(out[0]["S1_source_match_status"],
                         "NO_AUTHOR_S1_NAME_MATCH_NOT_ABSENT")
        self.assertEqual(out[0]["GBIF_accepted_species_key"],"NOT_QUERIED")

    def test_duplicate_source_infraspecific_is_not_two_distinct_species(self):
        ids={("I","lycopodioides"):{"Ivesia"}}
        out,r=source_match_rows([
          row("I_lycopodioides_megalopetala"),
          row("I_lycopodioides_scandularis")
        ],ids)
        self.assertEqual(r["unique_full_binomial_source_name_count"],1)
        self.assertEqual(
          r["original_source_binomials_with_multiple_infraspecific_source_traits"],
          {"Ivesia lycopodioides":2})

if __name__=="__main__":
    unittest.main()
