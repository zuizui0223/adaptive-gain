# Temporal routing theorem from the minimal four-world core

## Status

This note closes a first dynamic extension of the deterministic `adaptive-gain` normal form.

It is deliberately small. The result is not yet a general theory of learning, cue integration, or stochastic environments. Its purpose is to identify the first exact evolutionary-ecology consequence of the fixed-versus-contingent distinction already proved in the repository.

The main result is that the value of contingent sensing is controlled by **temporal predictability**, not by persistence alone.

---

## 1. Start from the exact deterministic normal form

Write each represented ecological state as a pair

\[
(T,C)\in\{0,1\}\times\{0,1\},
\]

where

- `T` is the fitness-relevant target;
- `C` is a context that determines which specialist cue is diagnostic.

Under the world ordering

```text
w0=(T=0,C=0)
w1=(T=0,C=1)
w2=(T=1,C=1)
w3=(T=1,C=0)
```

the three queries of the unique four-world strict-gain normal form are exactly

```text
q_route = C

q_left(T,C) = T  if C=1
                0  if C=0

q_right(T,C)= T  if C=0
                1  if C=1
```

which reproduces

```text
q_left  = (0,0,1,0)
q_route = (0,1,1,0)
q_right = (0,1,1,1).
```

In the static deterministic model,

\[
C_A=2,\qquad C_F=3.
\]

The router is marginally target-uninformative under the uniform four-world prior:

\[
\boxed{I(T;q_{route})=0.}
\]

Its role is to determine which continuation is useful.

---

## 2. Add one ecological time step

Hold the target fixed during one short sensing episode:

\[
T_1=T_0=T.
\]

Let the context change between routing and specialist sensing:

\[
P(C_1=C_0)=\rho,
\qquad
P(C_1\ne C_0)=1-\rho,
\]

with `T` and `C_0` independent fair bits.

The signed lag-one predictability of the binary context is

\[
\phi=2\rho-1.
\]

Thus

```text
rho = 1     -> perfect persistence
rho = 1/2   -> temporal independence
rho = 0     -> perfect alternation
```

The observation schedule is

```text
time 0: q_route observes C0
time 1: terminal query is acquired under C1
```

The inference target remains `T`.

---

## 3. Fixed two-query policies have a constant ceiling

At budget two, the only distinct fixed bundles in the three-query core are

```text
{q_route, q_left}
{q_route, q_right}
{q_left, q_right}.
```

For every

\[
\rho\in[0,1],
\]

Bayes-optimal target classification from each pair has accuracy

\[
\boxed{A_F^{(2)}(\rho)=\frac34.}
\]

The ceiling does not depend on temporal context predictability.

Intuitively, a fixed pair cannot condition terminal-cue identity on the route outcome. One quarter of target mass remains effectively lost after optimal decoding, regardless of whether context tends to persist or alternate.

The implementation enumerates all `T,C0,C1` histories and performs exact Bayes decoding from each fixed observation tuple.

---

## 4. Two contingent routing rules

After observing `C0`, an adaptive policy may use either of two natural rules.

### Persistence-following rule

```text
C0=0 -> q_right
C0=1 -> q_left
```

This is the original deterministic routing tree. Its Bayes accuracy is

\[
\boxed{A_{same}(\rho)=\frac{1+\rho}{2}.}
\]

### Alternation-following rule

```text
C0=0 -> q_left
C0=1 -> q_right
```

This deliberately routes to the opposite branch. Its Bayes accuracy is

\[
\boxed{A_{flip}(\rho)=1-\frac{\rho}{2}.}
\]

Therefore the optimal two-query contingent policy is

\[
\boxed{
A_A^{(2)}(\rho)
=
\max\left\{\frac{1+\rho}{2},1-\frac{\rho}{2}\right\}
=
\frac34+\frac{|2\rho-1|}{4}.
}
\]

---

## 5. Temporal routing theorem

Combining the fixed and adaptive formulas gives

\[
\boxed{
G_{time}(\rho)
=
A_A^{(2)}(\rho)-A_F^{(2)}(\rho)
=
\frac{|2\rho-1|}{4}
=
\frac{|\phi|}{4}.
}
\]

Hence

\[
\boxed{
G_{time}(\rho)>0
\iff
\rho\ne\frac12.
}
\]

The optimal qualitative policy is

\[
\boxed{
\rho>\frac12 \Rightarrow \text{follow persistence},
}
\]

\[
\boxed{
\rho<\frac12 \Rightarrow \text{follow alternation},
}
\]

with exact indifference at temporal independence.

### Interpretation

The evolutionary resource is not environmental slowness by itself.

It is

\[
\boxed{\text{predictability of future cue usefulness from present context}.}
\]

Positive autocorrelation and negative autocorrelation can both support contingent sensing. What destroys routing value is not rapid change per se, but loss of predictive dependence.

This corrects the weaker preliminary hypothesis that only persistent environments should favour deep routing.

---

## 6. Deterministic and temporally independent limits

### Static deterministic limit

At

\[
\rho=1,
\]

the persistence-following adaptive policy reaches

\[
A_A^{(2)}=1,
\]

whereas every fixed two-query bundle remains at

\[
A_F^{(2)}=3/4.
\]

This is the expected-risk shadow of the exact deterministic statement

\[
C_A=2<C_F=3.
\]

### Perfect alternation

At

\[
\rho=0,
\]

the alternation-following policy also reaches accuracy one.

Thus the deterministic routing pattern has a second dynamic analogue: a perfectly predictable reversal can be exploited by reversing the continuation rule.

### Temporal independence

At

\[
\rho=1/2,
\]

