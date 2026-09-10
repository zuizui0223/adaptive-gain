# Structural selection collision from an existing repository counterexample

## Purpose

This note reuses an existing exact information-loss result as an evolutionary counterexample.

The repository already registers `resource_role_profile_collision()`: two finite tasks have

- the same adaptive continuation root type;
- the same multiset of complete per-resource abstract role profiles;
- the same adaptive cost `C_A=2`;
- different fixed costs `C_F=2` and `C_F=3`.

Thus

\[
\boxed{
\text{continuation type + per-resource role profiles}
\not\Rightarrow C_F.
}
\]

---

## Minimal evolutionary lift

Under the branch's cost-to-log-fitness map

\[
s(X)=\lambda[C_F(X)-C_A(X)]-\kappa,
\]

choose

\[
\lambda=1,
\qquad
\kappa=1/2.
\]

For the no-gain member,

\[
C_A=C_F=2,
\]

so

\[
\boxed{s_-=-1/2.}
\]

For the strict member,

\[
C_A=2,
\qquad
C_F=3,
\]

so

\[
\boxed{s_+=+1/2.}
\]

Hence

\[
\boxed{
\text{two tasks with the same adaptive continuation and the same marginal resource-role summary can exert opposite selection on contingent sensing.}
}
\]

This is not a new combinatorial counterexample; it is a new interpretation of an already-audited repository collision.

---

## Ecological meaning

Suppose two community states expose an organism to cue systems with the same

- apparent adaptive decision depth;
- distribution of abstract cue roles across resources;
- marginal resource-role profile.

Those summaries still need not determine whether a fixed sensory architecture has a cheap bypass.

The difference can reside in **which cue roles co-occur in the same concrete ecological states**.

Therefore the evolutionary value of contingent sensing can depend on higher-order cue-obligation structure even when marginal cue summaries look the same.

This motivates the prediction

\[
\boxed{
\text{marginal cue prevalence or average informativeness alone may fail to predict selection on sensory routing.}
}
\]

A more informative empirical object is the state-conditioned co-location structure of cue usefulness.

---

## Why this matters for community ecology

Community change often alters combinations rather than only marginal frequencies:

- partner species co-occur in new combinations;
- cues that were previously separated become simultaneously available;
- a cue becomes a universal shortcut in some interaction contexts;
- redundant cues become co-located within the same natural-history stage.

The existing collision says that such rearrangement can change `C_F` while leaving adaptive continuation and weaker per-resource summaries unchanged.

Under the minimal evolutionary lift, that is enough to reverse selection.

So the proposed individual-to-community bridge is not merely

```text
community composition -> cue frequency -> selection.
```

It can require

```text
community composition
-> higher-order cue co-location / productive frontier
-> fixed bypass structure
-> C_F - C_A
-> selection on sensory architecture.
```

The executable test is `tests/test_structural_selection_collisions.py`.
