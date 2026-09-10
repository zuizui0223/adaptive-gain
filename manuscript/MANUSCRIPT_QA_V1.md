# Manuscript QA v1

## Status

Baseline manuscript: `manuscript/MANUSCRIPT_V1.md`.

The purpose of this audit is to stop theory growth and identify only changes needed for a submission-ready theoretical ecology paper.

## 1. Core question — PASS

The manuscript no longer asks the already-solved question "why can rapid short-term evolution coexist with long-term stasis?"

Current question:

> When state-dependent selection is generated through finite information use, which evolutionary amplitudes, temporal fluctuations, and local feedback phases are structurally reachable?

This is the correct paper-level question.

## 2. Result hierarchy — PASS

The main text no longer presents four equal headline theorems. The canonical hierarchy is:

1. **principal reachability theorem** — dynamical requirement -> minimum/Pareto-minimal information complexity;
2. **supporting extremal theorem** — structural-temporal envelope on long-run fluctuation;
3. **diagnostic theorem** — a model-compatible complex local mode forces feedback existence within the generalized model;
4. **mechanistic proposition** — neutral cancellation and attractive restoring stasis are dynamically distinct.

No continuation quotient, certificate ladder, solver enumeration, AR(2) inversion, critical-slowing result, or stasis identity/contraction algebra is promoted into an independent novelty headline.

## 3. Principal theorem carries the main biological conclusion — PASS

The reverse map

`required dynamical regime -> required structural gap q -> minimum/Pareto-minimal finite information structure`

is the manuscript's strongest claim. The finite sensing theory therefore carries a biological conclusion rather than serving only as a structural encoding.

The `q=3,b=4` Pareto example is especially useful because `(8,5,5)` and `(7,6,6)` show that reducing query/frontier burden and reducing represented-world count are not the same objective.

## 4. Structural-temporal theorem: sharpness versus tightness — PASS with wording discipline

The ceiling

\[
\sigma_{\rm eff}^2\le\frac{(\lambda g_{\max})^2}{4}\frac{1+r_{\max}}{1-r_{\max}}
\]

is **sharp in the extremal sense** because a symmetric two-state endpoint-reward construction attains equality.

Do not describe it as a generic prediction of realized long-run variance. The main text now exposes the two multiplicative sources of slack:

- range/variance saturation;
- reward alignment with the slowest algebraic mode.

This distinction must remain visible in Results, Discussion, Figure 3, and Scope.

## 5. Binary versus bounded-arity claims — PASS

The manuscript correctly distinguishes:

- binary: one exact componentwise first corner;
- bounded arity `b>2`: generally a Pareto frontier.

The binary `(6,5,5)` example is presented as a canonical corollary, not a universal minimum.

## 6. Stasis proposition — PASS with downgraded novelty status

Current exact distinction:

- cancellation stasis = zero period drift + neutral identity return;
- restoring stasis = zero equilibrium drift + attractive return.

Keep the word `local` on restoring claims because attraction is established from the local Jacobian.

Do not write that these are the only two possible causes of macroevolutionary stasis. Preferred wording: `two dynamically distinct mechanisms represented in the present framework`.

The distinction belongs in the main text for biological interpretation, but the identity-map versus contraction algebra is standard and should remain a proposition rather than a headline theorem novelty claim.

## 7. Feedback-existence claim, alpha boundary, and model compatibility — PASS

The strong result is conditional:

- stable real nonnegative modes can admit `G=0`;
- a non-real local eigenpair forces `G>0` for every compatible decomposition **only when the observed trace admits at least one persistence split in the generalized model**.

The generalized response domain is

\[
0\le\alpha\le1,
\qquad
0\le\phi<1.
\]

Since `T=alpha+phi`, model compatibility requires exactly

\[
0\le T<2.
\]

If a complex pair has `T<0` or `T>=2`, do not report feedback existence. Report that the observed transient lies outside the declared persistence domain. This avoids a vacuous universal statement over an empty feasible-decomposition set.

`alpha=1` is a permitted neutral boundary. A zero-feedback decomposition with one eigenvalue exactly one can be model-feasible if the other eigenvalue serves as `phi`, but it is outside the asymptotically stable monotone-return corollary. A double unit root is infeasible because it would require `phi=1`.

Always retain `within the generalized local model` or an equivalent qualifier. Do not write that oscillation empirically proves eco-evolutionary feedback in arbitrary systems.

## 8. Gain-infimum helper — PASS after boundary repair

For `R=1-T+D`, the public helper for

`inf_{0<=phi<1} G(phi)`

must preserve the exact four cases:

