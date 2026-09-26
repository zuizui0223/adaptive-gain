# Source-semantics audit for the topology-to-sensing bridge

Status: side-theory audit. This file records why the missing map `psi:T->S(T)` cannot currently be inferred from the source repositories without adding a new biological mechanism.

## 1. What PAYOFF topology means

In PAYOFF's `NETWORK_EXTENSION.md`, topology nodes are fitness-relevant functional coordinates and topology edges encode developmental/genetic/structural integration. Weakening or deleting an edge relaxes a coupling penalty between function-specific trait coordinates.

Thus a topology edge is a **functional-integration constraint**.

It is not defined as:

- a sensory channel;
- an environmental cue;
- an observation query;
- an attentional resource;
- a branch-specific decision rule;
- a measurement available to the organism.

PAYOFF's topology mutation graph therefore describes architectural reconfiguration, not cue acquisition.

## 2. What PAYOFF adaptive phase design means

`docs/ADAPTIVE_PHASE_DESIGN.md` defines a finite sequential measurement problem for identifying a phase on a declared finite parameter panel. The adaptive optimizer chooses which response contrast to acquire next after seeing earlier measurements.

Those queries are **researcher-side phase-identification measurements**. The file explicitly separates finite-panel phase identification from mutation support, evolving-resident trapping and continuous-region certification.

Therefore the fact that PAYOFF contains an adaptive measurement tree does not imply that a PAYOFF organismal architecture possesses the corresponding cue-routing mechanism.

## 3. What adaptive-gain extracted

`adaptive-gain/theory/PROVENANCE.md` deliberately preserves only the finite decision structure needed to compare adaptive versus fixed resolution. It copies no PAYOFF runtime model and does not claim that the source measurement queries are organismal sensors.

The current Theoretical Ecology manuscript then interprets the abstract finite task as an organismal sensing problem. This is a valid theoretical model class because natural history is explicitly required to declare the biological alternatives, cues and target distinctions.

But it is an **ecological interpretation of an abstract decision structure**, not a source-derived empirical demonstration that the original PAYOFF topology changes organismal sensing resources.

## 4. Negative source-audit result

The current public PAYOFF source provides no rule of the form

```text
retaining/releasing topology edge e
-> creates/removes cue q
```

or

```text
topology T
-> physically feasible contingent cue graph.
```

Accordingly, mappings such as

```text
one released edge = one new cue
```

or

```text
more modular topology = larger adaptive/fixed sensing gap
```

would currently be post hoc assumptions.

They must not be used to manufacture a numerical joint PAYOFF/adaptive-gain result.

## 5. What would license psi(T)

A defensible bridge needs one additional mechanistic layer. At least one of the following would suffice in principle.

### Route A — source biology already couples integration to sensing

Find a biological source system in which the retained/released functional coupling graph directly controls which sensory variables can be sampled, routed or acted on independently.

Then topology semantics already imply cue semantics.

### Route B — add a mechanistic transduction model

Declare a model that maps functional integration to sensor/decision resources before calculating adaptive gain. For example, an edge might constrain two functions to share a sensor or controller, whereas edge release might permit separate branch-specific sensing.

The mapping rule must be fixed before evaluating `C_A`, `C_F` or `g`.

### Route C — use a different architecture state space

Instead of PAYOFF's developmental/genetic integration topology, choose a source system whose architecture states are already sensing/decision networks. Then `psi` may be identity or nearly so.

## 6. Consequence for current novelty

This negative result does **not** weaken the current adaptive-gain flagship theorem. That theorem is conditional on a declared finite sensing task and does not claim to derive organismal cue architecture from PAYOFF topology.

It does block a stronger cross-repository claim:

```text
PAYOFF topology mutation
-> adaptive-gain sensing-gap change
-> feedback-phase reachability
```

is not yet established.

The future novelty target is therefore not merely to combine two existing thresholds. It is to supply a biologically justified bridge that makes the same architecture state control both mutation accessibility and finite sensing structure.

## 7. Submission boundary

No change to the frozen Theoretical Ecology submission is required. If anything, this audit supports the current manuscript's conservative language that natural history must define the feasible sensing architecture.
