# Evolution Letters figure plan v3 — mathematical integration

Status: design only; do not replace the validated V2 figure files until the V3 manuscript passes CI and length gates.

## Design constraint

Keep exactly three main display items. V3 broadens the mathematical backbone but must not look like a theorem catalogue. Each figure therefore integrates several results around one biological question.

## Figure 1. From finite decision cost to ecological selection and dynamical exclusion

**Question:** How does one finite sensing task become an eco-evolutionary constraint?

Panel A — exact finite task geometry:

```text
adaptive cost C_A <= fixed cost C_F
```

showing the hard ecological budget axis with three regions:

```text
B < C_A             C_A <= B < C_F              B >= C_F
both fail           adaptive only succeeds       both succeed
```

Panel B — threshold evolutionary lift:

show `s_B=-kappa` outside the adaptive-only window and

```text
s_B = log[(w0+v)/w0] - kappa
```

inside it. Label this as conditional on a biologically justified hard deadline/resource ceiling.

Panel C — state contrast and nonlinear no-go:

```text
g_i = C_F(i)-C_A(i)
Delta g = g_2-g_1
G <= B_f L Delta g
```

and the unreachable region

```text
B_f L Delta g_max <= G_osc.
```

Use `B_f` for feedback-per-selection scale in V3 to avoid collision with ecological budget `B`.

**Message:** The same exact finite geometry can affect evolution through a hard performance threshold or through bounded state-dependent selection contrast; insufficient structure yields a genuine no-go region.

## Figure 2. What structural complexity actually controls adaptive gain?

**Question:** Which features of sensing architecture matter, and which intuitive summaries do not?

Panel A — sharp binary requirement:

```text
required gap q
-> h_2*(q)
-> (n*,m*,E*)
```

with the canonical `q=2 -> (6,5,5)` example.

Panel B — bounded-arity Pareto tradeoff:

show `q=3,b=4` with nondominated points

```text
(7,6,6) and (8,5,5).
```

Panel C — balanced-query counterexample:

show a routing tree with globally 50/50 balanced binary queries but branch-specific terminal resources, annotated with

```text
C_F / C_A >= 2^d/(d+1) -> infinity.
```

**Message:** More cue outcomes change tradeoffs, but global marginal cue balance does not bound adaptive value. Branch/resource geometry is the controlling object.

## Figure 3. Ecology filters structurally generated selection through time

Retain the V2 recurrence figure concept with minimal notation change.

Panel A — recurrent ecological states each carry a state-specific finite decision problem and reward/selection contribution.

Panel B — two systems with the same slow ecological mode but different reward-mode alignment.

Panel C — reversible-chain spectral formula

```text
sigma_eff^2 = sum_r w_r (1+r_r)/(1-r_r)
```

with the message that persistence alone is insufficient.

## Supplementary visual, only if necessary

A single Supplement schematic may show the exact target-relevant reduction ladder:

```text
raw worlds/cues
-> identity-indexed target-pair incidence
-> world-twin quotient + nondominated query frontier
-> exact Bellman kernel.
```

Do not promote the solver/certificate machinery to another main figure.

## Claim firewalls

- Figure 1 must label the budget-gated fitness map as conditional, not universal.
- Figure 1 must say crossing the no-go threshold is `not ruled out`, not `guaranteed`.
- Figure 2 must label the balanced construction as an unbounded family/existence result, not a fixed-scope sharp maximum.
- Figure 2 must not imply that `(n,m,E)` is one scalar complexity score.
- Figure 3 must separate slow-mode persistence from reward-mode alignment.