- `R<0 -> -infinity`;
- `R=0 -> T-2` at the excluded boundary limit;
- `0<R<=1 -> T-2+2*sqrt(R)`;
- `R>1 -> D` at `phi=0`.

This helper optimizes over the unit community-memory interval itself; it does not additionally require the implied `alpha=T-phi` to lie in `[0,1]`. Model compatibility is checked separately before the feedback-existence inference.

Regression tests must include `R<0`, `R=0`, `alpha=1`, the half-open trace domain `0<=T<2`, and a complex eigenpair outside that domain.

## 9. Novelty boundary — PASS

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
- standard local dynamical-systems mathematics;
- identity maps versus contractions.

Candidate contribution is the exact ecological composition / reachability theory, with the reverse dynamics-to-information map as its strongest form.

Files governing claim discipline:

- `PRIOR_ART_AUDIT_V2.md`
- `FINAL_PRIORITY_SEARCH_LOG.md`
- `NOVELTY_PARAGRAPH_V1.md`
- `LITERATURE_POSITIONING.md`

Do not add a mathematical-priority claim back into the Introduction.

## 10. Observation design — PASS / EXCLUDED

No observation-design program belongs in this paper. Nonidentifiability remains only as a limit on interpreting evolutionary time.

`RUNNING_EXAMPLE_V1.md` is acceptable because it translates notation into natural history and explicitly states that it is not an observation-design proposal.

## 11. Natural-history grounding — GOOD, optional insertion remains

The separate running example maps:

`distant cue -> approach -> near cue -> landing/contact -> handling`

to a finite branching information structure.

For the final manuscript, insert at most one short paragraph or boxed example into the Model. Do not import the whole example file into the main text.

Its purpose is only to explain `world`, `query`, adaptive branching, and irreducible obligations.

## 12. Model assumptions — PASS, but keep visible

The manuscript currently exposes the major assumptions:

- finite state space;
- deterministic cue outcomes;
- guaranteed resolution;
- unit query costs for sharp information-complexity theorems;
- declared linear structural lift;
- finite ergodic reversible community chain for the structural-temporal envelope;
- local deterministic feedback linearization;
- `0<=alpha<=1` and `0<=phi<1` for the generalized response model;
- model-compatibility gate `0<=T<2` before feedback-existence inference.

These assumptions must remain in the main manuscript, not only the Supplement.

## 13. Terminology — mostly PASS

Preferred biological translations:

- `world` -> represented ecological alternative;
- `query` -> declared cue / information source;
- `arity` -> number of possible outcomes of one cue;
- `productive-frontier edge` -> irreducible required distinction / information obligation;
- `gap` -> avoidable fixed-information burden under adaptive branching.

Avoid introducing `continuation bisimulation`, `proof DAG`, `residual kernel`, or certificate terminology in the main text.

## 14. Citation work still needed before submission

The conceptual prior-art boundary is sufficiently audited to draft the paper. Remaining citation work is bibliographic rather than theory-blocking:

1. complete volume/page/DOI metadata for every cited paper;
2. add one or two multiway decision-tree / separating-system citations in the Model or Supplement;
3. add the information-processing-constraint references (Dukas 2004; Wright 2022) to the final bibliography;
4. cite a temporal-autocorrelation evolutionary paper near the introduction of `P` / spectral filtering;
5. run one final database search for a direct predecessor to the exact finite-information reachability composition.

Do not delay prose drafting for additional combinatorial priority searches.

## 15. Figures needed

Keep four figures maximum in this order:

1. common state space: finite sensing reward + community recurrence;
2. **principal reachability map**: required gain -> required gap -> binary corner / bounded-arity Pareto frontier;
3. **supporting structural-temporal envelope** with explicit slack factors and equality witness;
4. directional change, neutral cancellation stasis, monotone restoring stasis, oscillatory restoring stasis, marking the stasis comparison as a mechanistic proposition and only a **model-compatible** complex local regime as forcing feedback existence inside the model.

Do not add a separate observation-design figure.

## 16. Supplement boundary — PASS

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

## 17. Immediate next manuscript tasks

No new theorem is needed before these tasks:

1. complete the full CI check for the gain-infimum, `alpha=1`, and model-compatibility repairs;
2. complete bibliography metadata;
3. tighten Results proof sketches to the minimum needed for a theoretical-ecology reader;
4. perform a line edit for repeated phrases such as `within the declared model class`, retaining the qualifier where mathematically necessary;
5. decide whether to merge/squash PR #6 only after the manuscript surface stabilizes.

## Overall assessment

The theory is manuscript-limited rather than theorem-limited. Further value is more likely to come from protecting the principal reachability claim, ecological exposition, citation completeness, figure design, and shortening than from additional extremal cases or local dynamical extensions.
