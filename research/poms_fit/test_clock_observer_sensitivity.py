import unittest

import numpy as np
import pandas as pd

from clock_observer_sensitivity import (
    CLOCK_BINS, audit_clock, augmented_pair, label_clock, parse_clock
)
from fit_associations import WIND, prepare


class ClockObserverTests(unittest.TestCase):
    def test_exact_clock_formats_and_strict_rejection(self):
        self.assertEqual(parse_clock("09:42"),(582,"clock_24h"))
        self.assertEqual(parse_clock("16:05:33"),(965,"clock_24h"))
        self.assertEqual(parse_clock("3:30 PM"),(930,"clock_12h"))
        self.assertEqual(parse_clock("12:00 am"),(0,"clock_12h"))
        self.assertEqual(parse_clock("12:00 PM"),(720,"clock_12h"))
        for s in ("24:00","09:90","23:30:70","12.30","9 am", " "):
            self.assertIsNone(parse_clock(s)[0])
        self.assertIsNone(label_clock(float("nan")))
        self.assertEqual(label_clock(600),"10_to_12")
        self.assertEqual(label_clock(960),"from_16")

    def test_coverage_and_missing_time_not_imputed(self):
        d=pd.DataFrame({"count_start_time":["08:05","11:45","14:20",None,"nope"]})
        minutes,report=audit_clock(d)
        self.assertEqual(report["parsed"],3)
        self.assertAlmostEqual(report["parsed_fraction"],.6)
        self.assertEqual(report["clock_bin_counts"]["before_10"],1)
        self.assertEqual(report["clock_bin_counts"]["14_to_16"],1)
        self.assertIn("nope",report["unparsed_raw_examples"])
        self.assertTrue(minutes.iloc[3:].isna().all())

    def fixture(self,n=600):
        rng=np.random.default_rng(401)
        wind=rng.choice(WIND,n,p=[.4,.4,.2])
        sites=rng.choice([f"s{i}" for i in range(30)],size=n)
        when=rng.integers(8,19,size=n)
        nbee=rng.binomial(8,1/(1+np.exp(-(.1+.5*(wind==WIND[2])))))
        df=pd.DataFrame({
            "sample_id":np.arange(n),
            "date":pd.Timestamp("2022-05-01")+pd.to_timedelta(rng.integers(0,128,n),unit="D"),
            "year":2022,
            "target_flower_corrected":rng.choice(["Thistle","Clover","Buttercup"],n),
            "floral_unit":rng.choice(["flower head","individual flower"],n),
            "floral_unit_count":rng.integers(2,50,n),
            "wind_speed":wind,
            "sunshine":rng.choice(["Entirely in sunshine","Entirely shaded",
                                   "Partly in sun and partly shaded"],n),
            "location_code":sites,
            "count_start_time":[f"{h:02d}:{int(x):02d}" for h,x in zip(when,rng.integers(0,60,n))],
            "recorder_type":rng.choice(["experienced","new",None],n),
            "flower_cover":rng.choice(["Less than half","About half","Not recorded"],n),
            "bumblebees":nbee,
            "other_flies":8-nbee,
            "all_insects_total":8
        })
        return df

    def test_augmented_model_with_zero_imputation_for_recorder_only(self):
        d,flow=prepare(self.fixture(),"one_km")
        minutes,clock=audit_clock(d)
        self.assertEqual(clock["parsed"],len(d))
        d=d.copy()
        d["clock_bin"]=pd.Categorical([label_clock(x) for x in minutes],
                                       categories=CLOCK_BINS)
        d["recorder_type_audited"]=d["recorder_type"].fillna("__SOURCE_MISSING__").astype(str)
        d["flower_cover_audited"]=d["flower_cover"].fillna("__SOURCE_MISSING__").astype(str)
        result=augmented_pair(d,"one_km")
        self.assertEqual(result["status"],"fitted",result.get("error",""))
        self.assertEqual(result["design_rank"],result["design_columns"])
        self.assertGreater(result["strong_wind_or"],1)


if __name__=="__main__":
    unittest.main()
