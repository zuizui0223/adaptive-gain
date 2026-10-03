# Exact noisy temporal routing factorization

## Status

This note closes the symmetric binary-noise extension staged in `NEXT_NOISY_ROUTING_MODEL.md`.

It remains a deliberately minimal theorem. It does not claim a general result for arbitrary cue likelihoods, arbitrary Markov environments, or arbitrary fitness functions. The point is to identify an exact bridge from the deterministic four-world adaptive-gain core to noisy ecological sensing.

---

## 1. State and temporal structure

As in `TEMPORAL_ROUTING_THRESHOLD.md`, let

\[
(T,C_t)\in\{0,1\}^2,
\]

where `T` is the fitness-relevant target and `C_t` determines which specialist cue is diagnostic.

During one two-step sensing episode,

\[
T_1=T_0=T,
\]

while

\[
P(C_1=C_0)=\rho.
\]

Define signed temporal predictability

\[
\phi=2\rho-1.
\]

---

## 2. Symmetric noisy cues

### Routing cue

At time zero the organism observes a noisy route signal `R` with

\[
P(R=C_0)=a,
\qquad
1/2\le a\le1.
\]

Define its chance-centred signal strength

\[
\eta_R=2a-1.
\]

### Specialist cues

The deterministic specialist outputs remain

\[
q_L(T,C)=
\begin{cases}
T,&C=1,\\
0,&C=0,
\end{cases}
\]

and

\[
q_R(T,C)=
\begin{cases}
T,&C=0,\\
1,&C=1.
\end{cases}
\]

but each observed specialist bit passes independently through a binary symmetric channel with reliability

\[
P(Y_q=q(T,C_1))=b,
\qquad
1/2\le b\le1.
\]

Define

\[
\eta_S=2b-1.
\]

Restricting reliabilities to at least chance is without loss for this labelled binary channel: a consistently below-chance bit can be relabelled.

---

## 3. Exact fixed baseline

At budget two, the three fixed pairs are

```text
{route,left}
{route,right}
{left,right}.
```

Direct Bayes decoding of all latent histories gives the same target accuracy for every pair:

\[
\boxed{
A_F^{(2)}
=
\frac12+\frac{2b-1}{4}
=
\frac12+\frac{\eta_S}{4}.
}
\]

Remarkably, the fixed optimum is independent of both `rho` and `a` in this minimal symmetric construction.

The route cue can therefore improve contingent sensing without improving the best fixed two-cue baseline.

---

## 4. Exact contingent policies

After observing the noisy route bit `R`, consider two policies.

### Persistence-following

```text
R=0 -> right specialist
R=1 -> left specialist
```

Its accuracy is

\[
\boxed{
A_{same}^{(2)}
=
A_F^{(2)}
+
\frac{(2\rho-1)(2a-1)(2b-1)}{4}.
}
\]

### Alternation-following

```text
R=0 -> left specialist
R=1 -> right specialist
```

Its accuracy is

\[
\boxed{
A_{flip}^{(2)}
=
A_F^{(2)}
-
\frac{(2\rho-1)(2a-1)(2b-1)}{4}.
}
\]

Thus the sign of temporal predictability selects the continuation rule, while cue reliabilities scale its value.

---

## 5. Factorization theorem

The optimal contingent accuracy is

\[
\boxed{
A_A^{(2)}
=
A_F^{(2)}
+
\frac{|2\rho-1|(2a-1)(2b-1)}{4}.
}
\]

Therefore

\[
\boxed{
G_{noisy}
=
A_A^{(2)}-A_F^{(2)}
=
\frac{|\phi|\eta_R\eta_S}{4}.
}
\]

This is an exact factorization in the symmetric binary-noise model, not a local approximation.

### Collapse set

\[
\boxed{
G_{noisy}=0
\iff
\rho=1/2
\quad\text{or}\quad
a=1/2
\quad\text{or}\quad
b=1/2.
}
\]

Thus contingent cue routing requires all three ingredients:

```text
temporal predictability
x usable routing information
x usable downstream specialist information.
```

---

## 6. Evolutionary threshold with control cost

