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

Read `PERTURBATION_OBSERVABILITY_DESIGN.md` for the full derivation and natural-history interpretation.

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

Prior-art boundary: this is standard 2x2 observability/controllability geometry. The repository-specific role is to place experimental design before the eco-evolutionary inverse chain

```text
perturbation + observation
    -> two-mode visibility
    -> T,D
    -> independent alpha or phi
    -> generalized gain G
    -> finite sensing-gap compatibility / falsification
```

No noise-optimal design, multivariate sensor selection, constrained field-design optimization, or nonlinear global perturbation theory is claimed yet.
