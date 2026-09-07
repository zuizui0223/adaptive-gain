# Open problems

The first version closes the exact finite **guaranteed-resolution** problem. The cross-repository comparison leaves several nontrivial next questions.

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

Questions:

- Is branch-dependent next-action identity plus a utility separation condition sufficient?
- Can \(G(B)>0\) occur on multiple disconnected budget intervals?
- Under what assumptions is \(G(B)\) unimodal or submodular?

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

A useful theory needs a state that carries both scientific uncertainty and calibration uncertainty.

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

One must establish that the first result changes which subsequent measurement is informative or cost-effective, and that this interaction transports to the deployment context.

The source repositories currently provide synthetic/conditional witnesses, not that empirical demonstration.
