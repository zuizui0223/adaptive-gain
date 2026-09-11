# Reachability and admissibility synthesis

Status: side-theory synthesis. This note is **not** part of the frozen Theoretical Ecology submission and must not be merged into that submission surface without a fresh claim audit.

## 1. Common problem revealed across MROD, PAYOFF, BALANCE, and adaptive-gain

The cross-repository development repeatedly separated statements that are easy to collapse in prose but are mathematically different:

```text
possible
!=
accessible
!=
identifiable
!=
claimable
```

The four words are not a single total order in every model. They are distinct gates. A result may pass one gate and fail another, and some gates require model-specific bridges before they can even be compared.

The current synthesis therefore treats `reachability` as the umbrella question:

> What additional structure must be declared before a formally possible state, mechanism, or dynamical regime becomes accessible, identifiable, or scientifically reportable?

This is a schema for organizing exact results from the source repositories. It is not claimed as a new general theorem.

## 2. Gate A — declaration / admissibility

MROD's empirical observation contract requires the represented support, target, world weights, candidate likelihoods, and calibration assumptions to be declared before identification. It explicitly separates mathematical identification from permission to make a scientific report and explicitly states that no human informed-consent model is implemented.

The useful transfer to adaptive-gain is therefore **not** a human-consent formalism. It is the declaration rule:

```text
biology/natural history declares the admissible worlds, cues, targets, and calibration scope;
mathematics computes consequences only inside that declared object.
```

This principle is already reflected in the current manuscript: finite sensing theory does not decide which ecological alternatives or cues are biologically meaningful.

**Theorem status:** methodological/admissibility rule; no novelty claim.

## 3. Gate B — local evolutionary accessibility

PAYOFF's bounded-interaction extension makes mutation locality explicit. On a finite grid, mutation mass can move only within a declared jump radius. The corresponding continuous hard-cutoff calculation gives an exact escape threshold

```text
delta_escape = epsilon - x*
```

under the assumptions in `HARD_CUTOFF_ESCAPE_THEOREM.md`.

Thus

```text
globally better architecture exists
```

does not imply

```text
a lineage restricted to sufficiently small uphill jumps can reach it.
```

The conceptual lesson is that optimization and accessibility are different objects.

**Theorem status:** HCE1 is exact for the declared PAYOFF hard-cutoff model; the general small-jump principle is established prior art in adaptive dynamics.

## 4. Gate C — bounded interaction and local-versus-nonlocal fate

PAYOFF replaces globally coupled quadratic interaction by

```text
H_epsilon(r,q) = -gamma (r-q)^2 1{|r-q| <= epsilon}.
```

This is structurally analogous to Hegselmann-Krause bounded-confidence interaction, but the state variable is a heritable architecture rather than an opinion.

Two exact distinctions matter:

1. for every finite positive `epsilon`, the strictly local branching curvature and threshold remain the same as in the global quadratic kernel;
2. the nonlocal population fate can nevertheless change because the interaction term disappears once architectures separate beyond `epsilon`.

Therefore

```text
local branching compatibility
!=
nonlocal branch separation / endpoint fate.
```

The hard cutoff additionally creates a one-sided payoff interface of size `gamma epsilon^2`.

**Theorem status:** the local-threshold invariance and cutoff-interface statements are exact propositions for the declared PAYOFF model; Hegselmann-Krause / bounded-confidence interaction itself is prior art.

## 5. Gate D — mesoscopic population fate

PAYOFF's mesoscopic layer promotes a monomorphic architecture coordinate to a population distribution

```text
f(r,t).
```

Selection reweights the distribution by payoff, while mutation redistributes mass locally. A small-jump scaling motivates a replicator/advection/diffusion description, but the repository deliberately does not claim that the finite-grid implementation is an exact Fokker-Planck solver.

The finite-grid phase atlas keeps two outputs separate:

```text
dynamical_regime
small_jump_trapped
```

and demonstrates that, in the tested grid,

```text
more accessible != more differentiated.
```

A larger mutation radius can remove an all-uphill accessibility barrier while also reconnecting or smoothing the distribution enough to erase a separated-cluster phase.

**Theorem status:** the finite-grid outcomes are reproducible numerical results, not continuum PDE theorems. Replicator-mutator and mesoscopic trait-distribution dynamics are established prior art.

## 6. Gate E — finite sensing structural reachability

adaptive-gain extracts only the finite decision structure needed for contingent versus fixed target resolution. For each declared task,

```text
C_A = minimum worst-path adaptive cost
C_F = minimum fixed resolving cost
g   = C_F - C_A.
```

The early repository established exact finite combinatorics for `C_A`, `C_F`, productive frontiers, fixed-versus-adaptive gaps, and sharp bounded-arity extrema. The current flagship does not claim generic decision-tree or adaptivity-gap novelty.

The later eco-evolutionary layer declares

```text
G = a Delta g
```

and uses the local response model to derive the first integer gap `q` required for a requested regime. The principal reverse map is

```text
required local dynamical regime
-> required structural gap q
-> minimum / Pareto-minimal finite (n,m,E) sensing structure.
```

For bounded cue arity this generally returns a Pareto frontier rather than one scalar complexity value.

**Theorem status:** this reverse finite-structure reachability map is the principal theorem of the current adaptive-gain manuscript.

## 7. Gate F — model compatibility and mechanistic identifiability

For the generalized local model,

```text
T = alpha + phi
D = alpha phi + (1-phi)G
```

with `0 <= alpha <= 1` and `0 <= phi < 1`, a persistence split exists exactly when

```text
0 <= T < 2.
```

Only after that compatibility gate is passed does a non-real local eigenpair imply that every feasible decomposition has

