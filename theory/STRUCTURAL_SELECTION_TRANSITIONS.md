# Structural selection transitions: two exact eco-to-evo channels

## Status

This note is a direct corollary of the repository's existing exact costs.

For a community state `X`, the minimal structural fitness map on the evolutionary-timescale branch is

\[
s(X)=\lambda[C_F(X)-C_A(X)]-\kappa(X),
\]

where

- `C_A(X)` is determined by adaptive continuation structure;
- `C_F(X)` is determined by the productive frontier;
- `kappa(X)` is an explicitly modeled constitutive/control cost.

For a transition

\[
X\to Y,
\]

subtracting the two selection coefficients gives

\[
\boxed{
\Delta s
=\lambda\Delta C_F
-\lambda\Delta C_A
-\Delta\kappa.
}
\]

No new optimization theorem is required. The usefulness of the identity is ecological: it separates changes in selection on contingent sensing into distinct structural mechanisms already characterized by the repository.

---

## 1. Fixed/frontier channel

Define

\[
\boxed{
\Delta s_F=\lambda[C_F(Y)-C_F(X)].
}
\]

Because `C_F` is determined by the productive frontier, this term records changes in the global fixed burden caused by rearrangement of irreducible cue obligations.

Examples of possible biological interpretations include

- appearance or disappearance of a universal shortcut cue;
- new co-occurrence patterns among partner-specific cues;
- a community rearrangement that makes several formerly exclusive obligations simultaneously coverable;
- loss of a cue that was the sole separator for a biologically relevant state pair.

This channel can change while the optimal adaptive continuation cost does not.

---

## 2. Adaptive/continuation channel

Define

\[
\boxed{
\Delta s_A=-\lambda[C_A(Y)-C_A(X)].
}
\]

This term records changes in the cheapest outcome-contingent continuation itself.

For example, community change may

- add an extra necessary decision stage;
- remove an entire branch of possible continuations;
- change which mixed child states remain after an observation;
- collapse two continuation states into one value-equivalent state.

An increase in `C_A` weakens selection for the contingent phenotype relative to a fixed comparator, all else equal; a decrease strengthens it.

---

## 3. Control-cost channel

Define

\[
\boxed{
\Delta s_\kappa=-[\kappa(Y)-\kappa(X)].
}
\]

This is deliberately kept outside the finite resolution theorem. Physiological, neural, developmental, or maintenance costs of contingent control need empirical or model-specific justification.

The full identity is

\[
\boxed{
\Delta s=\Delta s_F+\Delta s_A+\Delta s_\kappa.
}
\]

---

## 4. Existing resource-overlap collision isolates one channel exactly

The repository already registers `resource_role_profile_collision()`.

Its two tasks have

- the same adaptive continuation root type;
- the same multiset of complete per-resource abstract role profiles;
- `C_A=2` in both tasks;
- `C_F=2` in one task and `C_F=3` in the other.

Therefore, moving from the no-gain member to the strict member gives

\[
\Delta C_A=0,
\qquad
\Delta C_F=1.
\]

With constant control cost,

\[
\boxed{
\Delta s=\lambda.
}
\]

and

\[
\boxed{
\Delta s_A=0,
\qquad
\Delta s_F=\lambda.
}
\]

Thus the entire change in selection is a fixed/frontier-side effect.

This is a useful exact ecological counterexample:

\[
\boxed{
\text{selection can change even when adaptive continuation and marginal per-resource role summaries do not.}
}
\]

The missing information is higher-order resource/state co-location structure that changes the fixed bypass problem.

---

## 5. Timescale consequence

If two community states alternate and differ only through this registered collision, choose a constant control cost halfway between their structural gaps. Then their selection coefficients are equal and opposite.

The community transition changes selection entirely through

\[
\Delta C_F,
\]

while

\[
\Delta C_A=0.
\]

The population can therefore show

- nonzero allele-frequency movement every generation;
- exact return after every two-generation cycle;
- zero long-horizon retained directional change;

without any change in adaptive continuation complexity.

In this witness, rapid reversible evolution is produced specifically by **frontier rewiring**, not by a change in the individual's optimal adaptive decision depth.

---

## 6. Relation to the full structural decomposition

The transition decomposition and the within-state policy decomposition answer different questions.

Within one state,

\[
C_F-C_A
=(U-C_A)-(C_U-C_F)-(U-C_U)
\]

separates branch-exclusive opportunity from external shortcut and internal redundancy.

Across two states,

\[
\Delta s
=\lambda\Delta C_F-\lambda\Delta C_A-\Delta\kappa
\]

separates change in the fixed/productive-frontier problem from change in adaptive continuation and control cost.

Together they give a two-level explanation:

```text
within state:
    why is contingent sensing favoured here?

between states:
    why did selection on contingent sensing change?
```

This is the intended role of the existing `adaptive-gain` mathematics in the eco-evolutionary extension.

---

## 7. Scope

This identity does not establish that a natural community transition actually changes a productive frontier or continuation type. That requires mapping natural-history states and cues into a justified finite task.

It also does not imply that sensing cost is the only component of fitness.

The exact result is conditional:

> given two finite sensing tasks and the stated minimal cost-to-log-fitness map, selection changes decompose exactly into fixed/frontier, adaptive/continuation, and control-cost channels.

Executable implementation: `adaptive_gain/structural_selection_transition.py`.

Regression tests: `tests/test_structural_selection_transition.py`.
