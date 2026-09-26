# Reachability synthesis prior-art ledger

Status: side-theory novelty audit accompanying `REACHABILITY_ADMISSIBILITY_SYNTHESIS.md`. This ledger is intentionally conservative.

## 1. What the synthesis does not make new

### Small-jump / rare-mutation adaptive dynamics

Adaptive dynamics has long used rare mutations and small mutational steps to derive trait-substitution and canonical-equation limits. Evolutionary branching theory also explicitly distinguishes local branching conditions from outcomes when mutation effects or rates depart from the idealized regime.

Therefore the synthesis must not claim novelty for:

- the small-jump assumption;
- local mutation neighbourhoods;
- canonical adaptive dynamics;
- the fact that finite jumps can alter accessibility or long-run outcome.

Representative anchors include Dieckmann & Law-style canonical adaptive dynamics, the 2005 `20 Questions on Adaptive Dynamics` review, and later jump/diffusion derivations.

### Hegselmann-Krause / bounded confidence

Hegselmann-Krause and related bounded-confidence models already formalize interaction only among sufficiently similar states and are known to generate multiple clusters and confidence-radius-dependent dynamics.

PAYOFF uses only a structural analogy: finite interaction range in architecture space. It does not turn the biological model into an opinion-dynamics model.

Therefore do not claim novelty for:

- finite interaction radius;
- bounded-confidence clustering as an abstract mechanism;
- confidence-radius-dependent fragmentation or consensus.

### Mesoscopic / replicator-mutator trait distributions

Trait-distribution, replicator-mutator, nonlocal reaction-diffusion, and Fokker-Planck-like evolutionary models are established. Rigorous and numerical work already studies mutation-selection distributions and evolutionary branching.

Therefore do not claim novelty for:

- promoting a monomorphic trait to a density `f(r,t)`;
- selection-mutation redistribution;
- diffusion limits from small mutations;
- branching in a replicator-mutator equation.

PAYOFF's finite-grid implementation is a repository-specific bridge and numerical atlas, not a new general mesoscopic formalism.

### Identification versus scientific reportability

The distinction between statistical/model identification and the broader evidential conditions needed for a scientific claim is not a novelty claim. MROD's contribution here is operational discipline: declared support, target, likelihood and calibration are kept separate from report licensing.

No human informed-consent model is present in the source implementation.

### Decision trees, separating systems, adaptivity gaps

The adaptive-gain static layer overlaps established decision-tree, separating-system, test-cover and adaptive-search theory. The current manuscript already records this boundary.

## 2. What survives as a defensible novelty candidate

After removing the established ingredients above, the strongest current candidate remains:

> A required local eco-evolutionary feedback regime is mapped backward to a required adaptive/fixed structural gap and then to an exact minimum or Pareto-minimal finite deterministic sensing architecture over represented alternatives, declared cues, and irreducible fixed-side obligations.

This is narrower than generic `required performance -> required information` because Moffett & Eckford (2022) already derive minimum mutual-information requirements for target fitness/selection using rate-distortion theory.

The distinguishing object is the finite deterministic structure `(n,m,E)` and the downstream target is a local feedback phase.

## 3. Why the four-concept synthesis is not itself a priority claim

The slogan

```text
possible != accessible != identifiable != claimable
```

is useful as a research-program summary but is too general to support a mathematical novelty claim. Similar distinctions occur throughout dynamical systems, control, adaptive dynamics, inverse problems, statistics and philosophy of science.

The synthesis should therefore be cited internally as an organizing schema, not a theorem.

## 4. The future bridge that could become genuinely new

The current repositories still lack an exact map from a continuous/heritable architecture state to a finite sensing task:

```text
psi: r -> S(r).
```

Without `psi`, the PAYOFF mutation threshold `delta_escape` and adaptive-gain structural threshold `q` cannot be combined numerically.

If `psi` can be biologically justified, define

```text
g(r)=C_F(S(r))-C_A(S(r))
```

and structural jump modulus

```text
J_g(delta)=sup{|g(r')-g(r)| : d(r,r')<=delta}.
```

Then a target regime requiring `g>=q` inherits path-length and impossibility bounds from `J_g(delta)`. The algebraic path-length bound is elementary; possible novelty would have to come from a nontrivial biological/structural characterization of `psi` or `J_g`, or from an exact interaction between mutation accessibility and finite sensing reachability.

This is the place where new theory should be sought rather than by relabelling HK, small-jump or mesoscopic machinery.

## 5. Current search outcome

A targeted search recovered substantial prior art for each ingredient separately:

- small-mutation and branching assumptions in adaptive dynamics;
- bounded-confidence/Hegselmann-Krause interaction;
- replicator-mutator and trait-distribution branching;
- information-fitness and minimum-information theory;
- decision trees and fixed/adaptive separation.

No exact predecessor was located in this search for the complete composition

```text
required local feedback phase
-> required integer adaptive/fixed gap
-> minimum/Pareto finite (n,m,E) sensing structure.
```

This is a search result, not proof of priority. Continue to avoid `first`, `first-ever`, `no previous theory`, or generic `minimum information` language.

## 6. Literature anchors

### Adaptive dynamics / small mutations

- Geritz et al. / Dieckmann-Law adaptive-dynamics lineage: rare, small mutations and canonical evolutionary change.
- Waxman & Gavrilets 2005, `20 Questions on Adaptive Dynamics`, Journal of Evolutionary Biology 18:1139-1154, DOI 10.1111/j.1420-9101.2005.00948.x.
- Champagnat & Lambert lineage: trait-substitution jump process and small-mutation diffusion limits.

### Bounded confidence

- Hegselmann-Krause bounded-confidence model and subsequent mathematical analyses.
- Li, Luo & Porter 2024, adaptive confidence bounds, SIAM Journal on Applied Dynamical Systems, DOI 10.1137/23M1558951.

### Mesoscopic / replicator-mutator

- Calsina & Cuadrado 2004, small mutation rate and evolutionarily stable strategies, Journal of Mathematical Biology 48:135-159, DOI 10.1007/s00285-003-0226-6.
- Alfaro & Veruete 2018, evolutionary branching via replicator-mutator equations, arXiv:1802.00501 and related publication lineage.

### Information-fitness / finite decision structure

Use the references already frozen in `manuscript/PRIOR_ART_AUDIT_V2.md`, especially Donaldson-Matasci et al. 2010; Rivoire & Leibler 2011; Moffett & Eckford 2022; Katona 1966; Hyafil & Rivest 1976; Chakaravarthy et al. 2009.

## 7. Claim recommendation

For any future companion paper, the novelty sentence should be no broader than:

> We combine an explicitly declared map from heritable architecture to finite sensing tasks with exact adaptive/fixed structural bounds, allowing mutation-scale accessibility and eco-evolutionary phase reachability to be evaluated in the same architecture space.

That sentence is **not yet licensed**, because the required map `psi` has not been built. It records the target novelty condition for future work.
