# Ecological state observability

## Status

This note gives an **ecological interpretation of the already proved deterministic theory** in this repository and specifies the smallest probabilistic extension needed for a theoretical-ecology paper.

It does **not** claim that the probabilistic extension is already proved, implemented, or empirically validated.

---

## 1. Ecological question

Let

\[
\Omega
\]

be a finite set of possible ecological states or mechanisms, and let

\[
T:\Omega\to\mathcal T
\]

be the ecological distinction that the investigator actually wants to resolve.

Examples of `T` need not identify the complete state. A target may instead distinguish, for example,

```text
pollinator-mediated vs primarily abiotic
alternative interaction regimes
alternative demographic mechanisms
alternative community states relevant to a prediction
```

A declared ecological observation `q` has an acquisition cost `c(q)>0` and, in the current deterministic layer, a state-dependent outcome

\[
y=q(\omega).
\]

The central comparison is between two observation regimes.

### Fixed observability

Choose one observation bundle in advance and acquire it regardless of the outcomes.

\[
C_F=
\min\{c(F):F\text{ resolves }T\}.
\]

### Adaptive observability

Choose the next observation after seeing the outcomes already obtained.

\[
C_A=
\min\{\text{worst-path cost of a policy resolving }T\}.
\]

Thus the current core theorem can be read ecologically as

\[
\boxed{C_A\le C_F}.
\]

Strict adaptive observability gain occurs exactly when

\[
\boxed{C_A<C_F}.
\]

The ecological statement is not merely that sequential observation can save cost. It is that **the cost of resolving an ecological state depends on the allowed observation policy class, even when the observation vocabulary is held fixed**.

---

## 2. Translation of the current structural objects

The repository currently separates the fixed and adaptive sides into two different exact structures.

### Adaptive continuation structure

The cost-only continuation quotient preserves `C_A`.

Ecological reading:

> Two unresolved ecological situations are equivalent for adaptive observation when, after forgetting irrelevant labels, they have the same cost-labelled menu of future target-resolving continuations.

This is a statement about **future observational possibilities**, not about whether the current observation itself is strongly associated with the ecological target.

### Productive frontier

For each target-mixed compatible state `s`, define the observations that are nonconstant on that state,

\[
P_s=\{q:q\text{ is productive on }s\}.
\]

The inclusion-minimal family of such sets is the productive frontier

\[
\mathcal H_{\min}.
\]

A fixed observation bundle resolves the target exactly when it hits every frontier edge. Hence

\[
C_F=\tau_c(\mathcal H_{\min}).
\]

Ecological reading:

> The productive frontier is the minimal collection of simultaneous observational obligations that any precommitted monitoring design must satisfy.

The adaptive and fixed costs are therefore controlled by different summaries:

\[
\boxed{
\text{future continuation geometry}\Longrightarrow C_A,
\qquad
\text{simultaneous observation obligations}\Longrightarrow C_F.
}
\]

That separation is the main theoretical object to carry into ecology.

---

## 3. Ecological consequences already supported by the deterministic theory

### 3.1 An observation can matter by routing, not by direct target information

The source-derived witnesses already include a first routing observation with zero direct target information under the represented uniform worlds while the adaptive policy still resolves the target.

The ecological interpretation is:

\[
\boxed{
\text{value of an observation}
\neq
\text{its direct association with the target alone}.
}
\]

An observation can be valuable because it determines **which later observation becomes useful**.

This is a future-contingent or routing value.

### 3.2 Identifiability is policy-class dependent

A set of possible ecological states can be cheap to resolve adaptively and expensive to resolve with a fixed bundle.

Therefore "is the state identifiable?" is incomplete unless the permitted observation policy is declared.

A more precise question is

```text
identifiable by which observation regime,
under which budget,
and with which declared target?
```

### 3.3 Low observation arity does not remove adaptive advantage

The repository proves unbounded multiplicative adaptive advantage even when every observation is binary and every acquisition cost is one.

Thus the advantage is not an artefact of an unrealistically high-arity diagnostic measurement.

### 3.4 Marginally balanced observations do not remove adaptive advantage

The repository also gives a balanced-binary family in which every declared observation has equal or nearly equal global outcome counts while adaptive advantage remains unbounded as problem size grows.

Thus global marginal balance is not a substitute for analysing continuation structure.

### 3.5 The number of fixed obligations matters differently from their width

An upper bound on productive-frontier edge count can bound the sharp fixed/adaptive ratio, whereas an upper bound on frontier rank is extremally vacuous.

Ecological reading:

> Restricting how many observations can be jointly useful in one unresolved situation is not the same as restricting how many distinct observational obligations must be covered across all plausible situations.

The second quantity can constrain the fixed-design burden; the first alone need not.

---

## 4. A schematic ecological example

Consider a target distinguishing two or more candidate explanations for a floral phenotype. The declared observations might be

