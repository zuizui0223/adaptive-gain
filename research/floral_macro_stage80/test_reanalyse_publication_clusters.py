import unittest
from reanalyse_publication_clusters import publication_id

class PublicationIdentityTests(unittest.TestCase):
    def test_publisher_declared_habitat_split(self):
        self.assertEqual(publication_id('23_Holzschuh'),publication_id('25_Holzschuh'))
        self.assertEqual(publication_id('24_Holzschuh'),publication_id('23_Holzschuh'))
    def test_same_author_not_automatically_same_paper(self):
        self.assertNotEqual(publication_id('4_Marini'),publication_id('5_Marini'))
        self.assertNotEqual(publication_id('5_Marini'),publication_id('6_Marini'))
    def test_non_split_preserves_label(self):
        self.assertEqual(publication_id('16_Manincor'),'16_Manincor')
        self.assertEqual(publication_id('9_Heleno'),'9_Heleno')

if __name__=='__main__':unittest.main()
