# V6 reproducible main figure artifact — first machine-generated pass

Status: THREE main figures generated successfully as editable SVGs from
frozen theorem computations and independently audited public mosquito
source-data receipts. **Not yet visually signed off for submission.**

- Pull request: https://github.com/zuizui0223/adaptive-gain/pull/67
- Figure workflow: https://github.com/zuizui0223/adaptive-gain/actions/workflows/v6-figures.yml
- Successful run: https://github.com/zuizui0223/adaptive-gain/actions/runs/37801453765
- Run HEAD: 6701bae91f492349c5dc213820dac8df633a5227
- Artifact: evolution-letters-v6-figures
- GitHub artifact id: 11560717072
- Recorded digest: sha256:c9cc5cc5fe530b583c8701016995ee3af241d33b8acc5f2a5d1e3a07ad7fe068
- Artifact expires: 2027-01-06 UTC (per GitHub's artifact response, check actual UI).
- Content: three SVGs, source-derived CSVs, Chandel timing JSON,
  numerical manifest and SVG SHA-256 manifest (11 files).

## Generation and verification

Run from the cloned repository root:

    python -m scripts.render_v6_figures --output-dir v6_figures

The script calls scripts.build_v6_figure_data.build(), which uses the
exact frontier/fitness functions and only existing frozen receipt JSONs.
It does not re-download source datasets or treat a behavioral time-course
as evolutionary fitness.

The corresponding successful GitHub Actions run validated:

1. all three SVG XML documents parse without error;
2. each output contains more than 2,500 UTF-8 bytes;
3. an SVG filename and SHA-256 manifest is emitted;
4. GitHub artifact upload succeeded (11 files).

Reported SVG hashes at that run:
- fig2_robust_no_go.svg:
  9e8769bfc60964241287e2998be7ebef7dfaf77eeea98edd2a37bcbe0b9714e7
- fig3_frequency_and_temporal_anchors.svg:
  dab3b6f951148130a1ef32153f4c351a0ad379b2a592000de8930993eb7a6718

The manifest in the archived artifact is the authoritative record
for *all three* SVGs. Do not manually retouch the released SVGs and
continue claiming they match these hashes; rerun from updated source.

## Non-negotiable human visual check

Machine-valid XML is not publication-ready figure design. Before journal
submission, open each SVG at the final intended figure width and inspect:

- labels/tick spacing, contrast, legibility, colorblind-safe line encoding;
- Figure 1: exactly the highlighted (2,3),(3,7),(4,9) frontiers and
  crossings near mu=.1547 and .6563; h=3 maximizes ratio;
- Figure 2: the vertical arity b (outcomes, not receptors), binary ceiling
  .290085, ternary .386328 and K=.30 example;
- Figure 3: global robust vs expected boundaries are different,
  finite p1 threshold is .6166, Uehara values are one-minute censored
  individual profiles with explicit 8-min right-censor limitations,
  Chandel markers show *aggregate* cumulative effect timing at 46.2/46.5 s
  rather than actual individual latencies;
- labels remain consistent with the final revised legend and journal style;
- figure captions, alt text, and final numerical citations remain accurate;
- externally released public-source data attribution is maintained.

There is **no** claim that these visual encodings were reviewed by a human
or render identically in every external graphics program.

## Submission gates not solved by this figure build

- Last full Python CI must be green at final submission HEAD.
- Prior-art priority for the exact fixed-(n,m,b) *joint attainable
  frontier* still requires critical comparison; the generic fixed
  test-cover and query-set/decsion-tree methods are already known.
- Author names, affiliations, contributions, declarations,
  journal-format adaptation and final scientific approvals remain human tasks.
- No real-world evolutionary selection coefficients or measured
  genetic variation have been inferred from these figures.
