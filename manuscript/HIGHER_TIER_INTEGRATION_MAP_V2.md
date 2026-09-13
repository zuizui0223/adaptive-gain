# Higher-tier manuscript integration map v2

Purpose: make `MANUSCRIPT_EVOLUTION_LETTERS_V2.md` the canonical higher-tier surface while preserving the frozen Theoretical Ecology fallback.

## Core notation

Use exactly:

```text
g_i = C_F(i) - C_A(i) >= 0       state-specific sensing gap
Delta g = g_2 - g_1 >= 0          ordered between-state contrast
s_i = f(g_i) - kappa              state-specific selection contribution
Delta s <= L Delta g              nonlinear marginal ceiling
G <= B L Delta g                  feedback ceiling
```

Never use `Delta g=C_F-C_A` in the higher-tier manuscript.

## Introduction

Lead with the reverse biological question:

> Which state-specific sensing architectures must exist before an eco-evolutionary feedback regime is even reachable?

End with the no-go claim, not a catalogue of theorem families.

## Methods

1. Define state-specific finite tasks and `g_i`.
2. Define ordered state contrast `Delta g`.
3. Present additive cue-acquisition cost as the constructive linear special case.
4. Generalize to a nondecreasing `L`-bounded lift.
5. Connect `Delta s` to local feedback through `B=-beta e>0`.
6. State exact binary / bounded-arity finite architecture bounds only after the dynamical requirement is defined.

## Results hierarchy

### Result 1 — nonlinear no-go

```text
G <= B L Delta g
and G > G_osc required
=> Delta g > G_osc/(B L)
```

If an architecture class imposes `0<=g_i<=q_max` in every state, then `Delta g<=q_max`; if `B L q_max<=G_osc`, the requested regime is unreachable for the class.

### Result 2 — required contrast implies one high-gap state

If `Delta g>=q` and all `g_i>=0`, then the high state has `g_i>=q`. Apply the existing sharp finite-task theorem to that state. Binary `q=2` gives `(6,5,5)`; bounded arity yields a Pareto set.

### Result 3 — ecological recurrence

Keep the spectral filtering result as supporting ecology: state architecture determines the reward field, while ecological recurrence determines which reward modes persist through time.

### Diagnostic

Keep the complex-eigenpair feedback-existence result short and model-conditional. Do not restore stasis as a coequal Letter headline.

## Figures

Canonical Letter figures:

1. `figures/figure_el1_no_go_v2.svg`
2. `figures/figure_el2_architecture_v2.svg`
3. `figures/figure_el3_recurrence.svg`

Canonical legends: `FIGURE_LEGENDS_EVOLUTION_LETTERS_V2.md`.

## Claim firewall

- necessary contrast bound != sufficiency;
- state gap != between-state contrast;
- finite deterministic architecture != Shannon information;
- constructive linear witness != empirical natural validation;
- slow ecological mode != large evolutionary effect without reward alignment.

## Fallback firewall

`MANUSCRIPT_V1.md` and the four Theoretical Ecology figures remain unchanged. A higher-tier rejection does not authorize theorem hunting; return to Am Nat or the preserved Theoretical Ecology package under the frozen claim ceiling.
