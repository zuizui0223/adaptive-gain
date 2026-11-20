"""Stage103 authentic WFO botanical source intervals: never invent midpoint/maximum."""
from __future__ import annotations
import tempfile,unittest,zipfile
from pathlib import Path
from original_WFO_wholeflower_size_intervals import source_evidence,aggregate_species
from authentic_WFO_diameter_strict_quality_audit import load_frozen_stage100,load_geographic_frame

def selected(text):
    records,quality=source_evidence(text)
    return records,quality

class OriginalSourceFloralIntervalSemantics(unittest.TestCase):
    def test_actual_WFO_double_dash_range_in_cm(self):
        v,diag=selected("Flowers violet, funnelform, 8--9 cm in diam.")
        self.assertEqual([(r["evidence_type"],r["lower_mm"],r["upper_mm"]) for r in v],
             [("bounded_interval",80.0,90.0)])
        self.assertEqual(diag["admitted_bounded_interval"],1)
    def test_all_dash_range_variants_are_interval_not_point(self):
        for txt in ("Flowers 3–5 mm in diam.","Flowers 3—5 mm across.",
                    "Flowers 3-5 mm wide.","Flowers 3~5 mm in diam.",
                    "Flowers 3 to 5 mm across."):
            v,_=selected(txt)
            self.assertEqual(len(v),1,txt)
            self.assertEqual((v[0]["evidence_type"],v[0]["lower_mm"],v[0]["upper_mm"]),
                            ("bounded_interval",3.0,5.0),txt)
    def test_axis_before_interval(self):
        v,_=selected("Flower diameter 1--2 cm.")
        self.assertEqual([(x["lower_mm"],x["upper_mm"]) for x in v],[(10.,20.)])
    def test_upper_only_is_left_censored_not_a_singleton(self):
        v,_=selected("Flowers to 2 cm in diam.")
        self.assertEqual([(x["evidence_type"],x["lower_mm"],x["upper_mm"]) for x in v],
                         [("upper_limit_only",None,20.0)])
        z=aggregate_species(v)
        self.assertEqual(z["status"],"upper_limit_only_source_NO_lower_bound")
        self.assertIsNone(z["lower_mm"])
    def test_upper_maximum_not_more_than(self):
        v,_=selected("Flowers not more than 1 cm across.")
        self.assertEqual([(x["lower_mm"],x["upper_mm"]) for x in v],[(None,10.)])
    def test_corolla_size_does_not_qualify(self):
        self.assertEqual(selected("Corolla 3--5 mm across.")[0],[])
        self.assertEqual(selected("Corolla 3 mm in diam.")[0],[])
    def test_inflorescence_head_size_not_qualify(self):
        self.assertEqual(selected("Flowers in clusters, heads 3--5 mm across.")[0],[])
        self.assertEqual(selected("Flowers in cymes 2--3 cm in diam.")[0],[])
    def test_exact_single_number_is_degenerate_interval(self):
        v,_=selected("Flowers 7 mm diam.")
        self.assertEqual([(x["evidence_type"],x["lower_mm"],x["upper_mm"]) for x in v],
                         [("exact_source_single_number",7.,7.)])
    def test_source_range_is_not_replaced_by_upper_as_exact(self):
        v,_=selected("Flowers 7--9 mm in diam.")
        self.assertEqual(len([r for r in v if r["evidence_type"]=="exact_source_single_number"]),0)
        self.assertEqual(aggregate_species(v)["status"],"bounded_source_range_or_mixed")
    def test_envelope_source_values_not_confidence_interval(self):
        v=[{"evidence_type":"bounded_interval","lower_mm":4,"upper_mm":9},
           {"evidence_type":"exact_source_single_number","lower_mm":8,"upper_mm":8}]
        a=aggregate_species(v)
        self.assertEqual((a["lower_mm"],a["upper_mm"]),(4,9))
        self.assertTrue(a["original_source_values_envelope_not_CI"])
        self.assertFalse(a["source_envelope_over_5fold_NEEDS_REVIEW"])
    def test_conflicting_ranges_warn_instead_of_faking_precision(self):
        v=[{"evidence_type":"bounded_interval","lower_mm":3,"upper_mm":6},
           {"evidence_type":"bounded_interval","lower_mm":90,"upper_mm":95}]
        a=aggregate_species(v)
        self.assertTrue(a["source_envelope_over_5fold_NEEDS_REVIEW"])
    def test_ambiguous_reversed_or_extreme_range_not_accepted(self):
        self.assertEqual(selected("Flowers 9--8 mm across.")[0],[])
        self.assertEqual(selected("Flowers 100--300 mm across.")[0],[])
    def test_missing_no_size_is_not_0(self):
        self.assertEqual(aggregate_species([]),{"status":"no_eligible_size_evidence","lower_mm":None,"upper_mm":None})
    def test_unverified_stage100_provenance_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/"dummy.zip"
            with zipfile.ZipFile(p,"w") as z:z.writestr("evidence.csv","untrusted")
            with self.assertRaises(ValueError):load_frozen_stage100(p)
    def test_unverified_geographical_split_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/"dummy.zip"
            p.write_bytes(b"not source")
            with self.assertRaises(ValueError):load_geographic_frame(p)

if __name__=="__main__":unittest.main()
