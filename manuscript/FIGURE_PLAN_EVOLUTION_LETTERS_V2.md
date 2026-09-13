# Evolution Letters figure plan v2

Status: **canonical three-display-item plan for Letter V2; Theoretical Ecology four-figure package remains untouched.**

The visual grammar must distinguish:

- `g_i=C_F(i)-C_A(i)`: state-specific adaptive-versus-fixed gap;
- `Delta g=g_2-g_1`: between-state structural contrast driving selection/feedback.

## Figure 1 — Architecture creates a dynamical no-go region

**A. State-specific sensing gap.** Show one ecological state with an adaptive branch and a fixed bundle; define `g_i=C_F(i)-C_A(i)`.

**B. Between-state nonlinear bridge.** Show two state gaps `g_1` and `g_2`, their contrast `Delta g=g_2-g_1`, and a family of nondecreasing sensing-to-selection lifts satisfying `Delta s<=L Delta g` and `G<=BL Delta g`.

**C. No-go boundary.** Horizontal axis = available between-state contrast `Delta g`; vertical axis = maximum permitted feedback `BL Delta g`. Shade `BL Delta g<=G_osc` as unreachable. The region beyond the necessary threshold is labelled `not ruled out`, never `guaranteed`.

## Figure 2 — Required contrast implies a high-gap state architecture

Show the logic:

```text
requested regime
-> required between-state contrast Delta g >= q
-> because every g_i >= 0, at least one state has g_i >= q
-> apply sharp single-task finite architecture theorem to that state
```

**A. Binary exact corner.** For `q=2`, show `(n*,m*,E*)=(6,5,5)` as the exact first state-specific gap-capable corner.

**B. Smaller classes ruled out.** Show that architecture classes with `n<=5`, `m<=4`, or `E<=4` impose `0<=g_i<=1` for every state, hence any two states satisfy `|Delta g|<=1`.

**C. Bounded-arity Pareto trade-off.** For `q=3,b=4`, show `(7,6,6)` and `(8,5,5)` as nondominated high-gap-state architectures.

## Figure 3 — Ecology filters structurally generated selection through time

Retain the existing recurrence figure. State-specific sensing architecture determines `g_i` and thus `s_i=f(g_i)-kappa`; the ecological transition operator determines recurrence. Slow ecological modes matter only when centered structural rewards align with them.

## Supplement firewall

Move continuation quotients, productive-frontier construction, proof DAGs, finite enumeration, certificate ladders and detailed bounded-arity proofs out of the Letter narrative.

## Visual claim ceiling

No main figure may imply that:

- one state gap is itself a feedback contrast;
- crossing the nonlinear lower bound guarantees oscillation;
- the six-world witness is a natural system;
- `B`, `L`, `alpha` or `phi` have been empirically estimated;
- finite deterministic structure is a Shannon-information bound.
