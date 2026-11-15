"""Stage30 scoping-ledger QA. No meta-effect values or invented data.

This test validates only provenance / endpoint-type bookkeeping, not whether
a comprehensive literature review has been completed. The sheet intentionally
keeps primary manipulations separate from review and meta-analysis records.
"""
from __future__ import annotations
import csv
import re
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parent
LEDGER=ROOT/'SEED_EVIDENCE_MAP_20261115.csv'
PROTOCOL=ROOT/'PROTOCOL_PHASED_FLORAL_INFORMATION_META_MACRO_20261115.md'
REQUIRED={
  'study_id','year','source_type','signal_family','mechanism_or_design',
  'decision_stage_or_endpoint','plant_fitness_observed','source_locator',
  'extraction_state'
}


class FloralRouteScopingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with LEDGER.open(newline='',encoding='utf-8') as handle:
            rd=csv.DictReader(handle)
            cls.headings=set(rd.fieldnames or ())
            cls.rows=list(rd)
        cls.proposal=PROTOCOL.read_text(encoding='utf-8')

    def test_explicit_non_quantitative_scoping_grain(self):
        self.assertEqual(self.headings,REQUIRED)
        self.assertGreaterEqual(len(self.rows),18)
        self.assertEqual(len({r['study_id'] for r in self.rows}),len(self.rows))
        self.assertNotIn('effect_size',self.headings)
        self.assertNotIn('standard_error',self.headings)
        for rec in self.rows:
            self.assertTrue(rec['extraction_state'])
            self.assertNotIn('pooled_effect',rec['extraction_state'].lower())
            self.assertTrue(re.match(r'^https://',rec['source_locator']))
            self.assertTrue(rec['year'].isdigit())
            self.assertTrue(1990<=int(rec['year'])<=2026)

    def test_different_prior_art_categories_not_called_primary(self):
        primary=[r for r in self.rows if r['source_type']=='primary_experiment']
        metas=[r for r in self.rows if 'meta_analysis' in r['source_type']]
        reviews=[r for r in self.rows if 'review' in r['source_type']]
        theories=[r for r in self.rows if r['source_type']=='theoretical_model']
        self.assertGreaterEqual(len(primary),7)
        self.assertGreaterEqual(len(metas),2)
        self.assertGreaterEqual(len(reviews),4)
        self.assertGreaterEqual(len(theories),1)
        self.assertTrue(all('source_identified' in r['extraction_state'] for r in primary))

    def test_anchor_primary_causal_and_dynamic_prior_art(self):
        links={r['source_locator'] for r in self.rows}
        for anchor in (
          'https://doi.org/10.1098/rspb.2011.1349',
          'https://doi.org/10.1111/1365-2435.14262',
          'https://doi.org/10.1371/journal.pone.0055914',
          'https://doi.org/10.1098/rspb.2020.2848',
          'https://doi.org/10.1016/j.isci.2023.107093',
          'https://doi.org/10.1111/evo.13639',
          'https://doi.org/10.1093/aob/mcy132'
        ):
            self.assertIn(anchor,links)

    def test_phase_and_plant_fitness_separation(self):
        for token in (
          'distance/initial detection',
          'flower landing',
          'reward discovery',
          'pollen removal',
          'male siring',
          'Do not infer UV reflectance from ordinary RGB images',
          'Do not equate pollinator approach with success',
          'not a completed PRISMA systematic review',
          '10.5061/dryad.bm558',
          '10.5061/dryad.612jm64gq',
          '10.1371/journal.pone.0014287',
        ):
            self.assertIn(token,self.proposal)

    def test_no_universal_ecological_translation_of_stage23_threshold(self):
        self.assertIn("Do not insert Stage23's exact cost thresholds",self.proposal)
        self.assertIn('Do not call the Stage23 cost optimum',self.proposal)
        self.assertIn('Do not manufacture a study-level effect size',self.proposal)
        self.assertIn('The absence of a unified guide-specific stage-value meta-analysis is NOT proven',self.proposal)


if __name__=='__main__':
    unittest.main()
