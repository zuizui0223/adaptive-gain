# Perturbation-observability design branch

This dependent branch sits after the generalized observability / identifiability layer and asks a practical question:

> which perturbation and which scalar observable actually expose both local eco-evolutionary modes?

The central factorization is

\[
\boxed{
R=x_0x_2-x_1^2
=
\det\begin{pmatrix}c^\top\\c^\top J\end{pmatrix}
\det\begin{pmatrix}v&Jv\end{pmatrix}.
}
\]

Thus the scalar mode-observability gate closes for two logically distinct reasons:

```text
observation-side blindness
    det([c^T;c^T J]) = 0

perturbation-side blindness
    det([v,Jv]) = 0
```

Read in this order:

1. `PERTURBATION_OBSERVABILITY_DESIGN.md`
   - derives the exact observation-side × perturbation-side factorization;
   - defines scale-free visibility scores;
   - gives the equal-mode optimum for symmetric local dynamics;
   - proves finite candidate-set design separates into independent observation and perturbation choices when feasibility is a Cartesian product.

2. `EXPERIMENTAL_GATE_SUMMARY.md`
   - places the perturbation and observation checks before the PR #6 scalar observability and biological-identifiability gates.

Executable layer:

- `adaptive_gain/perturbation_observability_design.py`
- `tests/test_perturbation_observability_design.py`
- `validation/perturbation_observability_design_v1.json`

Scale-free design scores are

\[
V_O(c)=\frac{|\det([c^\top;c^\top J])|}{\|c\|^2},
\]

\[
V_C(v)=\frac{|\det([v,Jv])|}{\|v\|^2},
\]

and

\[
\boxed{V_R(c,v)=V_O(c)V_C(v).}
\]

For symmetric `J` with eigenvalues `r1,r2`, a single observation or perturbation side is maximized by equal absolute weights on the two orthogonal eigenmodes:

\[
\boxed{V_{side}^{max}=|r_1-r_2|/2.}
\]

If both sides are designable,

\[
\boxed{V_R^{max}=(r_1-r_2)^2/4.}
\]

So a clean local experimental rule emerges:

> do not perturb only one mode and do not measure only one mode; deliberately mix both when possible.

## Finite natural-history candidate sets

If allowed observations form a finite set `C` and allowed perturbations form a finite set `V`, and every observation can be paired with every perturbation, then

\[
\boxed{
\max_{c\in C,v\in V}V_R(c,v)
=
\left(\max_{c\in C}V_O(c)\right)
\left(\max_{v\in V}V_C(v)\right).
}
\]

Therefore the best candidate observable and best candidate perturbation can be selected independently. The executable layer provides both separated selectors and a brute-force cross-check.

If feasibility is joint rather than Cartesian — for example a perturbation prevents a measurement — this reduction is not valid and pairwise constraints must be kept.

Prior-art boundary: this is standard 2x2 observability/controllability geometry and separable product optimization. The repository-specific role is to place experimental design before the eco-evolutionary inverse chain

```text
natural-history candidate perturbations + observables
    -> two-mode visibility
    -> T,D
    -> independent alpha or phi
    -> generalized gain G
    -> finite sensing-gap compatibility / falsification
```

No noise-optimal design, multivariate sensor selection, constrained field-design optimization, or nonlinear global perturbation theory is claimed yet.
