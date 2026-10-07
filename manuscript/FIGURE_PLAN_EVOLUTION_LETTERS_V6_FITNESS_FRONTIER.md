# Figure plan — Evolution Letters V6 fitness frontier

## Figure 1 — Natural history re-ranks an exact structural frontier

### Question

Does the architecture that maximizes structural adaptive gain also maximize
biological value?

### Panel A — Exact finite frontier

Show one schematic routeable tree and the finite frontier concept.

For fixed (n,m,b), plot:

- x-axis: adaptive worst-path cost (C_A=h);
- y-axis: sharp fixed burden (C_F=I_h).

Highlight the binary (n=10,m=9) points:

[
(2,3),quad(3,7),quad(4,9).
]

Annotate:

- every plotted point is constructively attainable;
- the frontier is not one scalar adaptive-gain score.

### Panel B — Structural ranking

Plot or label the fixed/adaptive ratios:

[
3/2,quad7/3,quad9/4.
]

Highlight (h=3) as the ratio optimum.

### Panel C — Natural-history ranking

For exponential completion value

[
U(c)=e^{-mu c},
]

plot

[
U(h)-U(I_h)
]

against (mu) for the three highlighted frontier points.

Mark the two crossings near:

[
mu=0.1546968,
qquad
mu=0.6562560.
]

Show the optimum sequence:

[
h^*:4	o3	o2.
]

### Figure 1 message

> The structural frontier is fixed, but natural history chooses which point is
> valuable.

Do not label (C_F/C_A) as fitness.

---

## Figure 2 — Finite information constraints impose exact evolutionary no-go regions

### Question

How costly can contingent control be before no finite environment in a declared
information class can support it?

### Panel A — Inverse resource requirement

Schematic of

[
K
	o
J_K(h)
	o
I_hge J_K(h).
]

Show that natural history plus control cost determines the fixed burden required
at each adaptive depth.

Use one shallow depth that fails structurally, one feasible intermediate depth,
and one late depth that fails biologically.

### Panel B — Global cue-arity ceilings

For

[
U(c)=e^{-0.3c},
]

plot

[
K_{m crit,robust}^{(b)}
]

against cue arity (b).

Mark:

- binary: approximately 0.290085;
- ternary: approximately 0.386328;
- unrestricted finite-information robust supremum:
  (e^{-0.6}approx0.548812).

Draw a horizontal line at

[
K=0.30.
]

This visually gives

[
b_{min}^{m robust}=3.
]

### Panel C — Interpretation

Use a three-level no-go schematic:

1. finite (n,m,b) resource ceiling;
2. unlimited task size but bounded cue arity;
3. unlimited finite information structure.

Emphasize that the result concerns query-outcome branching in the declared
model, not receptor number or neural complexity.

### Figure 2 message

> Some control costs cannot be paid by adding more environmental states or
> more sensors; the information branching class itself can be limiting.

---

## Figure 3 — Encounter frequencies create value unavailable to robust architecture

### Question

Can an architecture be favored in expectation even when no finite architecture
can make it valuable in every state?

### Panel A — Robust versus expected ceilings

For bounded-below (U), show:

[
sup R_{m robust}=U(2)-U_infty,
]

[
sup R_{m expected}=U(1)-U_infty.
]

Shade the frequency-assisted evolvability band:

[
U(2)-U_infty
le K
<
U(1)-U_infty.
]

For exponential (U(c)=e^{-0.3c}), annotate:

- robust ceiling (approx0.548812);
- expected ceiling (approx0.740818);
- example (K=0.60).

### Panel B — Finite-scope rescue

Use the exact finite (n=10,m=9) expected ceiling:

[
U(1)-U(9)
approx0.673613.
]

Show a binary tree with:

- common one-query branch;
- rare branches carrying the fixed burden.

Plot expected value against one-step encounter mass (p_1).

Mark the finite-scope threshold for (K=0.60):

[
p_{1,m crit}approx0.6166.
]

Optionally show the scalable asymptotic threshold

[
p_{m crit}approx0.2666
]

as a dashed comparison, clearly labeled as a different scope.

### Panel C — Public Aedes temporal process anchor

Plot the aggregate post-CO2 IR-minus-no-IR Figure 3a contrast through time for
the two post-pulse intervals, or plot cumulative signed advantage.

Mark the half-area times:

- 46.2 s;
- 46.5 s.

Label explicitly:

> temporal process-shape anchor — not a fitness estimate.

### Figure 3 message

> Information branching controls robust value; encounter frequency controls the
> additional early-termination premium.

---

## Supplementary figures

### Figure S1 — protected-spine private-pair sharpness construction

Show how one deepest world forces (C_A=h) while one private pair per internal
query forces (C_F=I_h).

### Figure S2 — extremal ratio versus biological value

Use the exact binary family

[
C_A=d+1,qquad C_F=2^d.
]

Show:

- (C_F/C_A	oinfty);
- for fixed exponential urgency, biological value tends to zero.

### Figure S3 — robust versus expected decomposition within one task

Show:

[
R_{m expected}
=
R_{m robust}
+
P_{m early}.
]

### Figure S4 — scalable complexity

Show the near-maximal-value scaling:

[
C_{A,min}=Theta(log(1/mu)),
]

[
C_{F,min},n_{min},m_{min}
=
Theta(1/mu).
]

Keep as Supplement because log-versus-linear adaptivity gaps have substantial
algorithmic prior art.

## Visual claim firewall

Main figures must not visually imply:

- (C_F/C_A) is fitness;
- cue arity is receptor number;
- the Aedes curve estimates (U(c));
- robust no-go means expected selection is impossible;
- expected-value rescue is distribution free.
