
# Mathematical recovery audit v1 — adaptive-gain from initial commit to the decision-ecology synthesis

Date: 2026-10-03

## Executive conclusion

The repository's mathematical output has not all been absorbed into the current
Ecology Letters manuscript, and it should not be. The project now contains
several distinct mathematical programs.

Disposition codes used here:

- MAIN — needed for the current decision-ecology manuscript.
- SUPPLEMENT — directly supports the current manuscript but should not compete
  with its biological headline.
- COMPANION — strong reusable finite-combinatorial mathematics deserving a
  separate mathematical paper.
- SEPARATE — exact side theory requiring additional biological assumptions or
  belonging to a different inferential paper.
- ARCHIVE — proof, compression, certification, or finite-classification
  machinery.

Two theorem groups deserve renewed attention under the current behavioural-
ecology framing:

1. the two-sided structural factorization
   g = C_F - C_A = tau_c(H_min) - V_A(K_A), with exact counterexamples showing
   that neither side alone determines the gap; and
2. the temporal/noisy routing theorems, where a cue with zero direct target
   information can have value because it predicts which later cue will be useful.

Everything else is either already represented in the manuscript/supplement or
belongs more cleanly to a companion/separate paper.

## 1. Initial finite-resolution foundation — 2026-09-07

The repository began with finite deterministic target-resolution tasks and

C_A = minimum worst-path adaptive cost,
C_F = minimum fixed resolving-set cost.

Closed results include:

- C_A <= C_F;
- exact adaptive-only budget interval C_A <= B < C_F;
- policy-union and bypass decompositions;
- target-pair cover formulations of the fixed comparator;
- private-pair, pair-packing, fractional, and exact integer certificates.

Canonical sources:
theory/ADAPTIVE_GAIN_THEOREM.md
theory/STRUCTURAL_DECOMPOSITION_AND_MINIMALITY.md
theory/FIXED_BYPASS_PAIR_COVER.md
theory/PAIR_PACKING_LOWER_BOUND.md
theory/FRACTIONAL_PAIR_COVER_BOUND.md
theory/INTEGER_FIXED_COVER_PROOF.md

Disposition: foundation + COMPANION/ARCHIVE.

## 2. Exact structural representations and kernels

Adaptive-side exact reductions:

- full target-pair incidence suffices for deterministic adaptive cost;
- target-relevant query refinement dominance;
- same-target world-twin quotient;
- exact two-sided Bellman kernel;
- recursive continuation equivalence preserving C_A.

Canonical sources:
theory/FULL_PAIR_INCIDENCE_SUFFICIENCY.md
theory/ADAPTIVE_SAFE_QUERY_COMPRESSION.md
theory/ADAPTIVE_WORLD_TWIN_QUOTIENT.md
theory/ADAPTIVE_TWO_SIDED_KERNEL.md
theory/CONTINUATION_BISIMULATION.md

A sharp boundary is already proved: two tasks can have the same recursive
continuation root type and the same C_A=2, yet C_F=3 and 2. Thus an adaptive-safe
quotient does not determine the fixed comparator.

Fixed-side exact reduction:

A fixed bundle B resolves the target iff it hits every reachable productive set.
Therefore C_F is exactly a weighted hitting-set optimum over the minimal
productive frontier.

Canonical sources:
theory/PRODUCTIVE_FRONTIER_SUFFICIENCY.md
theory/STATIC_MINIMAL_PRODUCTIVE_FRONTIER.md
theory/STATE_RESOURCE_INCIDENCE_SUFFICIENCY.md
theory/RESOURCE_OVERLAP_HIERARCHY.md

### Two-sided factorization — currently branch-only

On branch theory/reachability-admissibility-synthesis:

C_A = V_A(K_A)
C_F = tau_c(H_min)

and therefore

g = C_F - C_A = tau_c(H_min) - V_A(K_A).

Exact collisions prove:

K_A alone does not determine g;
H_min alone does not determine g;
the pair (K_A,H_min) does determine g.

Sources:
theory/TWO_SIDED_GAP_FACTORIZATION.md
theory/TOPOLOGY_SENSING_SUFFICIENT_KERNEL.md

Disposition: SUPPLEMENT candidate for the current paper.

Under the current framing this has a direct biological meaning:
effective decision burden has two sides — outcome-contingent continuation
structure and globally unavoidable simultaneous cue obligations.

## 3. Proof compression, certificates and symmetry

Closed infrastructure includes:

