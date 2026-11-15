"""Mock-only regression tests: no synthetic bee counted as biological evidence."""
import csv
import io
import math
import unittest

from preprocessing_sensitivity import (
    CUTOFFS,SPEED_METHODS,matched_by_bee,
    reconstruct_all_filters,summarize
)

HEADER=tuple(f'pt{i}_{axis}' for i in range(1,8) for axis in 'XYZ')


def artificial_constant_speed(n=240, velocity=.30):
    out=io.StringIO()
    wr=csv.writer(out)
    wr.writerow(HEADER)
    for i in range(n):
        x=.08-velocity*i/1000.
        row=[
          (x+.001,0,0),(x,0,0),(x-.001,0,0),
          (math.nan,)*3,(math.nan,)*3,(math.nan,)*3,
          (0,0,0) if i==0 else (math.nan,)*3
        ]
        wr.writerow([a for p in row for a in p])
    return out.getvalue().encode('utf8')


class Stage41Tests(unittest.TestCase):
    def test_source_free_fixed_velocity_all_six_methods(self):
        vals=reconstruct_all_filters(artificial_constant_speed(),header=HEADER)
        self.assertEqual(len(vals),6)
        for key,three in vals.items():
            self.assertIsNotNone(three,key)
            self.assertAlmostEqual(three[0],.30,delta=.01)
            self.assertAlmostEqual(three[1],.30,delta=.01)
            self.assertAlmostEqual(three[2],0,delta=.02)

    def test_zero_static_landmarks_rejected(self):
        rows=list(csv.reader(artificial_constant_speed().decode().splitlines()))
        rows[1][-3:]=['nan','nan','nan']
        out=io.StringIO()
        csv.writer(out).writerows(rows)
        with self.assertRaisesRegex(ValueError,'NO_GO_NO_SINGLE_STATIC'):
            reconstruct_all_filters(out.getvalue().encode(),header=HEADER)

    def test_unmatched_flower_cells_do_not_enter_pair(self):
        key=(100,'three_tag_mean')
        rows=[]
        for b in ('1','2'):
            for w,near in [('W0',.1),('W1',.2)]:
                rows.append({'B':b,'S':'0','P':'0','W':w,
                             'values':{key:(.2,near,near-.2)}})
        rows.append({'B':'1','S':'0','P':'1','W':'W1',
                     'values':{key:(.2,9.,8.8)}})
        got=matched_by_bee(rows,'three_tag_mean',100,1)
        self.assertEqual(len(got),2)
        for value in got:self.assertAlmostEqual(value,.1)

    def test_non_original_file_counts_hard_stop(self):
        with self.assertRaisesRegex(ValueError,'NO_GO_ORIGINAL_ARCHIVE_GRAIN'):
            summarize([{'W':'W0'}]*157)

    def test_six_specifications_precommitted(self):
        self.assertEqual(CUTOFFS,(50,100,150))
        self.assertEqual(SPEED_METHODS,('three_tag_mean','point2_only'))


if __name__=='__main__':
    unittest.main()
