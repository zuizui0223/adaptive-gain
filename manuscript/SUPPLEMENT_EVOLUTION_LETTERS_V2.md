# Supplementary Information — Evolution Letters V3 mathematical architecture

## Purpose and claim ceiling

This Supplement follows `MANUSCRIPT_EVOLUTION_LETTERS_V3.md` and the canonical map `MATHEMATICAL_ATLAS_V1.md`. Its purpose is to expose the mathematical architecture beneath the main biological argument without turning the Letter into a list of proof technologies.

The main paper has five mathematical roles:

1. exact adaptive/fixed resolution and ecological budget windows;
2. target-relevant reduction of raw natural-history structure;
3. sharp extremal architecture and balanced-query counterexamples;
4. two evolutionary lifts: hard-budget selection and nonlinear structural no-go;
5. ecological recurrence and feedback-identifiability boundaries.

The claim ceiling is unchanged throughout. Necessary exclusion bounds are not generic sufficiency; deterministic finite architecture is not Shannon information; balanced-unbounded gain is an existence result; hard-budget selection requires a justified ecological ceiling; exact kernel reductions apply to deterministic worst-path target resolution; slow ecological modes matter only through reward alignment; and feedback-existence diagnostics do not identify feedback magnitude or sensing causality.

---

## S1. Exact finite adaptive gain and the ecological budget interval

Let `W` be a finite represented-world set, `T` a declared target, and `Q` a finite query vocabulary with positive additive acquisition costs.

The minimum fixed resolving-bundle cost is

\[
C_F
=
\min_{F\text{ resolves}}
\sum_{q\in F}c(q).
\]

The minimum adaptive worst-path cost obeys the Bellman recursion

\[
C_A(S,R)
=
\min_{q\in R}
\left[
c(q)+
\max_{y:o_q^{-1}(y)\cap S\ne\varnothing}
C_A(S_{q,y},R\setminus\{q\})
\right]
\]

on unresolved states, with value zero when the target is already constant.

Every fixed resolver is an adaptive policy that ignores intermediate outcomes, so

\[
\boxed{C_A\le C_F.}
\]

For integer or commensurate hard budget `B`, adaptive-only guaranteed resolution occurs exactly when

\[
\boxed{C_A\le B<C_F.}
\]

Thus, when `C_A<C_F`, the adaptive-only budget region is one contiguous interval. Below `C_A` both classes fail; at or above `C_F` both succeed.

### Biological interpretation

The mathematics does not determine what `B` means. A focal natural history can justify a time-to-decision deadline, an energy ceiling, exposure risk, handling-time limit, phenological/developmental window, or opportunity budget. The exact theorem begins only after the biological budget and target are declared.

### Sources

- `theory/ADAPTIVE_GAIN_THEOREM.md`
- exact adaptive/fixed solvers under `adaptive_gain/`
- registered cross-repository finite witnesses and validation tests.

---

## S2. Target-relevant natural-history reduction

### S2.1 Query-side adaptive-safe refinement dominance

At current represented-world state `A`, let `S_A(q)` be the active set of identity-indexed cross-target pairs separated by query `q`.

If

\[
S_A(q)\supseteq S_A(r)
\]

and

\[
c(q)\le c(r),
\]

then `q` is target-relevantly at least as resolving as `r` at no greater root cost. Every unresolved child reached after `q` is a refinement of the corresponding unresolved structure under `r`, and `r` is constant on every unresolved `q`-child. Therefore `r` is safely removable at state `A`.

The equality case, in which two queries induce identical target-mixed continuation families, is a special case.

**Source:** `theory/ADAPTIVE_SAFE_QUERY_COMPRESSION.md`.

### S2.2 World-side quotient

Same-target worlds can be collapsed when they have identical cross-target separation profiles against every opposite-target world under every remaining query. Such worlds are twins for the declared continuation problem: every future target-mixed cell contains the whole twin class or none of it.

**Source:** `theory/ADAPTIVE_WORLD_TWIN_QUOTIENT.md`.

### S2.3 Two-sided Bellman kernel

The world quotient and query refinement-dominance operations are individually value preserving and can be recomputed recursively after every selected query. Their composition preserves the exact adaptive optimum:

\[
\boxed{
C_A^{\rm two-sided}=C_A^{\rm direct}.
}
\]

The representation ladder is

```text
full natural-history world/outcome description
-> full identity-indexed target-pair incidence
-> target-relevant world quotient + nondominated query frontier
-> exact adaptive Bellman value.
```

This gives the main paper's coarse-graining interpretation: descriptive ecological differences can be decision-irrelevant for a declared target without being biologically nonexistent.

**Source:** `theory/ADAPTIVE_TWO_SIDED_KERNEL.md`.

### Validation boundary

The exhaustive validation includes all set partitions of four represented worlds for multiple query combinations, unequal query-cost controls, strict refinement controls, no-progress queries and explicit examples in which both world- and query-side reductions act. The compressed solvers are required to equal the direct Bellman optimum exactly.

These reductions do not automatically extend to noisy likelihoods, expected loss, randomized policies, calibration-changing actions or information-valued objectives.