- residual fixed-cover kernelization;
- pair-obligation dominance;
- exact proof trees;
- shared-state proof-DAG compression;
- residual isomorphism quotients;
- bipartite color refinement;
- individualization-refinement;
- automorphism groups and orbit pruning;
- symmetry-pruned proof DAGs and branch-orbit size bounds.

Canonical sources include:
theory/FIXED_COVER_KERNELIZATION.md
theory/PROOF_DAG_COMPRESSION.md
theory/RESIDUAL_ISOMORPHISM_QUOTIENT.md
theory/BIPARTITE_COLOR_REFINEMENT.md
theory/SYMMETRY_REFINEMENT_AND_AUTOMORPHISMS.md
theory/SYMMETRY_PRUNED_PROOF_DAG.md

Disposition: ARCHIVE/COMPANION.

## 4. Minimal normal forms and finite classifications

Closed results include:

- unique minimal four-world strict-gain normal form;
- complete four-query extension classification;
- unique deletion-minimal five-world strict-gain normal form;
- exact resource co-location repair in the first ambiguous scope;
- sharp minimum query counts for internal and external bypass channels.

Sources:
theory/MINIMAL_STRICT_GAIN_NORMAL_FORM.md
theory/FOUR_QUERY_EXTENSION_CLASSIFICATION.md
theory/FIVE_WORLD_IRREDUCIBLE_NORMAL_FORM.md
theory/RESOURCE_COLOCATION_REPAIR_CLASSIFICATION.md
theory/BYPASS_CHANNEL_QUERY_MINIMALITY.md

Disposition: COMPANION/ARCHIVE.
The four-world core remains useful as the minimal experimental design.

## 5. Generic extremal adaptive advantage

The repository proves:

- unbounded unit-cost adaptive advantage;
- unbounded advantage using only binary observations;
- sharp fixed-(n,m) unit-cost ratios;
- sharp binary ratios;
- sharp bounded-arity ratios;
- sharp ratio with a productive-frontier edge cap;
- any positive upper cap on frontier rank is extremally vacuous;
- exact bounded-arity inverse/Pareto results for a required gap.

Sources include:
theory/UNBOUNDED_UNIT_COST_ADAPTIVE_GAIN.md
theory/EXTREMAL_DEPTH_TWO_ROUTING.md
theory/SHARP_UNIT_COST_WORLD_QUERY_RATIO.md
theory/SHARP_BINARY_UNIT_COST_WORLD_QUERY_RATIO.md
theory/SHARP_BOUNDED_ARITY_UNIT_COST_RATIO.md
theory/SHARP_FRONTIER_EDGE_CAPPED_RATIO.md
theory/FRONTIER_RANK_CAP_IS_EXTREMALLY_VACUOUS.md
theory/GENERAL_BINARY_DYNAMIC_SCOPE_THRESHOLD.md
theory/ARITY_GAP_PARETO.md
theory/DYNAMIC_ARITY_PARETO.md

Disposition: mostly COMPANION.

## 6. Exact-balanced binary geometry

The dedicated 2026-10-01 companion audit identifies this as the strongest
coherent mathematical companion line.

Sharp fixed-side cap, for even n:

max C_F = 1 at n=2,
max C_F = 2 at n=4,
max C_F = n-3 for n>=6.

For n=2h>=8, cap saturation forces the private-pair forest to have component
sizes {h-1,2,h-1}, with both large components stars: the star-edge-star spine.

Inside the saturated vocabulary:

C_A >= h-1 = n/2-1.

Define D_h(n)=max{C_F : C_A<=h} in the exact-balanced binary subclass.

Closed depth-three envelope:

D_3(6)=3,
D_3(8)=5,
D_3(10)=6,
D_3(n)=7 for even n>=12.

The n=10 row is a genuine finite compatibility defect.

Closed depth-four values:

D_4(12)=8,
D_4(14)=10,
D_4(16)=12,
D_4(18)=13,
D_4(n)=15 for even n>=20.

Selected depth-five values:

D_5(16)=12,
D_5(18)=14,
D_5(22)=17.

Yet exact 50/50 balance still permits

C_F/C_A >= 2^d/(d+1) -> infinity.

Canonical branch:
companion/math-priority-audit-v2

Key files:
manuscript/MANUSCRIPT_MATHEMATICAL_COMPANION_V0_2.md
manuscript/MATHEMATICAL_COMPANION_PRIORITY_AUDIT_V3.md

Disposition: COMPANION.
The current ecology Supplement should use only the portions needed as stress
tests or claim support.

## 7. Static information versus adaptive accessibility

This is the mathematics most successfully recovered into the current paper.

