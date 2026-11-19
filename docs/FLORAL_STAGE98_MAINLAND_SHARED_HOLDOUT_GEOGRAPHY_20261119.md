# Stage98 — source-only polygon contact audit of mainland floral holdout

2026-11-19 JST. This geography-only source integrity stage stacks on Stage97 #176. No wind, plant traits, Bombus or signal outcomes are read, and main is unchanged.

## The research design problem

Stage94 derived a strict original natural-mainland TDWG3 region cohort: 125 mainland, 120 island and 122 mixed/ineligible source regions. The 125 source regions were frozen into 88 exploration regions over 18 broad spatial blocks and 37 holdout regions over five disjoint blocks, by source geographic geometry only.

**Different spatial block IDs do not prove a nonzero physical distance between train and test geography**. A holdout and exploration polygon may share a boundary, or even overlap due to botanical source geography. Spatially independent prediction claims require auditing the original polygons, before any wind/cue outcome is tested.

## Original geographical sources and estimand

Source-frozen inputs:
- Stage94 original geo registry and split, GitHub Actions artifact 14529576121, ZIP SHA256 3475b544d0530e5dfa71b6324f80055d98971d1a3c364309596a381ea025d833.
- Original TDWG WGSRPD level3.geojson, Git blob SHA1 91104e5159e31f88154833a51d3b0d1c9271083f. Use the same original make-valid policy for 19 originally invalid source features as Stage87/94.

For every one of the 37 holdout regional polygons, compare against all 88 exploration polygons, exactly 3,256 source geographic pairs. Count original WGS84 polygon contact, touching, and overlapping; report the nearest source original exploration polygon. Noncontact approximate kilometres are calculated by selecting planar WGS84 polygon nearest points and converting the two points with WGS84 Geod; the conversion gives a useful **approximate boundary-gap diagnostic, not a guaranteed exact shortest geodesic distance** for irregular regions, polar shapes and antimeridian cases.

A source exact contact or overlap is an unambiguous no-buffer warning, even when source block IDs are disjoint. Never claim a fully verified 100-km holdout buffer based on this approximate point construction. If any contact exists, the fixed shared holdout must be described as geographic *block* validation, not independent buffer validation, and any later confirmed ecological model should predeclare a source-based buffer exclusion sensitivity without modifying observed effects.

## Outputs and limits

- Original 37 holdout region-by-source nearest border table.
- All original train/test region pairs that geometrically touch or overlap.
- Summary receipt with exact original region counts, contact and approximated distance range, no guessed signal direction.
- Geographic-source fingerprint and no cue/outcome access.
- No ERA5 1991-2020 original hourly 10fg CDS source acquired here; climate still has only source-sampled points from Stage95C/97 and no land-area regional gust integration.
- No regression coefficient, plant trait prevalence, bee information order, adaptation or evolutionary generality claim.

All numbers remain unavailable until real source GitHub Actions succeeds.

## Implementation

research/floral_macro_stage98/original_TDWG3_shared_holdout_polygon_contact_audit.py
research/floral_macro_stage98/test_original_TDWG3_shared_holdout_polygon_contact_audit.py
.github/workflows/floral-stage98-original-TDWG-heldout-polygon-contact.yml
