# Submission surface v1

## Purpose

The integrated theory stack (#2 -> #3 -> #5 -> #6) is now merged. This file defines the small set of files that should be treated as canonical for manuscript preparation and records the frozen theory baseline from which submission-only editing should proceed.

## Frozen integrated theory baseline

- main commit: `569abe805cedc3cee9eeebc4a8aa9410efc12c87`;
- tree: `40ce437bac9ba4ae50d04a06b4ed0a7dac0ecc18`;
- post-merge workflow: `34466336113`;
- Python 3.10 / 3.11 / 3.12: full `pytest`, `examples/audit_witnesses.py`, and `examples/audit_certificate_ladder.py` all passed.

Manuscript polishing may move beyond this commit, but changes to theorem statements, model domains, or executable mathematics should be treated as new theory work rather than routine copy-editing.

## Canonical manuscript surface

### 1. Main manuscript

**Canonical:**

- `manuscript/MANUSCRIPT_V1.md`

This is the single main-text source of truth.

### 2. Result hierarchy / theorem spine

**Canonical:**

- `theory/PAPER_THEOREM_SPINE.md`

This controls the hierarchical result spine and the main-text / Supplement boundary. The paper is organized around one principal reachability theorem, one supporting extremal theorem, one diagnostic theorem, and one mechanistic proposition. These are not four equal novelty claims. If prose conflicts with the theorem spine, fix the prose rather than silently changing the theorem.

### 3. Supplement

**Canonical:**

- `manuscript/SUPPLEMENT_V1.md`

This follows the same hierarchical result order and maps every main result to proof notes, executable implementations, tests, and validation receipts. It is an index/proof map rather than a second narrative manuscript.

### 4. Claim / novelty boundary

**Canonical:**

- `manuscript/NOVELTY_PARAGRAPH_V1.md`;
- `manuscript/PRIOR_ART_AUDIT_V2.md`;
- `manuscript/FINAL_PRIORITY_SEARCH_LOG.md`;
- `manuscript/LITERATURE_POSITIONING.md`.

The final targeted search was completed on 2026-09-10 and materially narrowed the novelty language. The canonical boundary now explicitly recognizes:

- fitness-value-of-information theory (Donaldson-Matasci et al. 2010; Rivoire & Leibler 2011);
- **minimum mutual-information requirements for target growth/selection** (Moffett & Eckford 2022);
- evolutionary information-threshold work (de Boer & Hogeweg 2010);
- evolved information-processing and sensing architectures (Trimmer & Houston 2014; Eliassen et al. 2016);
- classical separating-system and binary/multiway decision-tree theory.

Therefore `minimum information` in general is **not** a novelty claim. The principal claim must be stated as a minimum/Pareto-minimal **finite deterministic decision/separation structure**, preferably with explicit `(n,m,E)` language, required through the adaptive/fixed structural gap for a local feedback regime. Failure to locate an exact predecessor for that discrete composition remains a search outcome, not a priority proof; categorical `first` claims are prohibited.

### 5. Bibliography

**Canonical:**

- `manuscript/REFERENCES_CORE_V1.md`.

Core citation metadata and the closest conceptual/mathematical predecessors are synchronized with the current manuscript. Remaining work is target-journal rendering and a final metadata spot-check at submission.

### 6. Figure plan

**Canonical:**

- `manuscript/FIGURE_PLAN_V1.md`.

Four main figures maximum. Their order reflects the result hierarchy: common state space, principal discrete reachability map, supporting extremal envelope, then mechanistic/diagnostic long-time outcomes. Figure 2 must not visually label the principal result as a generic Shannon-information lower bound.

### 7. Editorial QA

**Canonical:**

- `manuscript/MANUSCRIPT_QA_V1.md`;
- `manuscript/SHORTENING_PLAN_V1.md`.

These are editorial controls, not citable manuscript sections.

### 8. Natural-history translation

**Canonical support only:**

- `manuscript/RUNNING_EXAMPLE_V1.md`.

Use at most a short paragraph or box in the final manuscript. This is not an observation-design section.

## Non-canonical manuscript drafts

The following remain useful for provenance and section-level comparison, but should not compete with `MANUSCRIPT_V1.md`:

- `manuscript/THEORETICAL_ECOLOGY_DRAFT.md`;
- `manuscript/ABSTRACT_V1.md`;
- `manuscript/INTRODUCTION_V1.md`;
- `manuscript/MODEL_V1.md`;
- `manuscript/RESULTS_V1.md`;
- `manuscript/DISCUSSION_V1.md`.

New substantive prose changes should normally be made in `MANUSCRIPT_V1.md` unless a section is intentionally being rewritten in isolation.

## Historical / audit material

Validation JSON receipts, proof documents, continuation quotients, solver audits, archived pre-squash branches, and prior branch handoffs remain evidence and Supplement support. They are not separate manuscript surfaces.

## Submission-freeze policy

Before any submission release or journal-formatted export:

1. ensure `MANUSCRIPT_V1.md` matches `PAPER_THEOREM_SPINE.md` mathematically;
2. ensure `SUPPLEMENT_V1.md` maps the full result hierarchy to proof/code/test/receipt sources;
3. ensure every in-text citation has a bibliography entry and every bibliography entry used for the submission is rendered to journal style;
4. explicitly retain Moffett & Eckford (2022) and the information-fitness boundary wherever the principal result is described as a minimum information requirement;
5. prefer `finite decision/separation structure`, `finite sensing architecture`, or explicit `(n,m,E)` wording over unqualified `minimum information` in novelty statements;
6. check the four main figure specifications against the actual result hierarchy and this information-theory distinction;
7. confirm the structural-temporal ceiling is described as extremally sharp rather than as a generic realized-variance predictor;
8. confirm the `alpha=1`, `phi<1` boundary convention remains synchronized between generalized-response theory, code, tests, and prose;
9. confirm the feedback-existence diagnostic checks model compatibility (`0<=T<2`) before treating a complex eigenpair as evidence for nonzero feedback;
10. confirm no observation-design or inverse-diagnostic side program has entered the canonical manuscript;
11. run full CI if any theory/code/test surface changed; documentation-only journal formatting need not be treated as a new theorem validation;
12. preserve the integrated theory baseline and record the exact submission commit/tree used for the submitted manuscript.

## Side branches

Open temporal-routing and inverse-diagnostic work should be treated as separate follow-on/short-report candidates unless deliberately reincorporated after a new claim audit. Their existence must not silently enlarge the canonical manuscript scope.

## Rule going forward

**One manuscript, one result spine, one supplement, one novelty boundary.**

Do not create additional competing full-manuscript drafts unless there is a deliberate journal-specific fork.
