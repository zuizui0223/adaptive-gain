"""Only source-free GBIF semantics; real record count and geometry need original bytes."""
import unittest
from global_gbif_bombus_tdwg3_observed_richness import norm_species,quality
class BombusSourceGuards(unittest.TestCase):
    def test_species_only_not_uncertain(self):
        self.assertEqual(norm_species("Bombus terrestris Linnaeus 1758"),"Bombus terrestris")
        self.assertEqual(norm_species("Bombus lucorum"),"Bombus lucorum")
        self.assertIsNone(norm_species("Bombus spp."))
        self.assertIsNone(norm_species("Bombus"))
        self.assertIsNone(norm_species("Apis mellifera"))
    def test_missing_species_not_a_guild_absence(self):
        a={"decimalLatitude":"52.9","decimalLongitude":"1.1",
           "species":"Bombus sp.","coordinateUncertaintyInMeters":""}
        source,why=quality(a,{"decimallatitude":"decimalLatitude",
                              "decimallongitude":"decimalLongitude",
                              "species":"species",
                              "coordinateuncertaintyinmeters":"coordinateUncertaintyInMeters"})
        self.assertIsNone(source)
        self.assertEqual(why,"UNRESOLVED_OR_NON_BOMBUS_SPECIES")
    def test_zero_coordinates_discarded_and_low_precision_flagged(self):
        c={"decimallatitude":"lat","decimallongitude":"lon",
           "species":"species","coordinateuncertaintyinmeters":"unc"}
        self.assertEqual(quality({"lat":"0","lon":"0","species":"Bombus ruderatus","unc":""},c)[1],"INVALID_OR_ZERO_GEO")
        self.assertEqual(quality({"lat":"52","lon":"1","species":"Bombus ruderatus","unc":"200000"},c)[1],"UNCERTAINTY_OVER_100KM")
        val,status=quality({"lat":"52","lon":"1","species":"Bombus ruderatus","unc":""},c)
        self.assertEqual(status,"ACCEPT")
        self.assertIsNone(val[-1])
if __name__=="__main__":unittest.main()
