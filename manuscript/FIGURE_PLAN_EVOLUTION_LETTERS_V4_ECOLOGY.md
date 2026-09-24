# Evolution Letters figure plan V4 — ecology-first

Status: design specification for the ecology-first V4 candidate. Do not replace the machine-frozen V3 figures until V4 passes its own validation gates.

## Design principle

Each main figure must answer an ecological question before it displays mathematics.

The three figures should read as:

1. **When does contingent sensing pay?**
2. **What kind of natural-history structure creates the advantage?**
3. **When does state-dependent sensing selection persist through time?**

Exact finite corners, Pareto geometry and solver/kernel machinery move to Supplementary Information.

---

## Figure 1. Ecological deadlines expose contingent sensing

### Panel A — one natural-history decision episode

Show a simple encounter sequence:

\[
\text{encounter}
\rightarrow
\text{early cue}
\rightarrow
\begin{cases}
\text{act/stop},\\
\text{sample branch-specific cue}
\end{cases}
\]

Use neutral biological icons or labels such as “resource / host / predator encounter” rather than one taxon-specific claim.

Key message:

> Later cues are conditionally relevant; the organism need not sample all of them on every encounter.

### Panel B — the three ecological budget regions

Show one horizontal budget axis:

- \(B<C_A\): neither strategy completes the decision;
- \(C_A\le B<C_F\): only contingent sensing completes it;
- \(B\ge C_F\): both complete it.

Label the middle region **selection opportunity for contingent sensing**, conditional on the resolution benefit exceeding maintenance cost.

### Panel C — non-monotonic ecological prediction

Plot conceptual performance advantage against available budget or, equivalently, against increasing constraint in reverse direction.

The advantage is zero → positive → zero across the three regions.

Message:

> Contingent sensing is not predicted to be most valuable under the harshest conditions; it is exposed by intermediate ecological constraint.

---

## Figure 2. Branch-specific cue dependence, not cue prevalence, creates adaptive value

### Panel A — two systems with the same marginal cue statistics

Construct two stylized natural-history decision networks with identical numbers of binary cues and balanced outcomes.

**System shared:** later cues are useful across nearly every branch.

**System routed:** an early cue sends the organism to one of several branch-specific terminal cues.

Do not display the full exact extremal construction in the main figure.

### Panel B — fixed versus contingent provisioning

For the shared system, fixed and contingent architectures require similar resources.

For the routed system:

- fixed strategy must provision all branch-specific terminal cues;
- contingent strategy uses routing cues plus only the terminal cue for the realized branch.

A small annotation may state that the repository contains an exactly balanced family in which \(C_F/C_A\) is unbounded.

### Panel C — ecological predictions

Display three predictors with visual emphasis:

- raw cue count: weak proxy;
- marginal cue balance: insufficient;
- conditional cue dependence / branch exclusivity: mechanistic predictor.

Message:

> Natural-history complexity is task- and branch-dependent.

---

## Figure 3. Ecological recurrence filters sensing-generated selection

### Panel A — recurrent ecological states

Show habitat/season/community states connected by transitions. Each state carries a different contingent-sensing payoff, not merely a different environmental value.

### Panel B — same persistence, different payoff alignment

Compare two systems with identical slow environmental modes.

- aligned system: persistent states contrast strongly in sensing payoff;
- unaligned system: persistent states have similar sensing payoff.

### Panel C — long-run consequence

Retain the compact spectral relation

\[
\sigma_{\rm eff}^2
=
\sum_r
w_r
\frac{1+r_r}{1-r_r},
\]

but make the labels biological:

- \(r_r\): ecological persistence;
- \(w_r\): alignment of state-specific sensing selection with that mode.

Message:

> Environmental autocorrelation alone is not enough.

---

## Supplementary figures

### Figure S1 — target-relevant coarse graining

Show:

raw natural-history distinctions
→ declared focal action
→ target-relevant states/cues
→ exact decision problem.

### Figure S2 — finite structural bounds

Move the V3 sharp binary corner and bounded-arity Pareto illustration here.

### Figure S3 — exact balanced-query construction

Show the full routing construction and family-level unbounded ratio here.

---

## Figure-level claim firewall

- Natural-history examples remain illustrative, not fitted empirical systems.
- The middle budget region creates a performance/selection opportunity; selection is positive only under the declared benefit–maintenance condition.
- Branch exclusivity is a mechanistic predictor within the finite deterministic model, not a universal scalar of ecological complexity.
- Crossing the feedback threshold means “not structurally excluded,” not “oscillation guaranteed.”
- Environmental persistence matters only through alignment with state-specific sensing selection.
