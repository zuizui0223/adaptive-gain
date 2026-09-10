# Manuscript QA v1

## Status

Baseline manuscript: `manuscript/MANUSCRIPT_V1.md`.

The purpose of this audit is to stop theory growth and identify only changes needed for a submission-ready theoretical ecology paper. The frozen submission candidate before the current readability pass is main commit `fa87a79d6f3d99048f357ad9253d53706cf227ff`; its post-merge workflow (`34473656265`) passed Python 3.10, 3.11, and 3.12 with full `pytest`, `examples/audit_witnesses.py`, and `examples/audit_certificate_ladder.py`.

## 1. Core question — PASS

The manuscript no longer asks the already-solved question "why can rapid short-term evolution coexist with long-term stasis?"

Current question:

> When state-dependent selection is generated through a declared finite decision/separation architecture, which evolutionary amplitudes, temporal fluctuations, and local feedback phases are structurally reachable?

This is the correct paper-level question.

## 2. Result hierarchy — PASS

The main text no longer presents four equal headline theorems. The canonical hierarchy is:

1. **principal reachability theorem** — dynamical requirement -> required structural gap -> minimum/Pareto-minimal finite decision/separation structure;
2. **supporting extremal theorem** — structural-temporal envelope on long-run fluctuation;
3. **diagnostic theorem** — a model-compatible complex local mode forces feedback existence within the generalized model;
4. **mechanistic proposition** — neutral cancellation and attractive restoring stasis are dynamically distinct.

No continuation quotient, certificate ladder, solver enumeration, AR(2) inversion, critical-slowing result, or stasis identity/contraction algebra is promoted into an independent novelty headline.

## 3. Principal theorem carries the main biological conclusion — PASS with terminology constraint

The reverse map

`required local dynamical regime -> required structural gap q -> minimum/Pareto-minimal finite decision/separation structure`

is the manuscript's strongest claim. The finite sensing theory therefore carries a biological conclusion rather than serving only as a structural encoding.

The `q=3,b=4` Pareto example is especially useful because `(8,5,5)` and `(7,6,6)` show that reducing query/frontier burden and reducing represented-world count are not the same objective.

**Terminology constraint:** do not shorten this novelty claim to unqualified `minimum information`. Moffett & Eckford (2022) already derive minimum mutual-information requirements for target growth and average selection coefficients. The present theorem concerns a different discrete object: represented alternatives, declared cues, irreducible fixed-side obligations, adaptive depth, and outcome arity.

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

## 9. Novelty boundary — PASS after material narrowing

Current manuscript assigns prior art to:

- evolutionary information use, cognitive/information-processing constraints, and evolved sensing architectures;
- the fitness value of information and information-fitness relations;
- **minimum mutual-information requirements for target fitness/selection** (Moffett & Eckford 2022);
- evolutionary information thresholds (de Boer & Hogeweg 2010);
- minimum test sets / separating systems / test cover;
- binary and multiway decision trees and generic adaptivity gaps;
- bounded-arity rooted-tree combinatorics used internally;
- fluctuating selection, temporal autocorrelation, and generic eco-evolutionary feedback;
- standard local dynamical-systems mathematics and identity maps versus contractions.

Candidate contribution is narrower: an exact discrete ecological composition in which a required local dynamical regime implies a required adaptive/fixed structural gap and therefore a minimum/Pareto-minimal finite decision/separation architecture over `(n,m,E)` under a declared outcome-arity cap.

The supporting structural-temporal theorem composes the finite structural reward range with recurrence of the same state-indexed rewards; it is not a new information-fitness-value theorem.

Files governing claim discipline:

- `PRIOR_ART_AUDIT_V2.md`;
- `FINAL_PRIORITY_SEARCH_LOG.md`;
- `NOVELTY_PARAGRAPH_V1.md`;
- `LITERATURE_POSITIONING.md`.

Do not add a categorical mathematical-priority claim back into the Introduction.

## 10. Observation design — PASS / EXCLUDED

No observation-design program belongs in this paper. Nonidentifiability remains only as a limit on interpreting evolutionary time.

`RUNNING_EXAMPLE_V1.md` remains support material and is not an observation-design proposal.

## 11. Natural-history grounding — PASS after minimal insertion

The line-edit pass inserted one short generic example of sequential habitat/resource assessment into Model 2.1:

`coarse cue -> branch choice -> fine-scale cue -> action`.

Its only job is to explain why contingent sensing can require fewer cues than a fixed strategy. The paragraph explicitly avoids prescribing an empirical measurement protocol and does not import the full running example into the main text.

## 12. Model assumptions — PASS, but keep visible

The manuscript currently exposes the major assumptions:

- finite state space;
- deterministic cue outcomes;
- guaranteed resolution;
- unit query costs for sharp decision/separation-structure theorems;
- declared linear structural lift;
- finite ergodic reversible community chain for the structural-temporal envelope;
- local deterministic feedback linearization;
- `0<=alpha<=1` and `0<=phi<1` for the generalized response model;
- model-compatibility gate `0<=T<2` before feedback-existence inference.