For deterministic exact resolution and any full-support prior:

C_F = min_{S:I(T;Q_S)=H(T)} c(S).

Thus the complete static subset-information function determines C_F.

The 12-state paired tasks have:

- identical physical cue matrices;
- identical target multiplicities;
- identical named subset-information values;
- identical complete Shannon entropy vectors over target plus all cues;
- identical C_F=4;

but C_A=4 versus C_A=3.

Therefore complete static Shannon information does not determine adaptive
accessibility.

Cartesian products preserve complete entropic equivalence and give

(4r,4r) versus (3r,4r),

so the additive adaptive-cost difference grows as r.

The same physical cue environment can also have sharply different
adaptive/fixed geometry when only the focal action map changes.

Canonical sources:
theory/STATIC_INFORMATION_ADAPTIVE_ACCESS_THEOREM.md
theory/QUANTITY_TOPOLOGY_ORTHOGONALITY.md
theory/ROUTEABILITY_SUMMARY_SUFFICIENCY_LADDER.md
theory/RELATIONAL_ROUTEABILITY_THEOREM_SPINE_V1.md

Disposition: MAIN.

## 8. Hard budgets and eco-evolutionary dynamics

The direct ecological budget result is

C_A <= B < C_F.

A separate threshold-selection model maps exact success into fitness.

The nonlinear no-go uses state-specific gaps g_i, contrast Delta g, a
nondecreasing L-Lipschitz sensing-to-selection lift, and feedback scale B_f:

G <= B_f L Delta g.

If a requested oscillatory local regime requires G>G_osc, then

Delta g > G_osc/(B_f L)

is necessary.

The broader dynamical stack also contains:

- structural-spectral joint ceilings;
- reward-mode alignment;
- structural loop-gain phase diagrams;
- phase-exclusion bounds;
- transient-time ceilings;
- critical slowing;
- compatible complex modes forcing feedback existence in the declared local
  model;
- nonidentifiability of persistence/memory/feedback decomposition;
- cancellation versus restoring stasis.

Sources include:
theory/BUDGET_GATED_EVOLUTIONARY_SELECTION.md
theory/NONLINEAR_LIFT_NO_GO_V2.md
theory/STRUCTURAL_SPECTRAL_JOINT_BOUND.md
theory/STRUCTURAL_LOOP_GAIN_PHASE_DIAGRAM.md
theory/STRUCTURAL_PHASE_EXCLUSION_BOUNDS.md
theory/GENERAL_EVOLUTIONARY_RESPONSE.md
theory/GENERAL_RESPONSE_IDENTIFIABILITY.md
theory/FEEDBACK_EXISTENCE_FROM_OSCILLATION.md
theory/TWO_ORIGINS_OF_STASIS.md

Disposition:
budget window = MAIN;
nonlinear no-go = secondary MAIN, but priority should be reconsidered under the
new behavioural-ecology framing;
spectral/identifiability = SUPPLEMENT or SEPARATE;
full phase/transient/stasis stack = SEPARATE/ARCHIVE for this paper.

## 9. Temporal and noisy routing — high-value unrecovered decision-ecology line

This line lives on branch theory/ecological-state-observability and is not
adequately represented in the current synthesis manuscript.

### Minimal temporal theorem

The route cue in the minimal four-world core has

I(T;q_route)=0.

Let P(C_1=C_0)=rho. The best fixed two-query policy has

A_F^(2)=3/4,

whereas the best contingent two-query policy has

A_A^(2)=3/4 + |2rho-1|/4.

Hence

G_time=|2rho-1|/4,

with strict routing value iff rho != 1/2.

Positive persistence and predictable alternation both create value; temporal
independence destroys it.

With classification value s and control cost k, routing is favoured iff

|2rho-1| > 4k/s.

### Arbitrary binary transition kernel

PREDICTIVE_CUE_USEFULNESS_THEOREM.md shows that current context can predict
future context yet have zero routing value if the same specialist remains
optimal in every current context.

The relevant ecological quantity is therefore:

action-relevant predictability of future cue usefulness.

### Noisy exact factorization

With signed temporal predictability phi=2rho-1, routing reliability
eta_R=2a-1, and specialist reliability eta_S=2b-1:

A_A^(2)-A_F^(2) = |phi| eta_R eta_S / 4.

With target-accuracy value v and control cost k, contingent routing is favoured
iff

|phi| eta_R eta_S > 4k/v.