---

## S3. Sharp finite architecture for a required gap

### S3.1 Binary exact corner

Suppose a state-specific finite task must support structural gap at least integer `q>=1`. Define

\[
h_2^*(q)=\min\{h\ge1:2^h-1-h\ge q\}.
\]

Binary flattening gives `C_F<=2^h-1` for adaptive depth `h`, hence a gap `q` requires `h>=h_2^*(q)`. A productive tree construction attains the boundary exactly.

The first componentwise gap-capable corner is

\[
\boxed{
(n^*,m^*,E^*)
=(h_2^*(q)+q+1,\;h_2^*(q)+q,\;h_2^*(q)+q).
}
\]

Moreover,

\[
h_2^*(q)\in
\left\{
\left\lceil\log_2(q+1)\right\rceil,
\left\lceil\log_2(q+1)\right\rceil+1
\right\},
\]

so

\[
h_2^*(q)=\log_2q+O(1)
\]

and

\[
n^*,m^*,E^*=q+\log_2q+O(1)
\]

up to the displayed constants.

**Source:** `theory/GENERAL_BINARY_DYNAMIC_SCOPE_THRESHOLD.md`.

### S3.2 Bounded arity and Pareto geometry

For cue arity bounded by `b>=2`, define

\[
h_b^*(q)
=
\min\left\{h\ge1:
\frac{b^h-1}{b-1}-h\ge q
\right\}.
\]

Separate minima obey

\[
m_{\min}=E_{\min}=q+h_b^*(q),
\qquad
n_{\min}=q+h_2^*(q)+1.
\]

For `b>2` they need not be jointly attained. The exact structural requirement is therefore generally a Pareto frontier. For `q=3,b=4`, the nondominated points

\[
(7,6,6),\qquad(8,5,5)
\]

show the tradeoff between represented alternatives and cue/frontier burden.

**Sources:**
- `theory/ARITY_GAP_PARETO.md`
- `theory/DYNAMIC_ARITY_PARETO.md`
- associated exact modules, tests and validation receipts.

---

## S4. Exactly balanced binary cues do not bound adaptive gain

Global marginal cue balance might appear to limit the value of contingent acquisition. It does not.

Fix routing depth `d>=1` and let `k=2^d`. Construct `k` target-mixed branch pairs plus two target-0 dummy worlds. Use `d` routing-bit queries and one branch-specific terminal query per branch. Dummy assignments and cyclic terminal assignments can be chosen so that every declared binary query has exactly equal numbers of zero and one outcomes over represented worlds.

For target-mixed pair `(a_j,b_j)`, only its branch terminal `t_j` separates the pair, so every `t_j` is fixed-mandatory. Therefore

\[
C_F\ge k=2^d.
\]

The adaptive strategy uses the `d` routing queries to identify the branch and then one terminal query, so

\[
C_A\le d+1.
\]

Hence

\[
\boxed{
\frac{C_F}{C_A}
\ge
\frac{2^d}{d+1}
\longrightarrow\infty.
}
\]

The construction simultaneously satisfies finite represented worlds, deterministic binary unit-cost queries, exact 50/50 global balance for every query and guaranteed exact target resolution.

### Interpretation

Global marginal cue balance does not control adaptive advantage. The operative structure is branch/resource incidence: fixed resolution must provision every branch-specific terminal resource simultaneously, whereas an adaptive strategy pays routing cost and then only the relevant terminal cost.

### Claim ceiling

This theorem gives an unbounded family/existence lower bound. It does not give the sharp maximum ratio at fixed `(n,m)` under exact balance.

**Source:** `theory/BALANCED_BINARY_UNBOUNDED_ADAPTIVE_GAIN.md`.

---

## S5. Hard-budget evolutionary selection

For ecological state `X`, define

\[
S_A(X,B)=\mathbf 1\{C_A(X)\le B\},
\qquad
S_F(X,B)=\mathbf 1\{C_F(X)\le B\}.
\]

With baseline fitness `w_0>0`, resolution benefit `v>=0`, and log maintenance cost `kappa>=0`, let

\[
W_A=e^{-\kappa}[w_0+vS_A(X,B)],
\qquad
W_F=w_0+vS_F(X,B).
\]

Then

\[
s_B(X)=\log\frac{W_A}{W_F}.
\]

The three exact budget regions are:

1. `B<C_A`: both fail, so `s_B=-kappa`;
2. `C_A<=B<C_F`: adaptive only succeeds, so

\[
\boxed{
s_B=\log\frac{w_0+v}{w_0}-\kappa;
}
\]

3. `B>=C_F`: both succeed, so `s_B=-kappa` under the declared threshold payoff.

Thus contingent architecture is favored in the adaptive-only interval exactly when

\[
\kappa<\log\frac{w_0+v}{w_0}.
\]

Ecological state changes can move `[C_A(X),C_F(X))` relative to a fixed organismal budget and thereby generate state-dependent selection.