These assumptions must remain in the main manuscript, not only the Supplement.

## 13. Terminology — PASS with information-theory distinction

Preferred biological translations:

- `world` -> represented ecological alternative;
- `query` -> declared cue / information source;
- `arity` -> number of possible outcomes of one cue;
- `productive-frontier edge` -> irreducible required distinction / information obligation;
- `gap` -> avoidable fixed-information burden under adaptive branching.

For the principal novelty claim prefer `finite sensing architecture`, `finite decision/separation structure`, or explicit `(n,m,E)` language. Do not use `minimum information` by itself because it is ambiguous with Shannon/mutual-information theory.

Avoid introducing `continuation bisimulation`, `proof DAG`, `residual kernel`, or certificate terminology in the main text.

## 14. Citation and priority audit — PASS after final close-precursor correction

The final targeted search on 2026-09-10 recovered a more important mathematical precursor than the initial submission-polish pass had recorded:

- Donaldson-Matasci et al. (2010): fitness value of information;
- Rivoire & Leibler (2011): information-fitness relations in varying environments;
- **Moffett & Eckford (2022): minimal mutual-information requirements for target growth and average selection coefficient**;
- de Boer & Hogeweg (2010): evolutionary information threshold;
- Trimmer & Houston (2014) and Eliassen et al. (2016): evolved information-processing/sensing architecture.

Moffett & Eckford materially narrows the novelty wording. It does not invalidate the principal theorem because the minimized object is different, but it means the manuscript cannot claim that reverse `required evolutionary performance -> required information` reasoning is new.

The exact distinction retained is:

- prior art: scalar Shannon/mutual-information or coding-information requirements for fitness/selection;
- present manuscript: finite deterministic decision/separation structure, with exact componentwise minima or a Pareto frontier over represented alternatives, declared cues, and irreducible obligations, composed with a local feedback phase.

Remaining bibliography work is journal-specific rendering and a final metadata spot-check, not a conceptual priority search.

## 15. Figures needed

Keep four figures maximum in this order:

1. common state space: finite sensing reward + community recurrence;
2. **principal reachability map**: required gain -> required gap -> binary corner / bounded-arity Pareto frontier, labelled explicitly as finite decision/separation structure rather than Shannon information;
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

## 17. Submission-surface hierarchy and claim audit — PASS

The prior submission-polish pass repaired the stale four-theorem wording and narrowed the information-theory novelty boundary after recovering Moffett & Eckford (2022). The current readability pass changes ecological exposition, not theorem content.

The canonical/control surface remains:

- `theory/PAPER_THEOREM_SPINE.md`;
- `manuscript/MANUSCRIPT_V1.md`;
- `manuscript/SUPPLEMENT_V1.md`;
- `manuscript/FIGURE_PLAN_V1.md`;
- `manuscript/SHORTENING_PLAN_V1.md`;
- `manuscript/SUBMISSION_SURFACE_V1.md`;
- `manuscript/NOVELTY_PARAGRAPH_V1.md`;
- `manuscript/PRIOR_ART_AUDIT_V2.md`;
- `manuscript/LITERATURE_POSITIONING.md`;
- `manuscript/FINAL_PRIORITY_SEARCH_LOG.md`;
- `manuscript/REFERENCES_CORE_V1.md`.

The theorem hierarchy and novelty boundary are unchanged by the line edit.

## 18. Theoretical Ecology readability pass — PASS pending branch CI

Current proposed title:

> Finite sensing structure constrains eco-evolutionary feedback regimes

The title is seven words and avoids using broad `information structure` language as the paper's primary branding. The abstract is approximately 190 words, contains no citations, and introduces contingent versus fixed cue use before formal decision-tree terminology. Five keywords are included.

The Introduction now proceeds in the order:

`ecological question -> information/sensing prior art -> finite decision architecture -> structural gap -> reverse reachability theorem`.

This matches the journal-level goal that theoretical work answer a question of ecological interest and remain readable by a broad ecological audience.

## 19. Immediate next manuscript tasks

No new theorem is needed. Remaining work is submission-facing:

1. complete Figure 1-4 as publication-ready conceptual/theoretical figures;
2. add final title-page author and affiliation metadata;
3. add required declarations (funding, competing interests, authorship/contributions, and code/data availability as applicable);
4. render references and manuscript formatting to the target journal's current submission style;
5. record the exact submitted manuscript commit/tree.

## Overall assessment

The theory remains manuscript-limited rather than theorem-limited. The final prior-art pass did not remove the principal discrete reachability result, but it made its proper novelty boundary substantially narrower: **finite decision/separation architecture and its exact local-phase/Pareto mapping**, not minimum information for evolutionary performance in general. The current line edit makes that narrower claim more legible to an ecological reader without adding mathematics.