Canonical sources:
branch theory/ecological-state-observability
theory/TEMPORAL_ROUTING_THRESHOLD.md
theory/PREDICTIVE_CUE_USEFULNESS_THEOREM.md
theory/NOISY_TEMPORAL_ROUTING_FACTORIZATION.md
theory/EVOLUTIONARY_INFORMATION_ROUTING.md

Disposition: REASSESS FOR CURRENT PAPER, otherwise a natural second
decision-ecology paper.

This line is now unusually relevant because the current manuscript asks what
makes ecological decisions difficult. It gives the exact biological statement:

an early cue may matter not because it predicts the target, but because it
predicts which later cue should be sampled.

## 10. Local mutation and finite-population routing evolution

Branch stack results include:

- exact local edit distance kr to realized gain r in the k-branch routing
  representation;
- first beneficial one-event mutation radius rho_first=k;
- direct gain-r radius rho_direct=kr;
- for the query-minimal required-gap specialization k=q+1, full gain q requires
  q(q+1) local edits;
- the first k-1 elementary edits are neutral in worst-path gain;
- under uniform branch proposals, first-gain waiting is a coupon collector with
  E[T_first]=k H_k;
- exact occupancy-chain lumping for full-target waiting;
- canonical q=2 full-target mean 347/36 attempts.

A declared Moran origin-fixation layer gives, for theta=a^(N-1),

pi(x) proportional to theta^(g(x)),

with gain-layer multiplicity

D_r=(q-r+1)^k-(q-r)^k.

The full-gain layer is stationary-modal iff

theta >= 2^k-1 = 2^(q+1)-1.

Later exact counterexamples show that q and phenotype fitness do not identify:

- shortest mutational accessibility;
- stationary phase occupancy;
- absolute waiting-time scale.

Even with fixed local gain-path support, arbitrary positive stationary gain
laws can be obtained by changing the reversible neutral mutation measure.
Overall proposal-rate scaling changes hitting time as 1/epsilon while leaving
stationary proportions fixed.

Canonical branches:
theory/local-routing-mutation-accessibility
theory/routing-neutral-plateau-dynamics
theory/routing-full-target-mesoscopic
theory/routing-origin-fixation-selection
theory/routing-representation-dependence
theory/routing-reversible-mutation-certificate
theory/routing-stationary-nonidentifiability
theory/routing-rate-scale-nonidentifiability
theory/downstream-population-nonidentifiability-ceiling

Disposition: SEPARATE.

The branch's own hard stop is correct: biological interpretation requires a
justified genotype-policy map, mutation locality, mutation bias and population
process.

## 11. Topology-to-sensing bridge side theory

The cross-repository bridge establishes:

- bare topology does not identify g;
- the pair (K_A,H_min) with resource costs is sufficient;
- changing one context-obligation semantic can change the exact gap and alter
  the required topology cut;
- local accessibility and structural capability are separate gates.

Canonical branch:
theory/reachability-admissibility-synthesis

Disposition: SEPARATE, except the two-sided factorization should be recovered
as Supplementary structural interpretation.

## 12. OU / evolutionary time-series congruence line

A distinct branch studies partially observed linear-Gaussian evolutionary
models.

Stationary two-state OU:
real modes admit an observation-equivalent realization with no reciprocal
feedback; complex modes force reciprocal restoring feedback, while magnitude
remains unidentified.

evoTS moving-optimum:
a continuum of reciprocal-feedback latent realizations can reproduce exactly
the same observed trait law as the one-way moving-optimum OUBM model.

paleoTS fixed-optimum:
the fitted OU relaxation rate remains an observable model-conditional rate, but
its attribution wholly to a one-way direct attraction coefficient is not
identified from the trait series alone.

Adaptation-half-life identified set:
the conventional one-way half-life is the lower endpoint of the direct-response
half-life set; without added latent-structure constraints, there is no finite
upper bound.

Common-shock sensitivity:
an external bound on hidden common-shock covariance yields a finite sensitivity
envelope for mechanistic half-life.

Canonical branch:
analysis/evoTS-moving-optimum-audit

Key files:
theory/CONTINUOUS_OU_CONGRUENCE_GATE.md
theory/EVOTS_MOVING_OPTIMUM_CONGRUENCE.md
theory/PALEOTS_FIXED_OPTIMUM_CONGRUENCE.md
theory/ADAPTATION_HALFLIFE_IDENTIFIED_SET.md
theory/COMMON_SHOCK_SENSITIVITY_BOUND.md
theory/CAUSAL_ATTRIBUTION_ASSUMPTION_GATE.md

Disposition: SEPARATE PAPER.

## 13. Perturbation / observation design

