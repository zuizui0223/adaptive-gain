"""Independent source-free exact regression invariants; real source CI is separate."""
import tempfile,unittest
from pathlib import Path
import numpy as np
from original_receptor_vs_bee_taxon_audit import (
    publication_id,source_eupp,source_receptor,score_records,
    exclude_taxa_and_recalculate,permute_source_taxon_vectors,
)

class Stage83Guards(unittest.TestCase):
    def test_original_published_study_habitat_split(self):
        self.assertEqual(publication_id("23_Holzschuh"),publication_id("25_Holzschuh"))
        self.assertEqual(publication_id("23_Holzschuh"),publication_id("24_Holzschuh"))
        self.assertNotEqual(publication_id("4_Marini"),publication_id("5_Marini"))
        self.assertNotEqual(publication_id("5_Marini"),publication_id("6_Marini"))
    def test_synthetic_file_is_not_accepted_as_author_spectra(self):
        with tempfile.TemporaryDirectory() as d:
            path=Path(d)/"not-author.zip"
            path.write_bytes(b"not the source")
            with self.assertRaises(ValueError):source_receptor(path)
    def test_synthetic_visitors_are_not_authentic_eupp(self):
        with tempfile.TemporaryDirectory() as d:
            path=Path(d)/"fake.csv"
            path.write_text("Study_id,n_observed_Bombus\ns1,2\n")
            with self.assertRaises(ValueError):source_eupp(path)
    @staticmethod
    def pair():
        b=np.array([8.,2.,0.]);o=np.array([2.,8.,0.]);n=b+o;p=b.sum()/n.sum()
        return {"pub":"A","study":"A","key":("A","N","2022"),"b":b,"o":o,"n":n,
                "N":n.sum(),"p":p,"u":b-n*p}
    def test_local_score_null_identity(self):
        z=np.array([[-1.], [1.], [0.]])
        q=score_records(z,[self.pair()])
        self.assertEqual(int(q["network_counts"][0]),1)
        self.assertAlmostEqual(q["score"][0],-1.2)
    def test_exclusion_recalculates_and_removes_one_taxon_pair(self):
        r=self.pair()
        # two distinct source plants are needed, so dropping either is uninformative
        self.assertEqual(len(exclude_taxa_and_recalculate([r],{0})),0)
        self.assertEqual(len(exclude_taxa_and_recalculate([r],{1})),0)
    def test_permutation_is_not_labeled_phylogenetic_inference(self):
        z=np.array([[-1.], [1.], [0.]])
        x=permute_source_taxon_vectors(z,[self.pair()],reps=20,seed=20261118)
        self.assertEqual(len(x),1)
        self.assertTrue(0<x[0]["species_vector_permutation_two_sided_tail_fraction"]<=1)
        self.assertTrue(0<x[0]["four_signal_maxT_familywise_diagnostic_tail_fraction"]<=1)

if __name__=="__main__":unittest.main()
