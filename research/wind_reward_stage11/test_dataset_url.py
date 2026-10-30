import unittest
from source_gate import dataset_url

class DatasetURLTests(unittest.TestCase):
    def test_doi_is_one_path_component(self):
        self.assertEqual(dataset_url('10.5061/dryad.9kd51c608'), 'https://datadryad.org/api/v2/datasets/doi%3A10.5061%2Fdryad.9kd51c608')

if __name__=='__main__': unittest.main()