`C0` contains no information about which terminal query will be diagnostic at time 1. Then

\[
A_A^{(2)}=A_F^{(2)}=3/4.
\]

This is the first exact collapse point of adaptive routing value in a changing environment.

---

## 7. Add an evolutionary maintenance cost

Let one unit of classification accuracy be worth `s>0` fitness units, and let maintaining or using contingent routing carry an extra cost

\[
k\ge0
\]

relative to a fixed two-query policy. This cost can represent neural control, memory, switching, developmental machinery, attention, or opportunity cost not already included in the two acquisitions themselves.

Then the invasion or selection advantage of contingent routing in this minimal model is

\[
\boxed{
\Delta W
=
\frac{s}{4}|2\rho-1|-k.
}
\]

Routing is favoured exactly when

\[
\boxed{
|2\rho-1|>\frac{4k}{s}.
}
\]

Thus a nonzero control cost converts the zero-at-independence result into a genuine predictability threshold.

---

## 8. Relative timescales

For a positively autocorrelated environment, suppose the signed context correlation after a sensing delay `Delta` is approximately

\[
\phi(\Delta)=e^{-\Delta/\tau_{env}}.
\]

Then

\[
G_{time}(\Delta)
=
\frac14 e^{-\Delta/\tau_{env}},
\]

and with routing-control cost `k`,

\[
\Delta W
=
\frac{s}{4}e^{-\Delta/\tau_{env}}-k.
\]

If `s>4k`, routing is favoured when

\[
\boxed{
\tau_{env}
>
\frac{\Delta}{\log(s/4k)}.
}
\]

This gives the desired timescale comparison without claiming that persistence is the only form of predictability.

For oscillatory or negatively autocorrelated environments, the relevant extension is the magnitude and sign of `phi(Delta)`, with the continuation rule tracking the sign.

---

## 9. Evolutionary-ecology predictions

The theorem yields several testable predictions.

### P1. Cue-routing value should track temporal predictability, not marginal cue-target association

The route cue is exactly independent of `T`, yet it has positive value whenever it predicts future cue usefulness.

Empirical studies that rank cues only by direct correlation with fitness-relevant state can therefore miss routing value.

### P2. Positive and negative environmental autocorrelation predict different cue orders

Persistent contexts favour same-branch continuation; predictably alternating contexts favour reversed continuation.

### P3. Cognitive or switching costs create a sharp selection boundary

Contingent sensing should disappear when temporal predictability falls below the cost-dependent threshold `4k/s`.

### P4. Longer acquisition delays weaken routing in positively autocorrelated environments

The relevant ratio is between cue-acquisition delay and the decorrelation timescale of the context that determines future cue usefulness.

### P5. Natural history determines the feasible routing graph

The theorem assumes one early context cue and two later specialist cues. Which such orderings are physically possible is a natural-history property, not an arbitrary modelling choice.

---

## 10. Natural-history interpretation

Many organisms encounter cues in an ordered sequence rather than as a simultaneous vector.

Examples include

```text
host finding:
    long-range habitat/plant cue
    -> approach
    -> contact chemistry / nutrition / predator cue

mate assessment:
    long-range signal
    -> approach
    -> close-range visual / acoustic / chemical cue

foraging:
    patch-class cue
    -> entry
    -> local prey or reward assessment

pollination:
    floral detection
    -> approach
    -> landing / handling
    -> reward assessment / memory update
```

The current theorem does not claim that any one published natural-history system already implements the exact three-query normal form. It supplies a diagnostic question:

> Does an early cue mainly predict the final target, or does it predict which later cue will be informative?

The second case is the empirical signature of a routing cue.

---

## 11. Relation to existing evolutionary ecology

The result must be positioned inside, not outside, established information-use theory.

Relevant starting points include:

- Dall, S. R. X., Giraldeau, L.-A., Olsson, O., McNamara, J. M. & Stephens, D. W. (2005). *Information and its use by animals in evolutionary ecology*. Trends in Ecology & Evolution. DOI: 10.1016/j.tree.2005.01.010.
- Eliassen, S., Jørgensen, C., Mangel, M. & Giske, J. (2009). *Quantifying the adaptive value of learning in foraging behavior*. The American Naturalist. DOI: 10.1086/605370.
- Schneeberger, K. & Taborsky, M. (2020). *The role of sensory ecology and cognition in social decisions: Costs of acquiring information matter*. Functional Ecology. DOI: 10.1111/1365-2435.13488.
- Bergman, T. J. & Beehner, J. C. (2023). *Information Ecology: an integrative framework for studying animal behavior*. Trends in Ecology & Evolution. DOI: 10.1016/j.tree.2023.05.017.
- Lund, M., Brainard, D. C. & Szendrei, Z. (2019). *Cue hierarchy for host plant selection in Pieris rapae*. Entomologia Experimentalis et Applicata. DOI: 10.1111/eea.12772.

Those literatures already establish that information has fitness value, acquisition costs, temporal structure, cue hierarchies, and context dependence.

The narrower contribution here is

\[
\boxed{
\text{an exact fixed-versus-contingent routing gain generated by temporal predictability.}
}
\]

---

## 12. Implementation and regression

Implementation:

```text
adaptive_gain/temporal_routing.py
```

Regression:

```text
tests/test_temporal_routing.py
```

The test suite checks by direct state enumeration that

```text
all fixed pairs = 3/4
persistence policy = (1+rho)/2
alternation policy = 1-rho/2
optimal adaptive = 3/4 + |2rho-1|/4
gain = |2rho-1|/4
strict gain iff rho != 1/2
```

The new module was independently exercised on the development branch with 18 focused tests passing before commit.