```text
q_colour      flower-colour phenotype
q_uv          UV pattern
q_visitor     visitor guild / visitation signal
q_seedset     reproductive outcome
```

The point is **not** to assert that these four observations satisfy the current deterministic assumptions in field data.

The structural possibility is instead:

```text
observe q_colour first
        |
        +-- outcome A --> q_visitor is the relevant continuation
        |
        +-- outcome B --> q_uv is the relevant continuation
        |
        +-- outcome C --> q_seedset is the relevant continuation
```

A fixed design must acquire enough observations to cover all unresolved branches simultaneously. An adaptive design only pays for the continuation realized on the observed branch.

This is the ecological meaning of branch-exclusive overhead.

The example becomes scientifically usable only after outcome uncertainty and calibration error are represented explicitly.

---

## 5. Boundary from ecological dynamics and management

This theory should not be presented as a new POMDP or adaptive-management framework.

The current state `s` is a **compatible set of ecological hypotheses/states**, and the action is an **observation acquisition**. The present objective is target resolution under observation cost.

That differs from a standard ecological management problem in which

```text
action -> changes the ecological system
state -> evolves through time
reward -> accumulates from management outcomes
```

The current deterministic theory can therefore be treated as an observation-policy layer that may later be embedded inside a dynamic or management model, but it does not replace those models.

---

## 6. Smallest probabilistic extension

For ecological use, deterministic outcomes should be replaced by observation likelihoods.

Let

\[
\omega\sim p(\omega),
\qquad
Y_q\sim P_q(\cdot\mid\omega).
\]

After observation history `h`, inference is represented by the posterior

\[
p(\omega\mid h).
\]

For a target loss `L(T,a)`, define posterior Bayes risk

\[
R(h)=\min_a\mathbb E[L(T,a)\mid h].
\]

For tolerance `\varepsilon\ge0`, define the adaptive and fixed observation costs required to reach the target risk threshold:

\[
C_A^{\varepsilon}
=
\inf_{\pi}
\{\text{policy cost}:R(H_\pi)\le\varepsilon\},
\]

with the precise pathwise/expected-cost convention declared explicitly, and

\[
C_F^{\varepsilon}
=
\inf_F
\{c(F):R(Y_F)\le\varepsilon\}.
\]

The first probabilistic theorem should be deliberately modest.

### Deterministic embedding proposition to formalize

Under

```text
deterministic observation likelihoods,
zero-one loss on the declared target,
and zero tolerated posterior risk,
```

the probabilistic definitions should reduce exactly to the present deterministic costs:

\[
\boxed{
C_A^{0}=C_A,
\qquad
C_F^{0}=C_F.
}
\]

This provides a clean mathematical bridge rather than replacing the deterministic theory with an unrelated stochastic framework.

---

## 7. Conditional observation value

A useful local quantity for the stochastic layer is the expected risk reduction of observation `q` after history `h`:

\[
\Delta(q\mid h)
=
R(h)-
\mathbb E_{Y_q\mid h}[R(h,q,Y_q)].
\]

This quantity is **history dependent**.

Two observations with the same unconditional information about the target can have different values after different histories because their future continuation roles differ.

A possible thresholded analogue of a productive set is

\[
P_h^{\delta}
=
\{q:\Delta(q\mid h)\ge\delta\}.
\]

This is only a candidate object. It is not yet claimed to inherit the deterministic hitting-set theorem.

The research question is precisely whether a useful probabilistic analogue of the productive frontier exists, and under what assumptions.

---

## 8. Theoretical-ecology paper claim

The paper should **not** be sold as "a new general theory of adaptive experimental design".

A defensible ecological claim is narrower and more interesting:

> Ecological state resolution has two distinct structural burdens: a continuation burden governing outcome-contingent observation and a simultaneous-coverage burden governing fixed observation. These burdens can diverge arbitrarily even under simple binary observations. Consequently, the observational value of a measurement can lie primarily in how it changes which future measurements matter.

The stochastic layer then asks when this exact structural distinction survives noisy ecological observation.

---

## 9. What would make this an ecology paper rather than a mathematical paper with ecological nouns

A theoretical-ecology manuscript should contain all four layers below.

1. **Ecological state problem.** Define a biologically meaningful target distinction and explain why observing the complete state is neither possible nor necessary.
2. **Exact deterministic theory.** Present the continuation/frontier split, strict-gain theorem, and the strongest bounded-observation consequences without reproducing the entire repository catalogue.
3. **Noisy embedding.** Prove at least the deterministic zero-risk embedding and one nontrivial stochastic result or counterexample.
4. **Ecological consequence.** Show a calibrated or literature-grounded ecological observation vocabulary in which outcome-contingent routing changes the useful continuation, while clearly separating illustration from empirical validation.

The repository's larger finite-profile receipts can remain validation/supporting material rather than becoming the conceptual center of the ecology paper.
