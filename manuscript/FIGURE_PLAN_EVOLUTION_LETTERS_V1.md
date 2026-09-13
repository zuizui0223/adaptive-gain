# Evolution Letters figure plan v1

Status: **three-display-item higher-tier plan; Theoretical Ecology four-figure package remains untouched.**

The Letter should use at most three main figures. Their order follows the biological claim, not the history of the mathematics.

## Figure 1 — Architecture creates a dynamical no-go region

### Question

When is a finite sensing architecture too simple to support a requested local eco-evolutionary regime?

### Layout

**Panel A — biological decision architecture**

Show one small natural-history decision problem:

```text
ecological alternatives
        ↓
coarse cue
   ↙         ↘
branch cue A  branch cue B
```

Beside it, contrast:

```text
adaptive: acquire only the branch-relevant cue
fixed:    carry both branch cues in advance
```

Define only the visual quantity:

```text
Delta g = C_F - C_A
```

Do not show proof machinery.

**Panel B — nonlinear biological bridge**

Plot a family of admissible nondecreasing sensing-to-selection curves below a common slope ceiling `L`. The vertical contrast at structural separation `Delta g` is bounded by

```text
Delta s <= L Delta g
G <= B L Delta g
```

The family should include a linear curve and at least one saturating curve. The figure must communicate that the theorem uses the ceiling, not exact linearity.

**Panel C — feedback phase boundary**

Horizontal axis: achievable structural gap or its finite architecture proxy.
Vertical axis: maximum permitted feedback `B L Delta g`.

Draw horizontal line `G_osc`. Shade:

```text
B L Delta g <= G_osc
```

as **UNREACHABLE OSCILLATORY REGIME**.

Mark the first necessary integer gap `q_osc^nec` immediately to the right of the prohibited region.

Key sentence inside panel:

> Architecture below the bound cannot generate the requested regime for any lift in the declared monotone-Lipschitz class.

### Claim ceiling

Crossing the line is labelled **not ruled out**, never **guaranteed**.

---

## Figure 2 — Required dynamics imply finite natural-history architecture

### Question

Once a dynamical regime requires gap `q`, what finite sensing structure is minimally capable of that gap?

### Panel A — binary exact corner

Show the map

```text
required regime
→ q
→ h_2*(q)
→ (n*, m*, E*)
```

with

```text
(n*,m*,E*) = (h_2*+q+1, h_2*+q, h_2*+q)
```

Use the canonical `q=2` example to mark the exact binary first corner `(6,5,5)`.

### Panel B — smaller scopes ruled out

Three simple crossed-out icons:

- `n <= 5` represented alternatives;
- `m <= 4` binary cue resources;
- `E <= 4` irreducible fixed obligations.

Each has `Delta g <= 1`, so each is prohibited in the canonical nonlinear no-go example where `q>=2` is necessary.

### Panel C — bounded-arity Pareto trade-off

Use `q=3, b=4` and display the two nondominated points

```text
(8,5,5)
(7,6,6)
```

The visual message is that richer cue outcomes trade represented alternatives against cue/obligation burden; there is generally no universal scalar minimum.

---

## Figure 3 — Ecology filters structurally generated selection through time

### Question

Why does sufficient sensing architecture not by itself determine long-term evolutionary effect?

### Panel A — shared ecological state space

```text
community state i
   ├─ finite sensing architecture → g_i → s_i
   └─ transition operator P        → recurrence
```

### Panel B — modal alignment

Draw two reward vectors over the same slow ecological mode:

1. reward aligned with slow mode → large long-run contribution;
2. reward nearly orthogonal → small long-run contribution.

Use the spectral expression only once:

```text
sigma_eff^2 = sum_r w_r (1+r_r)/(1-r_r)
```

### Panel C — biological synthesis

Two-line conclusion:

> What organisms can distinguish bounds the available selection contrast.
>
> How ecological states recur determines which part of that contrast persists through time.

---

## What moves to Supplement

- continuation bisimulation;
- productive-frontier construction details;
- proof DAGs and integer/fractional certificates;
- exhaustive finite task enumeration;
- bounded-arity recurrence proof details;
- exact equality witness derivations;
- local feedback identifiability algebra beyond the one diagnostic statement retained in text.

## Figure firewall

The main figures must not imply:

- that structural gap is intrinsically fitness;
- that crossing the nonlinear lower bound is sufficient for oscillation;
- that `B`, `L`, `alpha` or `phi` have been empirically estimated;
- that the six-world witness is a natural system;
- that finite deterministic architecture replaces Shannon information;
- that ecological slow modes cause selection without reward-mode alignment.
