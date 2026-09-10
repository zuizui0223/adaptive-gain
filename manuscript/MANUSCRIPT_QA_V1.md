# Manuscript QA v1

## Status

Baseline manuscript: `manuscript/MANUSCRIPT_V1.md`.

The purpose of this audit is to stop theory growth and identify only changes needed for a submission-ready theoretical ecology paper.

## 1. Core question — PASS

The manuscript no longer asks the already-solved question "why can rapid short-term evolution coexist with long-term stasis?"

Current question:

> When state-dependent selection is generated through finite information use, which evolutionary amplitudes, temporal fluctuations, and local feedback phases are structurally reachable?

This is the correct paper-level question.

## 2. Four-theorem spine — PASS

The main text contains exactly four headline results:

1. structural-temporal joint ceiling;
2. dynamical requirement -> minimum/Pareto-minimal information complexity;
3. two dynamically distinct origins of stasis;
4. complex local modes force feedback existence within the generalized model.

No continuation quotient, certificate ladder, solver enumeration, AR(2) inversion, or critical-slowing theorem is promoted to headline status.

## 3. Static mathematics carries downstream weight — PASS

The finite sensing theory is not merely an appendix because it enters the biological conclusions in two ways:

- `g_max` bounds long-run evolutionary fluctuation through the joint structural-spectral ceiling;
- a required feedback gain gives required integer gap `q`, which gives a minimum/Pareto-minimal information structure.

Productive-frontier edge count appears only where it constrains the fixed burden and reachable gain. This is the right level of exposure for the ecology manuscript.

## 4. Binary versus bounded-arity claims — PASS

The manuscript correctly distinguishes:

- binary: one exact componentwise first corner;
- bounded arity `b>2`: generally a Pareto frontier.

The binary `(6,5,5)` example is presented as a canonical corollary, not a universal minimum.

## 5. Stasis claims — PASS with wording discipline

Current exact distinction:

- cancellation stasis = zero period drift + neutral identity return;
- restoring stasis = zero equilibrium drift + attractive return.

Keep the word `local` on restoring claims because attraction is established from the local Jacobian.

Do not write that these are the only two possible causes of macroevolutionary stasis. Preferred wording: `two dynamically distinct mechanisms represented in the present framework`.

## 6. Feedback-existence claim — PASS with model-class qualifier

The strong result is conditional:

- real nonnegative stable modes can admit `G=0`;
- a non-real local eigenpair forces `G>0` for every compatible decomposition in the generalized model.

Always retain `within the generalized local model` or an equivalent qualifier.

Do not write that oscillation empirically proves eco-evolutionary feedback in arbitrary systems.

## 7. Novelty boundary — PASS

Current manuscript correctly assigns prior art to:

- information use and adaptive decision making;
- cognitive / information-processing constraints;
- sequential sampling and memory;
- minimum test sets / separating systems / test cover;
- binary and multiway decision trees;
- adaptivity gaps;
- bounded-arity rooted-tree combinatorics used internally;
- fluctuating selection and temporal autocorrelation;
- generic eco-evolutionary feedback;
- standard local dynamical-systems mathematics.

Candidate contribution is the exact ecological composition / reachability theory.

Files governing claim discipline:

- `PRIOR_ART_AUDIT_V2.md`
- `FINAL_PRIORITY_SEARCH_LOG.md`
- `NOVELTY_PARAGRAPH_V1.md`
- `LITERATURE_POSITIONING.md`

Do not add a mathematical-priority claim back into the Introduction.

## 8. Observation design — PASS / EXCLUDED

No observation-design program belongs in this paper. Nonidentifiability remains only as a limit on interpreting evolutionary time.

`RUNNING_EXAMPLE_V1.md` is acceptable because it translates notation into natural history and explicitly states that it is not an observation-design proposal.

## 9. Natural-history grounding — GOOD, optional insertion remains

The separate running example maps:

`distant cue -> approach -> near cue -> landing/contact -> handling`

to a finite branching information structure.

For the final manuscript, insert at most one short paragraph or boxed example into the Model. Do not import the whole example file into the main text.

Its purpose is only to explain `world`, `query`, adaptive branching, and irreducible obligations.

## 10. Model assumptions — PASS, but keep visible

The manuscript currently exposes the major assumptions:

- finite state space;
- deterministic cue outcomes;
- guaranteed resolution;
- unit query costs for sharp information-complexity theorems;
- declared linear structural lift;
- finite ergodic reversible community chain for the sharp spectral ceiling;
- local deterministic feedback linearization.

These assumptions must remain in the main manuscript, not only the Supplement.

## 11. Terminology — mostly PASS

Preferred biological translations:

- `world` -> represented ecological alternative;
- `query` -> declared cue / information source;
- `arity` -> number of possible outcomes of one cue;
- `productive-frontier edge` -> irreducible required distinction / information obligation;
- `gap` -> avoidable fixed-information burden under adaptive branching.

Avoid introducing `continuation bisimulation`, `proof DAG`, `residual kernel`, or certificate terminology in the main text.

## 12. Citation work still needed before submission

The conceptual prior-art boundary is sufficiently audited to draft the paper. Remaining citation work is bibliographic rather than theory-blocking:

1. complete volume/page/DOI metadata for every cited paper;
2. add one or two multiway decision-tree / separating-system citations in the Model or Supplement;
3. add the information-processing-constraint references (Dukas 2004; Wright 2022) to the final bibliography;
4. cite a temporal-autocorrelation evolutionary paper near the introduction of `P` / spectral filtering;
5. run one final database search for a direct predecessor to the exact finite-information reachability composition.

Do not delay prose drafting for additional combinatorial priority searches.

## 13. Figures needed

Keep four figures maximum:

1. common state space: finite sensing reward + community recurrence;
2. structural-temporal sharp ceiling and reward-mode alignment;
3. required gain -> required gap -> binary corner / bounded-arity Pareto frontier;
4. directional change, neutral cancellation stasis, monotone restoring stasis, oscillatory restoring stasis, marking only the latter as forcing feedback existence inside the model.

Do not add a separate observation-design figure.

## 14. Supplement boundary — PASS

Move or retain outside the main text:

- continuation equivalences;
- fixed-side kernels;
- proof DAGs;
- LP / integer certificates;
- enumeration receipts;
- bounded-arity recurrence proof details;
- private-pair forest construction details;
- critical-slowing derivations;
- exact transient ceilings;
- inverse algebra;
- solver-cap implementation details.

## 15. Immediate next manuscript tasks

No new theorem is needed before these tasks:

1. reconcile `MANUSCRIPT_V1.md` with one short running-example paragraph;
2. complete bibliography metadata;
3. prepare four figure specifications;
4. tighten Results proof sketches to the minimum needed for a theoretical-ecology reader;
5. perform a line edit for repeated phrases such as `within the declared model class`, retaining the qualifier where mathematically necessary;
6. decide whether to merge/squash PR #6 only after the manuscript surface stabilizes.

## Overall assessment

The theory is now manuscript-limited rather than theorem-limited. Further value is more likely to come from ecological exposition, citation completeness, figure design, and shortening than from additional extremal cases or local dynamical extensions.