A side branch derives exact factorization of two-mode transient visibility into
perturbation-side excitation and observation-side projection, with scale-free
design scores and exact finite-candidate separability.

Canonical branch:
theory/perturbation-observability-design

Source:
theory/PERTURBATION_OBSERVABILITY_DESIGN.md

Disposition: SEPARATE/ARCHIVE.

## 14. Current manuscript coverage

The current manuscript already recovers the mathematically central claims:

1. finite C_A/C_F distinction;
2. exact static characterization of C_F;
3. complete-Shannon-equivalent tasks with different C_A;
4. additive product amplification;
5. relational routeability on one physical cue environment;
6. exact finite budget window;
7. exact-balanced unbounded-ratio result under weaker matching;
8. nonlinear monotone-Lipschitz reachability no-go as a secondary consequence.

The current proof supplement additionally retains pairwise-information and
exact-balanced stress controls, Bellman interpretation, spectral recurrence
notes, general-response identifiability notes, and selected exact-balanced
extremal geometry.

Therefore the current paper has not lost its central theorem spine.

## 15. Genuine recovery gaps

### Gap A — two-sided structural factorization

The main/supplement does not yet state the strongest exact structural split:

g = tau_c(H_min) - V_A(K_A),

nor the paired counterexamples proving that either side alone is insufficient.

Recommendation: add to the proof supplement, not the main Results.

### Gap B — temporal/noisy routing

The current manuscript discusses sequential decisions biologically but omits
the repository's exact dynamic result that a routing cue can have zero direct
target information while gaining value entirely from predicting which future
cue is useful.

Recommendation: scientific reassessment before submission.

Two defensible options:

1. keep the current paper purely deterministic and freeze temporal/noisy routing
   as the next decision-ecology paper; or
2. replace/demote the eco-evolutionary no-go secondary result with one compact
   temporal-routing result because it is more directly connected to animal
   decision-making.

Do not add both merely to maximize theorem count.

## 16. Results intentionally outside the current paper

Correctly excluded:

- proof-DAG and symmetry machinery;
- full normal-form catalogues;
- most sharp fixed-(n,m,b) extremal formulas;
- the exact-balanced companion's full finite D_h(n) program;
- local routing mutation distances;
- coupon-collector/mesoscopic waiting laws;
- origin-fixation stationary occupancy;
- representation/mutation-bias/rate-scale nonidentifiability;
- topology-to-sensing mutation bridges lacking a biological genotype map;
- OU/evoTS/paleoTS congruence;
- perturbation-observability design.

These are not failures of recovery; they are separate mathematical programs.

## 17. Final disposition map

| Mathematical family | Disposition |
|---|---|
| C_A <= C_F, budget interval | MAIN |
| Static information determines C_F | MAIN |
| Complete Shannon vector does not determine C_A | MAIN |
| Entropic twin product amplification | MAIN |
| Relational routeability | MAIN |
| Nonlinear feedback no-go | secondary MAIN; reconsider priority |
| Continuation/frontier two-sided factorization | SUPPLEMENT — recover |
| Productive-frontier / Bellman kernels | COMPANION / selected SUPPLEMENT |
| Bypass/certificate/proof-compression machinery | ARCHIVE / COMPANION |
| Minimal normal forms | COMPANION / experimental-design support |
| Generic sharp ratios / bounded arity | COMPANION |
| Exact-balanced finite geometry | COMPANION |
| Temporal/noisy routing | REASSESS — high relevance to current framing |
| Local mutation / neutral plateau / mesoscopic waiting | SEPARATE |
| Origin-fixation / stationary routing evolution | SEPARATE |
| Representation / mutation-bias / rate-scale no-go | SEPARATE |
| Topology-to-sensing bridge | SEPARATE, except factorization |
| Spectral recurrence / local response identifiability | SUPPLEMENT / SEPARATE |
| OU/evoTS/paleoTS congruence | SEPARATE PAPER |
| Perturbation-observability design | SEPARATE |

## 18. Bottom line

The repository has produced substantially more mathematics than the present
paper should contain.

The correct recovery goal is not to put every theorem in one Letter. It is:

one biological question
+ the minimum theorem set needed to answer it
+ a complete provenance map for everything else.

Under the current question

When does ecological diversity become effective decision complexity?

the complete-static-information theorem is the main mathematical result.

The most valuable unrecovered structural result is the two-sided
continuation/frontier factorization.

The most valuable unrecovered biological-mathematical result is the
temporal/noisy routing line.

Everything else is now accounted for and has an explicit destination.
