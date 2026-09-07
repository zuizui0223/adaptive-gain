# Open problems

The repository now closes the exact finite **guaranteed-resolution cost** problem far enough to separate three quantities:

```text
branch-exclusive overhead
=
realized adaptive gain
+
fixed bypass discount.
```

The cross-repository comparison still leaves several nontrivial next questions.

## 1. Information-valued adaptive gain

For MROD-like tasks the utility need not be binary target resolution. Define

\[
G(B)
=
\max_{\pi:\,c(\pi)\le B} I(T;H_\pi)
-
\max_{F:\,c(F)\le B} I(T;Q_F).
\]

The current repository can audit information of a selected deterministic policy, but it does not yet provide a general optimizer or a theorem characterizing when \(G(B)>0\).

The cost validation shows that **branch-dependent next actions are not sufficient**: a fixed design can sometimes bypass the routing query. The information-valued analogue therefore needs to compare against the fully optimized fixed class, not merely against the union of branch-specific actions.

Questions:

- What is the information-theoretic analogue of `fixed bypass discount`?
- Can a branch-dependent policy have positive routing entropy but zero class-oracle information gain at every budget?
- Can \(G(B)>0\) occur on multiple disconnected budget intervals?
- Under what assumptions is \(G(B)\) unimodal, submodular, or adaptively submodular?

## 2. Continuous compatible sets

PAYOFF's scientific parameter uncertainty is continuous, whereas the exact adaptive theorem here is finite.

The next target is a compatible set

\[
\Theta_t\subset\mathbb R^d
\]

updated by observations:

\[
\Theta_{t+1}
=
\Theta_t\cap C(q_t,y_t).
\]

The problem is to minimize worst-path acquisition cost for identifying a target map \(T(\theta)\) without replacing the continuous set by an unjustified finite panel.

The finite union-flattening theorem suggests a possible route: characterize whether the union of all query constraints used by a continuous adaptive tree is itself a valid fixed certificate, and then define a continuous analogue of the bypass discount.

## 3. Calibration actions versus target actions

All three source lines now expose a common resource-allocation problem:

```text
measure the scientific target
vs
spend budget improving the measurement model itself.
```

Examples:

- MROD: calibrate `P(Q|world)` versus acquire the target-facing observation;
- PAYOFF: distinguish kernel/range calibration versus phase-discriminating payoff contrasts;
- BALANCE: improve forcing-command precision `e` versus collect more switch-bracketing queries.

A useful theory needs a state that carries both scientific uncertainty and calibration uncertainty. A calibration action can also create a fixed-design bypass, so its effect cannot be scored only by branch specialization.

## 4. Stochastic branch-invariance

BALANCE's no-routing control is deterministic/minimax. Under stochastic errors or expected loss, two branches with equal interval span can have different future distributions.

Question:

What is the correct probabilistic analogue of the sufficient-state condition

\[
\sigma(s_{q,y})=\sigma'
\quad\forall y?
\]

A likely formulation uses equality of continuation-value kernels rather than equality of raw state summaries.

## 5. Randomized policies

The current exact solver optimizes deterministic trees.

For minimax regret under multiple scenarios, a randomized mixture of adaptive policies may reduce worst-case regret even when it cannot lower guaranteed-resolution cost.

This should be treated as a separate objective, not silently added to the deterministic theorem.

## 6. Empirical identification of routing value

A natural-data claim of routing value requires more than showing

\[
I(T;Q_1)\approx0.
\]

The new five-world control proves that zero direct root information is not even necessary for strict deterministic cost gain, while the bypass control proves that zero direct information plus branch-dependent continuation is not sufficient.

An empirical claim therefore needs to establish all of the following in the deployment context:

1. the first result changes the useful continuation action or future-value state;
2. the branch-specific plan has a resource advantage;
3. no equally cheap fixed bypass measurement set resolves the same target;
4. the measurement/calibration relationships transport to deployment.

The source repositories currently provide synthetic/conditional witnesses, not that empirical demonstration.

## 7. Structural prevalence beyond the tiny binary universe

The exhaustive validator classifies the complete 4-world / 3-binary-query labeled universe for fixed binary target assignments. The balanced 2+2 target has 192 strict-gain tasks out of 4096; the 3+1 target has none.

Those counts are not empirical prevalence estimates. The next mathematical questions are:

- what are the symmetry classes of the 192 strict-gain tasks?
- can they be characterized without enumeration?
- how do counts change with multi-outcome queries, unequal costs, more target labels, or repeated queries?
- what is the maximum possible ratio `C_fixed/C_adapt` as world and query vocabularies grow?

The union-cost theorem suggests that large gains require many costly queries that live on mutually exclusive branches and cannot be replaced by a smaller fixed bypass bundle.
