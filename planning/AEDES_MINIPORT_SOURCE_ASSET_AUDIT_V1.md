# Upstream Miniport construction asset audit v1

## Purpose

Pin the exact public source assets referenced by the NPYLR7 papers so the local apparatus is built from the original construction files rather than reconstructed from prose or memory.

This audit does not copy or modify the upstream binary design files.

## Canonical upstream repository

Repository:

`VosshallLab/Miniport-Construction`

Default branch:

`master`

Repository was created in 2018 and is the construction repository explicitly cited by the Miniport methods used in the NPYLR7 studies.

## Upstream files confirmed

The current `master` tree contains:

1. `Instruction Sheet for Printing Miniport Parts.docx`
   - blob SHA: `69f0eb4d7311f51eb9414b6763dea3edb01723fb`
   - size: approximately 1.84 MB

2. `Miniport 3mm Components_FINAL.ai`
   - blob SHA: `01a94338081ee52451e9ec8d9c585d02916a6178`
   - size: approximately 62 KB

3. `Miniport 6mm Components_FINAL.ai`
   - blob SHA: `2ae23dca7b2038c4ac688beb54a65361a7bc1ce0`
   - size: approximately 96 KB

4. `Visual Instruction Manual for Miniport Construction.pptx`
   - blob SHA: `404a7a73febb9c42ae6b4d0c88ce8d770e75bbc4`
   - size: approximately 3.13 MB

5. `README.md`
   - blob SHA: `7c613afcbd69588c4f459258f411355b7e2d232b`

## Build rule

For local Miniport fabrication:

- obtain the 3 mm and 6 mm component design files from the upstream repository at the pinned blob versions above;
- follow the upstream printing / construction instructions and visual manual;
- record any unavoidable material or fabrication substitution before apparatus qualification;
- do not change dimensions because the local build is difficult, then compare the resulting device to the published Miniport as if it were equivalent;
- if CAD / fabrication adaptation is necessary, qualify the adapted apparatus using the full frozen environmental-control gate before compounds are opened.

## Why the prose SOP remains necessary

The upstream construction repository specifies physical fabrication, while `AEDES_MINIPORT_REPLICATION_SOP_V1.md` specifies the 2024 biological-use contract:

- feeding formulation and timing;
- 48 h post-meal behavior;
- CO2 flow;
- human odor handling;
- 5 min test duration;
- day-level environmental QC;
- locked compounds and interpretive controls.

Both are required. A faithfully fabricated apparatus does not automatically imply a qualified biological assay.

## Readiness status

`UPSTREAM_CONSTRUCTION_ASSETS_IDENTIFIED = YES`

`UPSTREAM_BINARY_ASSETS_LOCALLY_REVIEWED = NO`

`LOCAL_MINIPORT_BUILT = NO`

`LOCAL_MINIPORT_QUALIFIED = NO`

The binary source assets were confirmed through GitHub metadata; their full DOCX/PPTX/AI contents were not parsed through the current connector path. Physical fabrication should use the upstream files directly rather than re-authored local copies.
