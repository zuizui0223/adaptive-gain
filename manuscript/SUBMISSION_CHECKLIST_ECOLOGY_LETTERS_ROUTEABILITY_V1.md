# Ecology Letters submission checklist — routeability v1

Date: 2026-10-04  
Target: *Ecology Letters* — Letter  
Canonical manuscript: `manuscript/MANUSCRIPT_RELATIONAL_ROUTEABILITY_V0_4_INFORMATION_ACCESS.md`

## Scientific surface

- [x] Primary ecological question is explicit: when does ecological diversity become effective decision complexity?
- [x] Complete-Shannon nonidentification is the main theorem.
- [x] Exact target-relevant state/query redundancy is retained as supporting mathematics.
- [x] Common finite-budget window (C_A\le B<C_F) is explicit.
- [x] Temporal predictive routing is the only secondary main-text theorem.
- [x] Nonlinear eco-evolutionary no-go is retained in Supplement, not as a competing headline.
- [x] *Bombus* is one quantified example, not the study organism or unique empirical anchor.
- [x] Parasitoid host finding, predator avoidance and patch foraging establish cross-system scope.
- [x] Existing data are not described as direct validation of the exact (C_A<C_F) theorem.
- [x] V5 remains retired as a standalone submission.

## Claim firewalls

- [x] No novelty claim for sequential choice.
- [x] No novelty claim for decision trees / separating systems.
- [x] No novelty claim for costly/adaptive feature acquisition.
- [x] No novelty claim for PID/synergy.
- [x] No claim that Shannon information is generally uninformative.
- [x] Complete-Shannon product amplification is explicitly additive and does not claim an unbounded fixed-binary-action separation.
- [x] Minimal noisy temporal result is not generalized to arbitrary stochastic expected-loss problems.
- [x] Cross-system examples are biological scope evidence, not theorem validation.

## Controlled counts

- [x] Abstract: 150 words.
- [x] Main text: approximately 4,363 words.
- [x] Main-text references: 29.
- [x] Every main bibliography reference is cited in the main manuscript; Yuan et al. 2026 is Supplementary-only with a local full citation.
- [x] Main figures: 2.
- [x] Main tables: 0.
- [x] Text boxes: 0.

## Mathematical verification

- [x] Complete-Shannon twins independently reimplemented:
  `validation/independent_section5_audit_v1.json`.
- [x] One-copy costs: (C_F=(4,4)), (C_A=(4,3)).
- [x] Two-copy costs: (C_F=(8,8)), (C_A=(8,6)).
- [x] Temporal perfect-cue formula independently enumerated:
  (G_{\rm time}=|2\rho-1|/4).
- [x] Noisy temporal factorization independently enumerated on 45 exact rational parameter triples:
  (G_{\rm noisy}=|2\rho-1|(2a-1)(2b-1)/4).
- [x] Independent temporal audit:
  `validation/independent_temporal_routing_audit_v1.json`.
- [x] Two-sided structural factorization is retained in Supplement.
- [x] Exact-balanced finite/extremal mathematics is assigned to the mathematical companion.
- [x] Routing population and OU/inference mathematics have explicit separate-paper/archive destinations.

## Repository / CI

- [ ] Final content-head GitHub Actions run completes successfully on Python 3.10, 3.11 and 3.12.
- [x] Surface tests guard abstract/main-text/reference counts.
- [x] Surface tests guard complete-Shannon claim ceiling.
- [x] Surface tests guard temporal-routing result.
- [x] Witness audit and certificate-ladder audit are part of the full workflow.

## Figures and rendering

- [x] Figure 1: complete Shannon equivalence versus adaptive accessibility.
- [x] Figure 2: finite budget + temporal predictive routing + peer-reviewed Spaethe example + cross-system scope + prospective causal test + measurement rule.
- [x] Figure 2 does not label *Bombus* as the unique empirical anchor and contains no Yuan preprint panel.
- [ ] Render final manuscript PDF and inspect equations, line breaks, figure legibility and legend consistency.
- [x] Canonical SVGs rendered at 1600×950 and 1000px proxy; no clipping, overlaps, broken glyphs or stale Yuan/Chow/empirical-anchor labels detected.
- [x] Inspect both SVG figures at publication-size rendering.

## Data and code accessibility

- [x] External public-data provenance is recorded.
- [x] Independent theorem verification assets are listed.
- [x] Temporal-routing code/tests/receipts are listed.
- [ ] Freeze the exact submitted repository state.
- [ ] Create permanent archive / DOI for that state.
- [ ] Replace `[PERMANENT DOI]` in Data Accessibility.
- [ ] Replace `[SUBMITTED COMMIT SHA]` in Data Accessibility.

## Journal submission fields

- [x] Running title is under 45 characters.
- [x] Eight keywords are supplied (journal permits up to 10).
- [ ] Supply e-mail address for every author.
- [ ] Prepare recommended and opposed reviewer list.
- [ ] Prepare recommended/opposed editorial-board conflict list with reasons for conflicts.
- [ ] Graphical abstract is deferred: Wiley requires it at major/minor revision rather than initial submission.

## Author-controlled fields

- [ ] Final author list/order.
- [ ] Publication spelling of all author names.
- [ ] Affiliations.
- [ ] Corresponding author.
- [ ] Correspondence address/e-mail/telephone.
- [ ] ORCIDs.
- [ ] Funding statement.
- [ ] Competing interests.
- [ ] Author contributions.

## Upload gate

Do not upload until all unchecked items above are resolved.

No further theorem hunting or broad public-data search is part of the initial
submission route.
