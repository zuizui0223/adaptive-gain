# Submission surface v1

## Purpose

PR #6 contains a large theory and validation history. This file defines the small set of files that should be treated as canonical for manuscript preparation. Everything else can support or document the work without competing as a second manuscript source of truth.

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

These files govern what may and may not be claimed as new. In particular, do not promote the standard dynamical-systems ingredients or the stasis identity/contraction distinction into independent novelty claims.

### 5. Bibliography

**Canonical:**

- `manuscript/REFERENCES_CORE_V1.md`.

This is the seed for the final journal-formatted bibliography.

### 6. Figure plan

**Canonical:**

- `manuscript/FIGURE_PLAN_V1.md`.

Four main figures maximum. Their order should reflect the result hierarchy: common state space, principal reachability map, supporting extremal envelope, then mechanistic/diagnostic long-time outcomes.

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

Validation JSON receipts, proof documents, continuation quotients, solver audits, and prior branch handoffs remain evidence and Supplement support. They are not separate manuscript surfaces.

## Merge policy for PR #6

Before merging or squashing:

1. ensure `MANUSCRIPT_V1.md` matches `PAPER_THEOREM_SPINE.md`;
2. ensure `SUPPLEMENT_V1.md` maps the full result hierarchy to proof/code/test/receipt sources;
3. ensure the final bibliography includes every manuscript citation;
4. check the four main figure specifications against the actual result hierarchy;
5. confirm the structural-temporal ceiling is described as extremally sharp rather than as a generic realized-variance predictor;
6. confirm the `alpha=1`, `phi<1` boundary convention is synchronized between generalized-response theory, code, tests, and prose;
7. confirm no observation-design material entered the canonical manuscript;
8. run full CI;
9. prefer a squash merge or otherwise preserve a clear release/tag for the submission theory state.

## Rule going forward

**One manuscript, one result spine, one supplement, one novelty boundary.**

Do not create additional competing full-manuscript drafts unless there is a deliberate journal-specific fork.
