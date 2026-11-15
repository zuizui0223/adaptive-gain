# Stage32 — UV-manipulation original workbook retrieval status and noninference gate

**2026-11-15. Operational source check, NOT a completed experimental-effect extraction.** This Draft is stacked on Stage31 PR #110 and does not change Stage22–31 frozen claims, V5/V6, or main.

## Author primary dataset
Koski & Ashman 2014, Dryad DOI 10.5061/dryad.bm558, original UV bullseye field experiment, expected workbook FEKoskiSF2.xlsx. Stage32 implements an isolated, read-only Dryad archive and OOXML workbook-name metadata check with synthetic regression tests. It never exports raw author trial data, and it refuses to treat worksheet count or cell count as a count of independent flowers, pollinators or arrays.

## Actual source-access outcome

**NO_GO_DRYAD_UPSTREAM_DOWNLOAD_UNAVAILABLE.**

At 2026-11-15, the GitHub Actions runner's official Dryad v2 dataset ZIP request to

    https://datadryad.org/api/v2/datasets/doi%3A10.5061%2Fdryad.bm558/download

returned **HTTP 401**. This status was caught, logged, and written as a reproducible source-acquisition no-go receipt on the Stage32 dedicated workflow. It must NOT be described as successful retrieval of the original Excel file, verification of sheet contents or an effect estimate. The original workbook bytes and experiment denominators are not available in the project yet.

## Delivered source-gated software

- dryad_original_structure_probe.py — download status capture, ZIP file whitelist, SHA-256 for obtained packages, OOXML sheet-name metadata only (if a valid original file becomes available), explicit zero effect estimates and source unavailability state.
- test_dryad_original_structure_probe.py — seven source-free tests including intentionally fake in-memory OOXML archives and HTTP-401 failure recording, without presenting synthetic sheet names as actual original workbook information.
- Dedicated GitHub Actions workflow — source-free tests and *attempted* official API acquisition; source metadata JSON artifact only. Full repository Python 3.10–3.12 validation is a separate gate.
- The target stimulus comparison remains UV bullseye versus spatially different UV manipulation at original independent-array grain, but NO effect or standard error can be extracted before authentic workbook contents are inspected.

## Next source-resolution route

A browser-authorized Dryad download, a published DOI-linked file landing page with a direct lawful original-file link, or an original file with source receipt can be used in the next attempt. Pin file bytes and verify the true experimental observation grain before any quantitative model. Do not guess a Dryad download endpoint or fabricate a treatment table.

**STOP:** No observed stage-specific UV/landing benefit, cognition effect, bee foraging gain, or plant fitness inference arises from the Stage32 workflow. Current research direction is expanded in the successor study, which tests cognition and signal use as independent moderators of plant pollination efficiency.