Let one unit of target accuracy be worth `v>0` fitness units and let contingent control impose an extra cost `k>=0` relative to a fixed two-cue policy.

Then

\[
\boxed{
\Delta W
=
\frac{v}{4}|\phi|\eta_R\eta_S-k.
}
\]

Contingent routing is favoured exactly when

\[
\boxed{
|\phi|\eta_R\eta_S>\frac{4k}{v}.
}
\]

This is a three-way gate: improving one component cannot rescue routing if another component is at chance.

---

## 7. Complementarity and possible coevolution

For `a,b>1/2` and `rho!=1/2`,

\[
G_{noisy}
=
\frac{|2\rho-1|}{4}(2a-1)(2b-1).
\]

Hence

\[
\frac{\partial G}{\partial a}
=
\frac{|2\rho-1|}{2}(2b-1),
\]

and

\[
\frac{\partial G}{\partial b}
=
\frac{|2\rho-1|}{2}(2a-1).
\]

The cross-partial is

\[
\boxed{
\frac{\partial^2G}{\partial a\,\partial b}
=|2\rho-1|>0.
}
\]

So the routing and specialist channels are complementary in this minimal model:

- better specialist sensing strengthens selection for accurate routing;
- better routing strengthens the value of accurate specialist sensing;
- temporal unpredictability removes that complementarity.

This creates a concrete evolutionary hypothesis: **temporal structure can gate the coevolution of early context sensing and later specialist sensing.**

The theorem alone does not prove population-genetic coevolution; it identifies the within-episode fitness curvature that could generate it once heritable investments and trade-offs are specified.

---

## 8. Natural-history predictions

The factorization suggests several empirical signatures.

### H1. Early cues can be weak target predictors yet strongly conserved

An early cue may be maintained because it predicts which later cue is worth sampling, not because it directly predicts the final target.

### H2. Sensory precision should depend on downstream opportunity

Selection on an early routing cue should weaken where the downstream specialist cue is unreliable, unavailable, or too costly.

### H3. Temporal decorrelation should flatten sensory hierarchy

Where the ecological context determining specialist usefulness becomes temporally unpredictable between early and late sensing, contingent cue order should lose value.

### H4. Predictable alternation can reverse the hierarchy

Negative temporal autocorrelation can favour deliberately selecting the specialist associated with the opposite current context.

### H5. Natural history determines whether the theorem is applicable

The organism must actually encounter an early cue before mutually substitutable later cues become available. Approach, contact, movement, handling, and habitat geometry define this feasible cue graph.

---

## 9. Deterministic and noisy limits

### Perfect cues

Setting

\[
a=b=1
\]

recovers

\[
G=|2\rho-1|/4,
\]

the exact temporal theorem.

### Static environment and perfect cues

Setting

\[
\rho=a=b=1
\]

gives

\[
A_F^{(2)}=3/4,
\qquad
A_A^{(2)}=1,
\]

the expected-risk shadow of the deterministic exact-resolution result

\[
C_A=2<C_F=3.
\]

### Chance routing cue

At `a=1/2`, the early cue contains no usable information about which branch will be diagnostic and contingent gain vanishes even if the environment is predictable.

### Chance specialist cue

At `b=1/2`, there is no useful downstream information to route toward, so routing value also vanishes.

---

## 10. Claim boundary

This theorem relies on

```text
binary target
binary context
uniform initial target/context prior
one context transition
symmetric binary routing noise
symmetric binary specialist noise
independent observation noise conditional on latent state
two-query budget
minimal four-world specialist semantics
Bayes-optimal target decoding.
```

It does not establish the same product formula under asymmetric likelihoods, correlated observation errors, multiple time steps, changing targets, more than two specialist channels, or nonlinear long-run fitness.

Those are the next generalization problems.

---

## 11. Implementation

Implementation:

```text
adaptive_gain/noisy_temporal_routing.py
```

Regression:

```text
tests/test_noisy_temporal_routing.py
```

The implementation computes both exact state-enumerated Bayes accuracies and the closed-form factorization, so the theorem is checked against the generative model rather than only against its algebraic expression.
