# Evolution Letters submission checklist v1

Target: **Evolution Letters — Letter**. Canonical higher-tier manuscript: `MANUSCRIPT_EVOLUTION_LETTERS_V2.md`.

Current journal guidance was checked 2026-09-13 and is recorded in `EVOLUTION_LETTERS_FORMAT_RECEIPT_20260913.md`. Recheck the live journal site immediately before upload.

## Scientific surface

- [x] One principal claim: finite sensing architecture can exclude local eco-evolutionary feedback regimes.
- [x] Nonlinear monotone-Lipschitz no-go theorem merged to main.
- [x] State-specific gap `g_i` separated from between-state contrast `Delta g`.
- [x] Linear acquisition-cost lift retained only as constructive special case.
- [x] Necessary-versus-sufficient firewall explicit.
- [x] Evolution Letters V2 manuscript surface exists.
- [x] Three canonical main figures exist as separate SVG files.
- [x] V2 figure legends exist.
- [x] Current Theoretical Ecology manuscript/package remains intact as fallback.
- [ ] Latest full CI passes after the V2 semantic/figure commit.

## Journal-format surface

Machine-enforced in `tests/test_evolution_letters_surface.py`:

- [ ] title <=30 words;
- [ ] teaser <=150 words;
- [ ] abstract <=300 words;
- [ ] <=10 keywords;
- [ ] Introduction / Methods / Results / Discussion / References present;
- [ ] main Letter text <=5,000 words under repository counting rule;
- [ ] `g_i=C_F(i)-C_A(i)` and `Delta g=g_2-g_1` remain distinct.

Figure validation in `tests/test_evolution_letters_figures.py`:

- [ ] canonical SVGs parse as valid XML;
- [ ] Figure 1 distinguishes state gap from between-state contrast;
- [ ] Figure 1 labels the post-threshold region `not ruled out`, not guaranteed;
- [ ] Figure 2 derives a high-gap state from the required contrast and preserves q=2/q=3 examples;
- [ ] Figure 3 preserves reward-mode-alignment interpretation.

## Author-controlled metadata — HARD STOP

Do not infer these from Git, account metadata, unrelated grants or earlier projects:

- [ ] final author names and order;
- [ ] final affiliations;
- [ ] corresponding author name/address/email;
- [ ] ORCID(s) if supplied;
- [ ] CRediT author contributions;
- [ ] funding statement;
- [ ] conflict-of-interest statement;
- [ ] acknowledgements if any;
- [ ] no-simultaneous-submission approval from all authors.

## Data/code/archive

- [x] no empirical datasets are claimed for this theoretical paper;
- [x] public code repository exists;
- [ ] mint or identify permanent archive DOI if available before submission;
- [ ] verify that archived release corresponds exactly to the submitted scientific surface;
- [ ] record submitted commit/tree and figure checksums.

## Final visual QA

A human must inspect each rendered figure/PDF before upload:

- [ ] Figure 1 labels readable at journal-page scale;
- [ ] Figure 1 does not visually imply that one `g_i` is itself feedback;
- [ ] Figure 1 does not imply sufficiency after crossing the bound;
- [ ] Figure 2 `(6,5,5)`, `(7,6,6)` and `(8,5,5)` are legible;
- [ ] Figure 3 distinction between persistence and reward alignment is legible;
- [ ] mathematical symbols survive manuscript/PDF conversion;
- [ ] no clipped labels or overlapping text;
- [ ] figure legends match the final files.

## Dispatch-time checks

- [ ] re-open current Evolution Letters author guidelines;
- [ ] confirm Letter article type and current word/abstract/title limits;
- [ ] confirm teaser requirement/status;
- [ ] confirm reference/file conventions;
- [ ] confirm ScholarOne route and required portal declarations;
- [ ] final cover letter approved;
- [ ] all authors approve exact files being submitted.

## Stop rule

Do not reopen theorem development to solve metadata, formatting, portal, or visual-QA problems. Do not add a new theorem family solely to improve perceived journal prestige.
