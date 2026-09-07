# Open problems

The finite deterministic guaranteed-resolution layer now has a certificate hierarchy rather than one monolithic fixed-class computation:

```text
exact adaptive optimum C_A
private-pair fixed lower bound
integral pair-packing fixed lower bound
fractional pair-cover dual lower bound
exact integer fixed-budget infeasibility proof at B=C_A
exact fixed optimum C_F, only when its value is needed
```

It also separates branch-exclusive overhead into internal and external bypass channels:

\[
U-C_A=(C_F-C_A)+(C_U-C_F)+(U-C_U).
\]

The next problems begin where those certificates stop.

## 1. Compress the integer cover proof

The previous LP-integrality-gap problem is now closed for strict-gain certification: `integer_cover_proof.py` can prove directly that no fixed resolver exists with cost at most `C_A`, and its proof tree is independently verified.

The new question is **proof compression**, not existence of an exact certificate.

The branching proof can still be exponential. Useful next targets are:

- stronger cover cuts that collapse many proof-tree branches into one checkable inequality;
- symmetry reduction of equivalent cross-target pairs and equivalent queries;
- parameterized bounds in adaptive-tree union size, branch-exclusive overhead, or residual pair-cover width;
- proof minimization: given several valid infeasibility trees, find the smallest receipt that still verifies;
- a canonical proof format that can be checked without rerunning search.

The fail-closed rule remains: hitting `max_states` means `certificate_incomplete`, never `strict_gain` or `no_gain`.

## 2. Characterize fixed bypass structurally

The refined decomposition distinguishes

```text
internal union redundancy = U - C_U
external shortcut discount = C_U - C_F.
```

Both can be zero, can eliminate all adaptive gain, or can consume only part of the branch-exclusive overhead while strict gain survives.

Open questions:

- Can `C_U-C_F>0` be predicted from local separator structure around the adaptive tree rather than a global cover decision?
- What query-vocabulary operations create or destroy external shortcuts monotonically?
- Is there a useful minimal bypass set analogous to a cut or alternate path?
- How does the decomposition change with random or state-dependent query costs?

## 3. Information-valued adaptive gain

For MROD-like tasks the utility need not be binary target resolution. Define

\[
G(B)
=
\max_{\pi:\,c(\pi)\le B} I(T;H_\pi)
-
\max_{F:\,c(F)\le B} I(T;Q_F).
\]

The repository can audit information of a selected deterministic policy but does not yet provide a general optimizer or theorem characterizing `G(B)>0`.

The cost results show why branch-dependent next actions are not enough: the fixed class can have internal or external bypasses. The information-valued analogue therefore needs an optimized fixed comparator too.

Questions:

- What is the information analogue of `internal union redundancy` and `external shortcut discount`?
- Can positive routing entropy coexist with zero class-oracle information gap at every budget? (The source MROD XOR control suggests yes.)
- Can `G(B)>0` occur on several disconnected budget intervals?
- Under what assumptions is the information objective submodular or adaptively submodular?

## 4. Continuous compatible sets

PAYOFF's scientific uncertainty is continuous, whereas the current exact adaptive theorem is finite.

The next target is

\[
\Theta_t\subset\mathbb R^d,
\qquad
\Theta_{t+1}=\Theta_t\cap C(q_t,y_t),
\]

with a target map `T(theta)`. The challenge is to minimize worst-path acquisition cost without replacing the continuous compatible set by an unjustified finite panel.

A continuous counterpart of the current pair-cover view would need a certificate that every pair of parameter points with different target values is separated by selected constraints. This becomes an uncountable separation/cover problem.

## 5. Calibration actions versus target actions

All three source repositories expose the resource tradeoff

```text
measure the scientific target
vs
spend budget improving the measurement model.
```

Examples:

- MROD: calibrate `P(Q|world)` versus acquire a target-facing observation;
- PAYOFF: kernel/range calibration versus phase-discriminating payoff contrasts;
- BALANCE: improve forcing-command precision `e` versus collect more switch-bracketing queries.

A useful state must carry both target uncertainty and calibration uncertainty. A calibration action can alter the future query hypergraph itself, so the static pair-cover representation is no longer enough.

## 6. Stochastic branch-invariance

BALANCE's no-routing control is deterministic/minimax. With stochastic errors or expected loss, two branches with equal interval span may have different future distributions.

The probabilistic analogue of

\[
\sigma(s_{q,y})=\sigma'\quad\forall y
\]

likely requires equality of continuation-value kernels, not equality of raw summaries.

## 7. Randomized policies and scenario robustness

The current exact solver optimizes deterministic trees. Under multiple calibration scenarios, a randomized mixture of policies may reduce minimax regret even when it cannot lower guaranteed-resolution cost.

This is a separate objective and should not be imported into the deterministic theorem by default.

## 8. Empirical identification of routing value

A natural-data routing claim requires much more than

\[
I(T;Q_1)\approx0.
\]

The validation controls now show:

- zero direct root information is not necessary;
- zero direct information plus branch-dependent continuation is not sufficient;
- a fixed bypass can be internal or external;
- bypass can eliminate all gain or only part of it;
- fractional lower bounds can miss a real integer fixed-cost gap.

An empirical claim therefore needs evidence that:

1. the first result changes the useful continuation action/future-value state;
2. the branch-specific plan has a real resource advantage;
3. fixed bypass alternatives have been measured or bounded, not ignored;
4. the measurement/calibration relationships transport to deployment.

The source repositories currently provide synthetic/conditional witnesses, not that natural-data demonstration.

## 9. Structural prevalence beyond the tiny binary universe

The complete 4-world / 3-binary-query balanced universe has 192 strict-gain labeled tasks out of 4096. In that tiny universe the private-pair certificate catches all 192.

That completeness disappears in larger controls, where integral packing, fractional packing, and exact integer budget proofs each become necessary on different examples.

Next combinatorial questions:

- What are the symmetry classes of the 192 minimal strict-gain tasks?
- What is the smallest universe exhibiting an integral-packing gap? a fractional integrality gap? partial internal/external bypass with residual gain?
- How do results change with unequal costs, multi-outcome queries, multiple target labels, or reusable queries?
- What is the maximum possible ratio `C_F/C_A` as world and query vocabularies grow?
