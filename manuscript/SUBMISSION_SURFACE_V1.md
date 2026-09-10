# Submission surface v1

## Purpose

PR #6 contains a large theory and validation history. This file defines the small set of files that should be treated as canonical for manuscript preparation. Everything else can support or document the work without competing as a second manuscript source of truth.

## Canonical manuscript surface

### 1. Main manuscript

**Canonical:**

- `manuscript/MANUSCRIPT_V1.md`

This is the single main-text source of truth.

### 2. Theorem spine

**Canonical:**

- `theory/PAPER_THEOREM_SPINE.md`

This controls the four headline theorems and the main-text / Supplement boundary. If prose conflicts with the theorem spine, fix the prose rather than silently changing the theorem.

### 3. Supplement

**Canonical:**

- `manuscript/SUPPLEMENT_V1.md`

This follows the same four-theorem order and maps every main result to proof notes, executable implementations, tests, and validation receipts. It is an index/proof map rather than a second narrative manuscript.

### 4. Claim / novelty boundary

**Canonical:**

- `manuscript/NOVELTY_PARAGRAPH_V1.md`;
- `manuscript/PRIOR_ART_AUDIT_V2.md`;
- `manuscript/FINAL_PRIORITY_SEARCH_LOG.md`;
- `manuscript/LITERATURE_POSITIONING.md`.

These files govern what may and may not be claimed as new.

### 5. Bibliography

**Canonical:**

- `manuscript/REFERENCES_CORE_V1.md`.

This is the seed for the final journal-formatted bibliography.

### 6. Figure plan

**Canonical:**

- `manuscript/FIGURE_PLAN_V1.md`.

Four main figures maximum.

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
2. ensure `SUPPLEMENT_V1.md` maps every headline result to proof/code/test/receipt sources;
3. ensure the final bibliography includes every manuscript citation;
4. check the four main figure specifications against the actual theorem statements;
5. confirm no observation-design material entered the canonical manuscript;
6. run full CI;
7. prefer a squash merge or otherwise preserve a clear release/tag for the submission theory state.

## Rule going forward

**One manuscript, one theorem spine, one supplement, one novelty boundary.**

Do not create additional competing full-manuscript drafts unless there is a deliberate journal-specific fork.