A repository-native witness uses one state with `(C_A,C_F)=(2,3)` and another with `(2,2)` at `B=2`, producing opposite selection signs for a suitable positive maintenance cost without a linear cost-to-fitness map.

**Source:** `theory/BUDGET_GATED_EVOLUTIONARY_SELECTION.md`.

### Claim ceiling

This is a threshold payoff model conditional on exact deterministic resolution. It does not yet model graded accuracy, stochastic cue errors, continuous time-to-decision or heterogeneous individual budgets.

---

## S6. Nonlinear structural no-go theorem

For two ecological states define state-specific structural gaps

\[
g_i=C_F(i)-C_A(i)\ge0
\]

and ordered contrast

\[
\Delta g=g_2-g_1\ge0.
\]

Let state-specific selection be `s_i=f(g_i)-kappa`, where `f` is nondecreasing and

\[
0\le f(g_2)-f(g_1)\le L\Delta g.
\]

With positive feedback-per-selection scale `B_f`,

\[
0\le G\le B_fL\Delta g.
\]

If complex return requires `G>G_osc`, then a necessary condition is

\[
\Delta g>\frac{G_{\rm osc}}{B_fL}.
\]

If an admissible architecture class has maximum contrast `Delta g_max` satisfying

\[
B_fL\Delta g_{\max}\le G_{\rm osc},
\]

that class cannot generate the requested oscillatory regime for any sensing-to-selection lift in the declared monotone-Lipschitz class.

Crossing the bound is necessary, not sufficient.

**Sources:**
- `theory/NONLINEAR_LIFT_NO_GO_V2.md`
- `adaptive_gain/nonlinear_feedback_reachability.py`
- `tests/test_nonlinear_feedback_reachability.py`
- `validation/nonlinear_lipschitz_no_go_v2.json`.

---

## S7. Ecological recurrence as spectral filtering

Let ecological states form a finite ergodic reversible Markov chain with stationary distribution `pi`. For centered state-specific selection reward, the asymptotic variance rate is

\[
\sigma_{\mathrm{eff}}^2
=
\sum_r w_r\frac{1+r_r}{1-r_r}.
\]

Here `r_r` is a nonstationary ecological eigenvalue and `w_r` is reward loading on that mode.

In the linear structural-lift special case, if `0<=g_i<=g_max`,

\[
\sigma_{\mathrm{eff}}^2
\le
\frac{(\lambda g_{\max})^2}{4}
\frac{1+r_{\max}}{1-r_{\max}}.
\]

The ceiling is extremally sharp but need not be tight in a generic multi-state system. Its slack separates reward-range saturation from alignment with the slowest ecological mode.

**Interpretation:** persistence alone is insufficient; structural selection variation must align with the persistent ecological mode.

**Sources:**
- `theory/STRUCTURAL_SPECTRAL_JOINT_BOUND.md`
- `theory/STRUCTURAL_REWARD_MODE_ALIGNMENT.md`
- associated implementations, tests and receipts.

---

## S8. Feedback-existence diagnostic and identifiability boundary

The generalized local response has

\[
T=\alpha+\phi,
\qquad
D=\alpha\phi+(1-\phi)G
\]

with `0<=alpha<=1` and `0<=phi<1`. A persistence split is model-compatible only when `0<=T<2`.

Stable monotone return can admit a zero-feedback decomposition. For a non-real conjugate eigenpair that is compatible with the declared persistence domain, every model-compatible decomposition has

\[
G>0.
\]

This diagnoses feedback existence only. It does not identify feedback magnitude, the separate persistence parameters or the causal contribution of sensing architecture.

**Sources:**
- `theory/FEEDBACK_EXISTENCE_FROM_OSCILLATION.md`
- `theory/GENERAL_RESPONSE_IDENTIFIABILITY.md`
- associated implementations, regression tests and validation receipts.

---

## S9. Proof-support and companion mathematics retained in the repository

The repository contains additional exact finite recurrences, private-pair constructions, balanced-binary fixed-scope profiles, fixed-cover kernels, certificate ladders, equality witnesses, budget-collision notes, stasis propositions and transient-observability results. These remain valuable mathematics but are not promoted to equal headline status in the Evolution Letters V3 narrative.

Their role is one of:

- proof support for a MAIN theorem;
- exhaustive finite validation of a closed form;
- a computationally smaller exact representation;
- a reusable companion result whose inclusion would split the ecological story.

The canonical disposition is recorded in `manuscript/MATHEMATICAL_ATLAS_V1.md`.

---

## S10. Integrated interpretation

The expanded theory can be summarized as

```text
natural-history alternatives + cues
-> target-relevant decision kernel
-> exact (C_A, C_F)
-> adaptive-only budget window and structural gap
-> state-dependent selection
-> finite architecture threshold / no-go region
-> temporal filtering by ecological recurrence.
```

The mathematical layers answer different biological questions and are not interchangeable. Kernelization asks which distinctions matter to the declared target. Extremal theory asks how much architecture is required. Budget gating asks when exact performance becomes selectively exposed. The nonlinear no-go theorem asks which feedback regimes remain structurally unreachable. Spectral recurrence asks how generated selection persists through time.
