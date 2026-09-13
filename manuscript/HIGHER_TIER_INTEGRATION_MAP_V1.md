# Higher-tier manuscript integration map v1

Purpose: integrate the nonlinear no-go theorem into the current manuscript **without** proliferating headline results or destroying the frozen Theoretical Ecology fallback.

The current `MANUSCRIPT_V1.md` remains the fallback surface until this promotion lane is accepted and rebuilt as a distinct higher-tier manuscript version.

---

## 1. Title

### Preferred Evolution Letters title

**Finite sensing architecture excludes eco-evolutionary feedback regimes**

Reason: puts the no-go result before the machinery and makes the biological consequence explicit.

### Conservative alternative

**Finite sensing structure constrains eco-evolutionary feedback regimes**

Use if outside readers judge `excludes` too absolute without immediately seeing the model-class qualifier.

---

## 2. Abstract

Replace the four-result catalogue with `ABSTRACT_EVOLUTION_LETTERS_V1.md`.

Required hierarchy:

1. biological question;
2. finite adaptive/fixed structural gap;
3. reverse reachability/no-go theorem;
4. nonlinear robustness;
5. ecological recurrence as temporal filtering;
6. scope qualifier `within the declared model class`.

Do not advertise the stasis proposition as a coequal headline result.

---

## 3. Introduction

Retain the existing prior-art firewall on:

- rapid evolution/stasis;
- fitness value of information;
- rate-distortion/minimum mutual information;
- separating systems/decision trees;
- generic eco-evolutionary feedback.

Change the final setup from

```text
finite sensing structure -> possible feedback
```

to the stronger reverse question:

```text
requested feedback regime
-> required structural gap
-> required finite sensing architecture
```

End the Introduction with one sentence only:

> We show that finite sensing architecture can rule out entire local eco-evolutionary regimes, and that this prohibition survives a broad nonlinear class of sensing-to-selection maps.

---

## 4. Model §2.3 — sensing-to-selection bridge

### Keep the linear model, but demote it to a microfounded special case

Current text:

```text
s_i = lambda g_i - kappa
```

New order:

1. Define the additive cue-acquisition-cost microfoundation: if each guaranteed cue acquisition costs `c` on the declared selection scale and correct target resolution has the same terminal payoff, then the worst-case adaptive-vs-fixed structural advantage is `c(C_F-C_A)`.
2. State `s(g)=c g-kappa` as the minimal additive baseline.
3. Immediately generalize to

```text
s(g)=f(g)-kappa
```

with `f` nondecreasing and

```text
0 <= f(g2)-f(g1) <= L(g2-g1).
```

4. Say explicitly that the principal no-go theorem needs only the upper marginal bound `L`; it does not need exact linearity or differentiability.

Do not call `g` fitness.

---

## 5. Model §2.5 — local feedback

Keep the existing factorization

```text
G = - beta Delta_s e
```

and define

```text
B = -beta e > 0.
```

For the nonlinear class,

```text
0 <= G <= B L Delta_g.
```

Then present the linear equality

```text
G = a Delta_g,  a = B lambda
```

as the exact additive special case used for constructive reachability examples.

This order matters. The inequality is the robust biological theorem surface; the equality is the sharp constructive submodel.

---

## 6. Results §3.1 — principal theorem

Start with the biological no-go orientation, before binary formulas.

### Theorem 1A — nonlinear necessary architecture bound

If oscillation requires

```text
G > G_osc
```

and the sensing-to-selection lift is nondecreasing with marginal effect at most `L`, then

```text
Delta_g > G_osc/(B L)
```

is necessary, hence

```text
q_required = floor(G_osc/(B L)) + 1.
```

### Corollary — impossible regime under insufficient architecture

If a declared architecture family has

```text
Delta_g <= q_max
```

and

```text
B L q_max <= G_osc,
```

then the oscillatory regime is impossible for every lift in the declared nonlinear class.

Use the sentence:

> **Architecture below the structural threshold does not merely make oscillation unlikely; it makes that local regime unreachable in the declared model class.**

### Theorem 1B — exact finite architecture translation

Only then translate `q_required` into:

- exact binary first corner;
- bounded-arity Pareto frontier `P_b(q)`.

This keeps the combinatorics subordinate to the biological prohibition.

### Constructive special case

For `alpha=1`, `phi=1/2`, `B=1/2`, `L=1/4`, the necessary gap is 2. Existing binary extremal results rule out:

- <=5 worlds;
- <=4 queries;
- <=4 productive-frontier obligations.

The six-world/five-query/five-obligation witness proves actual reachability only for the linear special case that attains the allowed marginal gain.

Do not imply generic nonlinear sufficiency.

---

## 7. Results §3.2–3.4

### §3.2 structural-temporal envelope

Retain, but frame as the answer to a second question:

> once a structural reward is possible, which part survives ecological recurrence?

The key ecological line is:

> Slow community modes matter only when the structurally generated reward vector loads onto them.

### §3.3 feedback diagnostic

Retain as a diagnostic theorem, not a second flagship.

### §3.4 stasis

Compress sharply. Keep cancellation versus restoration because it prevents mechanistic conflation, but move most algebra to Supplement if needed for the 5,000-word Evolution Letters route.

---

## 8. Discussion

The first subsection should now be titled:

**Some evolutionary dynamics require a minimum sensing architecture**

Lead with the no-go result rather than the reverse-map formalism.

Second subsection:

**Ecological recurrence filters, rather than creates, structural reward**

This is where the Markov spectral result becomes ecologically indispensable rather than decorative.

Third subsection:

**What the theorem does not identify**

Include:

- empirical `B` and `L` are not estimated here;
- above-threshold architecture is not sufficient under a generic nonlinear lift;
- deterministic guaranteed sensing is narrower than noisy Bayesian sensing;
- local feedback theory is not a global bifurcation theorem.

End with the conceptual statement:

> Evolutionary reachability can be limited before genetics or demography enter the model: some feedback regimes are unavailable because the organism's declared sensing architecture cannot generate enough state-contingent structural contrast.

---

## 9. Figure hierarchy

### Figure 1 — biological architecture and no-go logic

```text
finite ecological alternatives
-> cue architecture
-> adaptive/fixed structural gap
-> bounded selection contrast
-> bounded feedback gain
-> reachable / unreachable local regime
```

Show a blocked arrow when `B L q_max <= G_osc`.

### Figure 2 — exact/Pareto architecture requirement

Keep the current binary exact corner and bounded-arity Pareto example.

### Figure 3 — ecological recurrence filter

Keep the two slack factors, with emphasis on reward--slow-mode alignment.

### Figure 4

Move to Supplement for Evolution Letters unless the final word/display budget permits it. For Am Nat it can remain main text.

---

## 10. Promotion stop rule

Do not add a noisy-sensing theorem, continuous-world theorem, mutation/drift layer, or global bifurcation theory merely to improve journal positioning.

The promotion question is now narrow:

> Does the nonlinear no-go theorem plus the exact architecture translation make the existing paper a broad evolutionary-theory result?

If yes, submit upward. If no, retain the existing Theoretical Ecology package or use the Am Nat route; do not theorem-hunt.