```text
G > 0.
```

The magnitude of `G` remains unidentified.

Thus even inside the current flagship:

```text
oscillation observed
!=
feedback magnitude identified
```

and, outside the trace domain,

```text
complex transient
-> model incompatibility,
```

not a feedback-existence claim.

**Theorem status:** exact diagnostic theorem inside the declared generalized local model; not a generic system-identification theorem.

## 8. What really connects the four motivating concepts

The strongest common principle is not a shared equation but a repeated refusal of invalid implication:

```text
MROD declaration discipline:
identified ->/-> scientifically reportable

PAYOFF small-jump layer:
globally better ->/-> locally accessible

PAYOFF bounded interaction:
local branching criterion ->/-> nonlocal population fate

PAYOFF mesoscopic layer:
accessible ->/-> differentiated

adaptive-gain finite reachability:
mathematically available feedback phase ->/-> structurally reachable from a declared sensing architecture

adaptive-gain diagnostic:
model-compatible oscillation -> feedback exists,
but ->/-> feedback magnitude identified.
```

This is the conceptual lineage that survived into the current theory.

## 9. Cross-repository double-gate exclusion principle

A biological hypothesis can require more than one gate simultaneously. For example, suppose a proposed evolutionary route requires both:

1. reaching an architecture region through a declared mutation process; and
2. once there, possessing enough finite sensing structure to support a requested local feedback phase.

Then the route is excluded if **either** necessary gate fails:

```text
mutation accessibility fails
OR
finite structural reachability fails
-> proposed route is excluded under the joint declared model.
```

This conjunction is logically useful but is **not** itself claimed as a new theorem.

At present the two exact thresholds live in different coordinates:

```text
PAYOFF:        architecture coordinate r and jump threshold delta_escape
adaptive-gain: finite task structure and required gap q
```

There is currently no exact map

```text
psi: r -> finite task S(r)
```

that would justify combining `delta_escape` and `q` numerically. Any paper that writes them into one inequality before constructing `psi` would be overclaiming.

## 10. The genuinely open bridge

The next mathematically meaningful problem is to define a biologically declared map

```text
psi: architecture state r -> finite sensing task S(r)
```

or, more generally, a map from an architecture state space into a family of finite decision problems.

Let

```text
g(r) = C_F(S(r)) - C_A(S(r)).
```

For a mutation radius `delta`, define the induced structural jump modulus

```text
J_g(delta)
= sup{|g(r')-g(r)| : d(r,r') <= delta and both states are admissible}.
```

If a target regime requires gap at least `q` and the current architecture has gap `g0`, then every `k`-step path whose steps are at most `delta` satisfies

```text
g_k <= g0 + k J_g(delta).
```

Hence, whenever `J_g(delta)>0`, a necessary path-length bound is

```text
k >= ceil((q-g0)_+ / J_g(delta)).
```

and if `J_g(delta)=0` while `g0<q`, the regime is structurally unreachable under that mutation radius.

This inequality is elementary once `psi` is declared. The nontrivial scientific work is constructing and validating `psi`, characterizing `J_g(delta)`, and determining whether the PAYOFF hard-cutoff accessibility barrier and the adaptive-gain structural threshold interact nontrivially in a biological architecture family.

**Status:** candidate bridge problem, not a result of the current manuscript.

## 11. Novelty discipline

Do not claim novelty for:

- informed consent or ethical consent models;
- precommitment / admissibility as a general scientific principle;
- rare/small mutations in adaptive dynamics;
- Hegselmann-Krause or bounded-confidence models;
- replicator-mutator / Fokker-Planck / mesoscopic trait-distribution models;
- local branching criteria;
- decision trees, separating systems, test cover, or generic adaptivity gaps;
- generic local/global or existence/accessibility distinctions.

The strongest current novelty candidate remains narrower:

```text
required local eco-evolutionary regime
-> required adaptive/fixed structural gap
-> exact minimum or Pareto-minimal finite deterministic sensing architecture.
```

A second, future novelty candidate would require completing the missing `psi` bridge so that mutation-scale accessibility can be composed with finite sensing reachability without changing coordinates by assertion.

## 12. Source lineage

### adaptive-gain

Current frozen scientific bundle baseline:

`a505aea386e477bffccbe1a14f575564c940730a`

Relevant internal surfaces:

- `theory/PAPER_THEOREM_SPINE.md`
- `manuscript/PRIOR_ART_AUDIT_V2.md`
- `theory/PROVENANCE.md`

### PAYOFF

Current inspected mesoscopic source state from public repository search:

`3cad45d09a3fd9b691e4b23fd363ed3290e12f98`

Relevant surfaces:

- `theory/MESOSCOPIC_ARCHITECTURE_DYNAMICS.md`
- `theory/BOUNDED_INTERACTION_PHASE_ATLAS.md`
- `theory/HARD_CUTOFF_ESCAPE_THEOREM.md`
- `docs/ADAPTIVE_PHASE_DESIGN.md`

The original adaptive-gain PAYOFF witness was extracted from the earlier source state recorded in `theory/PROVENANCE.md`.

### MROD

Current inspected empirical-contract source state from public repository search:

`345883a4ecbeea3bc1b7beb18ed6475d1151f2c7`

Relevant surface:

- `docs/EMPIRICAL_IDENTIFICATION_CONTRACT.md`

The original adaptive-gain MROD routing witness was extracted from the earlier source state recorded in `theory/PROVENANCE.md`.

## 13. Submission boundary

This note belongs on a side-theory branch. It should not be merged into the frozen Theoretical Ecology submission merely because the concepts are connected. The current flagship is stronger for keeping the mesoscopic and observation-contract layers out of the main theorem spine.
