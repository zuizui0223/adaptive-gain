# Manuscript QA v1

## Status

Baseline manuscript: `manuscript/MANUSCRIPT_V1.md`.

The purpose of this audit is to stop theory growth and identify only changes needed for a submission-ready theoretical ecology paper. The integrated theory baseline is main commit `569abe805cedc3cee9eeebc4a8aa9410efc12c87`; its post-merge workflow (`34466336113`) passed Python 3.10, 3.11, and 3.12 with full `pytest`, `examples/audit_witnesses.py`, and `examples/audit_certificate_ladder.py`.

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

Do not describe it as a generic prediction of realized long-run variance. The main text exposes the two multiplicative sources of slack:

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

Keep the word `local` on restoring claims because attraction is established from the local Jacobian. Do not write that these are the only two possible causes of macroevolutionary stasis. Preferred wording: `two dynamically distinct mechanisms represented in the present framework`.

The distinction belongs in the main text for biological interpretation, but the identity-map versus contraction algebra is standard and remains a proposition rather than a headline theorem novelty claim.

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

If a complex pair has `T<0` or `T>=2`, report that the observed transient lies outside the declared persistence domain rather than reporting feedback existence. `alpha=1` is a permitted neutral boundary; a double unit root is infeasible because it would require `phi=1`.

Always retain `within the generalized local model` or an equivalent qualifier. Do not write that oscillation empirically proves eco-evolutionary feedback in arbitrary systems.

## 8. Gain-infimum helper — PASS after boundary repair

For `R=1-T+D`, the public helper for

`inf_{0<=phi<1} G(phi)`

preserves the exact four cases:

- `R<0 -> -infinity`;
- `R=0 -> T-2` at the excluded boundary limit;
- `0<R<=1 -> T-2+2*sqrt(R)`;
- `R>1 -> D` at `phi=0`.

This helper optimizes over the unit community-memory interval itself; model compatibility is checked separately before the feedback-existence inference. Regression tests include `R<0`, `R=0`, `alpha=1`, the half-open trace domain `0<=T<2`, and a complex eigenpair outside that domain.

## 9. Novelty boundary — PASS

Current manuscript correctly assigns prior art to information use, cognitive and information-processing constraints, proximate sensing architectures, sequential sampling and memory, minimum test sets/separating systems/test cover, binary and multiway decision trees, adaptivity gaps, bounded-arity rooted-tree combinatorics used internally, fluctuating selection and temporal autocorrelation, generic eco-evolutionary feedback, standard local dynamical-systems mathematics, and identity maps versus contractions.

Candidate contribution is the exact ecological composition/reachability theory, with the reverse dynamics-to-information map as its strongest form.

Files governing claim discipline:

- `PRIOR_ART_AUDIT_V2.md`;
- `FINAL_PRIORITY_SEARCH_LOG.md`;
- `NOVELTY_PARAGRAPH_V1.md`;
- `LITERATURE_POSITIONING.md`.

Do not add a categorical mathematical-priority claim back into the Introduction.

## 10. Observation design — PASS / EXCLUDED

No observation-design program belongs in this paper. Nonidentifiability remains only as a limit on interpreting evolutionary time.

`RUNNING_EXAMPLE_V1.md` is acceptable because it translates notation into natural history and explicitly states that it is not an observation-design proposal.

## 11. Natural-history grounding — GOOD, optional insertion remains

The separate running example maps

`distant cue -> approach -> near cue -> landing/contact -> handling`

to a finite branching information structure.

For the final manuscript, insert at most one short paragraph or boxed example into the Model. Do not import the whole example file into the main text. Its purpose is only to explain `world`, `query`, adaptive branching, and irreducible obligations.

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

## 14. Citation and priority audit — PASS; journal-style rendering remains

The previously open bibliography tasks are now closed at manuscript level:

1. core cited ecology/evolution references have volume/page/DOI metadata where applicable;
2. binary/multiway decision-tree and separating-system anchors are cited in the Introduction/Model;
3. Dukas, Wright et al., Trimmer & Houston, and Eliassen et al. are present in the manuscript bibliography;
4. Cotto & Chevin is cited near the temporal-recurrence construction;
5. Post & Palkovacs and Schoener anchor generic eco-evolutionary feedback;
6. the final targeted direct-predecessor search was completed on 2026-09-10.

The closest additional conceptual precursors found in the final search were Trimmer & Houston (2014) and Eliassen et al. (2016), which strengthen the prior-art boundary around evolved information-processing and sensing architecture. The search did not locate the exact reverse lower-bound map from a required dynamical regime to a required finite decision/separation structure. This is a search outcome, not proof of priority, so `first`/`no previous theory` language remains prohibited.

Remaining bibliography work is journal-specific rendering: capitalization, punctuation, conference-proceedings format, and a final metadata spot-check at submission.

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
- LP/integer certificates;
- enumeration receipts;
- bounded-arity recurrence proof details;
- private-pair forest construction details;
- critical-slowing derivations;
- exact transient ceilings;
- inverse algebra;
- solver-cap implementation details.

## 17. Submission-surface hierarchy audit — PASS after one editorial repair

The original hierarchy audit correctly synchronized the theorem spine, canonical manuscript, Supplement, figure plan, shortening plan, submission surface, and novelty paragraph, but it missed one stale line in `LITERATURE_POSITIONING.md` that still said `keep four headline theorems only`. The submission-polish pass detected and corrected that inconsistency.

The audited claim/control surface now explicitly includes:

- `theory/PAPER_THEOREM_SPINE.md`;
- `manuscript/MANUSCRIPT_V1.md`;
- `manuscript/SUPPLEMENT_V1.md`;
- `manuscript/FIGURE_PLAN_V1.md`;
- `manuscript/SHORTENING_PLAN_V1.md`;
- `manuscript/SUBMISSION_SURFACE_V1.md`;
- `manuscript/NOVELTY_PARAGRAPH_V1.md`;
- `manuscript/LITERATURE_POSITIONING.md`;
- `manuscript/FINAL_PRIORITY_SEARCH_LOG.md`;
- `manuscript/REFERENCES_CORE_V1.md`.

They consistently treat the reverse dynamics-to-information map as principal, the structural-temporal bound as an extremal envelope rather than a point predictor, oscillation as a model-gated diagnostic, and the stasis comparison as a mechanistic proposition. No observation-design program has entered the canonical manuscript surface.

The integrated main commit `569abe805cedc3cee9eeebc4a8aa9410efc12c87` has tree `40ce437bac9ba4ae50d04a06b4ed0a7dac0ecc18` and passed post-merge workflow `34466336113` on Python 3.10/3.11/3.12, including full `pytest` and both repository audit scripts.

## 18. Immediate next manuscript tasks

No new theorem is needed. Remaining work is manuscript-facing:

1. line-edit repeated qualifiers and explanatory duplication without weakening theorem conditions;
2. tighten Results proof sketches to the minimum needed for a theoretical-ecology reader;
3. decide whether one short natural-history paragraph/box materially improves comprehension;
4. turn the four figure specifications into submission-ready figures;
5. render references and manuscript formatting to the target journal style.

## Overall assessment

The theory is manuscript-limited rather than theorem-limited. Further value is more likely to come from ecological exposition, figure design, shortening, and journal-specific presentation than from additional extremal cases or local dynamical extensions.
