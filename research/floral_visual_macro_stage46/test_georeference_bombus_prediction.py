"""Mock DBF/cell joins; zero missing vs modeled absence isolation."""
import struct
import unittest
from unittest.mock import patch
from georeference_bombus_prediction import (
    parse_original_dbf_centroids,join_modelled_bombus_and_centroids
)

def fake_one_record(lon,lat):
    # mocked field schema, actual reader validates from original DBF separately
    fields=[{"name":"CENTRELON","length":12},
            {"name":"CENTRELAT","length":12},
            {"name":"siteid","length":12}]
    head=bytearray(33)
    struct.pack_into("<HH",head,8,33,37)
    row=b" "+f"{lon}".ljust(12).encode()+f"{lat}".ljust(12).encode()+b"HEX101      "
    return bytes(head)+row,{"records":1,"field_schema":fields}

class HexJoinContract(unittest.TestCase):
    def test_parse_original_cell_coordinates_and_codes(self):
        binary,meta=fake_one_record(10.5,46.5)
        with patch("georeference_bombus_prediction._dbf_header",return_value=meta):
            centers,stats=parse_original_dbf_centroids(binary)
        self.assertEqual(centers["HEX101"],(10.5,46.5))
        self.assertEqual(stats["distinct_original_hex_id"],1)

    def test_outside_earth_original_coordinate_fails(self):
        binary,meta=fake_one_record(190,46.5)
        with patch("georeference_bombus_prediction._dbf_header",return_value=meta):
            with self.assertRaisesRegex(ValueError,"NO_GO_HEX_LAT_LON_OUTSIDE"):
                parse_original_dbf_centroids(binary)

    def test_missing_model_cell_is_unknown_not_zero(self):
        geo={"HEX1":(0.,50.),"HEX2":(1.,51.)}
        records,bands=join_modelled_bombus_and_centroids(
            [("HEX1",2,3)],geo)
        byid={x["source_siteid"]:x for x in records}
        self.assertEqual(byid["HEX1"]["n_source_modelled_Bombus_taxa"],2)
        self.assertIsNone(byid["HEX2"]["n_source_modelled_Bombus_taxa"])
        self.assertEqual(byid["HEX2"]["model_support_status"],
                         "NO_SOURCE_BEE_PA_CELL_NOT_TRUE_ABSENCE")
        self.assertEqual(bands[0]["n_cells_with_modelled_bees"],1)

    def test_unmatched_hex_grid_id_fails(self):
        with self.assertRaisesRegex(ValueError,"NO_GO_BEE_PA_SITEID"):
            join_modelled_bombus_and_centroids([("HEX3",2,3)],
                                               {"HEX2":(0.,0.)})

if __name__=="__main__":
    unittest.main()
