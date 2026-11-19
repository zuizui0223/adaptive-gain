# Stage94 — Source-driven mainland-only regional eligibility for global floral cue biogeography

2026-11-19 JST. This is a geographic-source audit, NOT a gust-flower regression. Draft stacked on Stage93 #172; main unchanged.

## Problem and goal

The existing WCVP native floras comprise 55,775 strict accepted species across 367 TDWG botanical-region units, INCLUDING islands. Some TDWG3 units are entirely islands; some contain mainland and offshore island land. Species records cannot be assigned to local polygons inside mixed TDWG3 units without an actual site locality.

The aim is to prefreeze a conservative source-only mainland region frame and identical geographical exploration/holdout block partition for each of three separate signal endpoints (textual marking, measured flower diameter, original botanical floral scent). It cannot create biological trait-negative observations or pollinator causal mechanisms.

## Grounded geometry sources

1. Original TDWG WGSRPD Level 3 geographic data, exact Git blob SHA1 91104e5159e31f88154833a51d3b0d1c9271083f, with 19 original invalid features explicitly repaired by the already audited Stage87C spatial parser.
2. Natural Earth 10m physical land polygons including major islands, version 5.1.1, NACIS source https://naciscdn.org/naturalearth/10m/physical/ne_10m_land.zip, independently reported ZIP SHA256 e547d749445eaa0964aba76738090ec88f5e63c4585122170f98c67a7ea922dc. Original archive byte verification is mandatory.
3. Original Stage91B real source 367-TDWG regions, GitHub Actions derived artifact 14526435551 SHA256 f1197a050d110d1e3626ab01f3c5d49626ac32fd0588d41ce3a162b44d921cdf. Region keys are read without selecting on plant cue responses.

## Fixed mainland classification

Dissolve Natural Earth component polygons into physically connected land components. Declare six pre-outcome geographic anchors: Eurasia 72E 46N, Africa 20E 12S, North America 103W 40N, South America 60W 15S, Australia 134E 26S, Antarctica 0E 80S. Verify that large ISLANDS (Greenland, Madagascar, Great Britain and Bali) are not selected as mainlands; size by itself does not confer continental status.

For each original TDWG3 polygon, intersect actual physical land areas in the region with the selected mainland and other island components. Compute geodesic areas, preserve the original region shape hash and source-repaired status. Declare strict mainland when mainland land area is at least 5 km2 with less than 0.1 km2 of nonmainland island area (coastline discrepancy tolerance), island when substantially island land without any mainland, mixed otherwise. Mixed and tiny/ambiguous areas are excluded completely rather than assigning island species to mainland. A region with mainland-dominant area is NOT enough to enter the strictly mainland-only sample.

A mainlands-only region gets a block ID from 20-degree latitude by 45-degree longitude fixed bins based on the original region representative position. The existing Stage91 source-blind frozen salt assigns each block to exploration or held-out, reused for all three independently estimated signal endpoints. Spatial block separation, exact region boundary cross-dataset mismatch and retained source lineage breadth still require explicit inspection; hashing alone never establishes a geographic buffer.

The entire operation is geographic, not selected using gust, signal, Bombus or flower colour outcomes. No ecology result may be reported as a wind adaptation from this audit.

## Files

- research/floral_macro_stage94/original_tdwg_naturalearth_strict_mainland.py
- research/floral_macro_stage94/test_original_tdwg_naturalearth_strict_mainland.py
- .github/workflows/floral-stage94-tdwg-naturalearth-mainland-only.yml

Until successful original-source processing, report exact mainland/island/mixed counts as UNKNOWN. The planned 1991-2020 ERA5 primary daily maximum 10m gust above 15 m/s still has not been recovered at full floristic spatial coverage.
