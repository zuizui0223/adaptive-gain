# Evolution Letters V3 mathematical integration implementation plan

> For agentic workers: execute this plan task-by-task with verification after each task.

**Goal:** Broaden the Evolution Letters manuscript so the repository's major mathematical results are actively used in one coherent eco-evolutionary argument, without adding new theorem families or weakening the existing claim ceilings.

**Architecture:** Preserve the frozen V2 submission package unchanged. Build a V3 manuscript and V3 Supplement around a five-layer theorem hierarchy: exact adaptive-gain foundation, target-relevant reduction, sharp extremal geometry, dual evolutionary lifts, and temporal/diagnostic consequences. Add a canonical Mathematical Atlas that maps every major theorem family to MAIN/SUPPLEMENT/COMPANION/ARCHIVE status.

**Tech Stack:** Markdown manuscript surfaces, existing Python theorem implementations/tests, GitHub Actions pytest matrix.

**Spec:** `docs/superpowers/specs/2026-09-16-evolution-letters-math-integration-design.md`

## Global constraints

- Do not alter or delete the frozen V2 manuscript, V2 Supplement, validated figures, or V2 readiness ledger.
- Do not create new theorem families.
- Necessary no-go conditions must never be phrased as sufficient conditions.
- Keep finite deterministic architecture distinct from Shannon/mutual information.
- Treat balanced-query unbounded gain as an existence result only.
- Treat the budget-gated selection model as conditional on a biologically justified hard budget.
- Keep kernel theorems within deterministic exact target resolution with positive additive costs and worst-path objective.
- Run the existing full test suite and both repository audits after integration.

---

### Task 1: Create the Mathematical Atlas

**Files:**
- Create: `manuscript/MATHEMATICAL_ATLAS_V1.md`

**Deliverable:** A theorem-by-theorem map covering foundation, reduction/kernel, extremal geometry, evolutionary lifts, temporal filtering, and identifiability, with MAIN/SUPPLEMENT/COMPANION/ARCHIVE disposition and explicit ecological interpretation.

- [ ] Inventory the major theorem notes and their executable/test/validation counterparts.
- [ ] Assign each theorem family a paper role and claim ceiling.
- [ ] Verify that no theorem classified MAIN lacks a direct biological interpretation.
- [ ] Commit the Atlas independently.

### Task 2: Build the V3 main manuscript

**Files:**
- Create: `manuscript/MANUSCRIPT_EVOLUTION_LETTERS_V3.md`

**Deliverable:** A V3 manuscript that retains the V2 nonlinear no-go spine and adds two mathematically substantive biological results: the exact adaptive-only budget window/budget-gated selection lift, and the exactly-balanced-query unbounded-gain structural counterexample.

- [ ] Preserve all V2 scope limitations and references.
- [ ] Add the exact foundation `C_A<=C_F` and `C_A<=B<C_F` near the finite-sensing definitions.
- [ ] Add a Results subsection showing why exact global cue balance does not bound adaptive gain: `C_F/C_A >= 2^d/(d+1) -> infinity` under exactly balanced binary unit-cost queries.
- [ ] Add a Results subsection deriving the hard-budget selection regions and the adaptive-only selection window.
- [ ] Connect both additions to the existing nonlinear no-go theorem rather than presenting them as independent headlines.
- [ ] Keep the sharp binary/Pareto threshold, spectral recurrence, and feedback diagnostic.
- [ ] Measure title, abstract, teaser, keyword, and main-text word counts against the current Letter guidance recorded in the repository.

### Task 3: Expand the V3 Supplement

**Files:**
- Create: `manuscript/SUPPLEMENT_EVOLUTION_LETTERS_V2.md`

**Deliverable:** A proof-and-reproducibility supplement aligned to V3, with dedicated sections for target-relevant quotient/kernel results and the balanced-unbounded construction in addition to the V2 theorem spine.

- [ ] Add an exact-adaptive-gain foundation section.
- [ ] Add world-twin/query-dominance/two-sided-kernel sections with exact preservation statements.
- [ ] Add the balanced binary unbounded family, with its existence-only claim ceiling.
- [ ] Add the budget-gated selection derivation and natural-history budget interpretations.
- [ ] Retain nonlinear no-go, finite architecture, spectral recurrence, and feedback-identifiability sections.
- [ ] Point detailed solver/certificate machinery to repository-level proof support rather than duplicating it.

### Task 4: Add V3 regression checks

**Files:**
- Create: `tests/test_evolution_letters_v3_surface.py`

**Deliverable:** Text-level firewalls ensuring the expanded manuscript contains the intended mathematics and preserves its scope boundaries.

- [ ] Assert that V3 contains `C_A <= B < C_F` semantics and the three budget regions.
- [ ] Assert that V3 contains the balanced-query lower bound and explicitly says global/marginal balance does not control adaptive gain.
- [ ] Assert that V3 retains the monotone-Lipschitz no-go and necessary-not-sufficient wording.
- [ ] Assert that V3 distinguishes deterministic finite architecture from Shannon information.
- [ ] Assert that V3 retains recurrence alignment and feedback-magnitude nonidentifiability.

### Task 5: Add V3 readiness ledger and validate

**Files:**
- Create: `manuscript/EVOLUTION_LETTERS_V3_READINESS_V1.json`

**Deliverable:** A machine-readable ledger that records V3 as an expanded candidate, not a replacement for frozen V2, until all tests and word-count checks pass.

- [ ] Run `python -m pytest -q`.
- [ ] Run `python examples/audit_witnesses.py`.
- [ ] Run `python examples/audit_certificate_ladder.py`.
- [ ] Record exact validated commit/workflow once CI is green.
- [ ] Record V2 as fallback and V3 as preferred only if the expansion remains within Letter scope and does not dilute the headline.
