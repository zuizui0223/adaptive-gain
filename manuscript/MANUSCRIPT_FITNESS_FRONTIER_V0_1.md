# Manuscript v0.1 — Natural history selects among finite information architectures

Status: synthesis draft on `theory/opportunity-fitness-process-v1`.
This document is intentionally shorter than the theorem archive. It defines one
paper-sized biological story.

## Working title

**Natural history selects among finite information architectures**

Alternative:

**Ecological time value re-ranks the finite frontier of adaptive sensing**

## One-sentence claim

> Structural adaptive gain is potential, not fitness: natural history re-ranks
> an exact finite frontier of information architectures, while encounter
> frequencies add an early-termination premium that can favor architectures
> which cannot repay their cost robustly in every ecological state.

## Biological question

Why can contingent sensing or behavioral flexibility be strongly favored in one
ecological setting but not another, even when the available cues and hidden
states are structurally similar?

The paper answers this in two steps:

1. finite information structure determines what adaptive/fixed completion-cost
   pairs are attainable;
2. natural history determines how those completion costs translate into
   biological value.

The main object is therefore not one scalar "adaptive gain."

It is an exact structural frontier plus a biological value function.

## Result 1 — exact finite structural frontier lifts sharply to biological value

Fix:

- (n) represented ecological worlds;
- (m) query resources;
- maximum query arity (b);
- unit query costs.

For adaptive worst-path depth (h), define

[
I_h=min{m,F_b(n,h)}.
]

The protected-spine private-pair construction attains

[
oxed{(C_A,C_F)=(h,I_h)}
]

for every feasible (h).

Therefore for any finite nonincreasing biological completion value (U(c)),

[
oxed{
R_{m robust,max}
=
max_h
left[
U(h)-U(I_h)
ight].
}
]

This is the first headline theorem.

Interpretation:

> finite information architecture gives an exact set of attainable robust
> benefits before any particular ecological time model is chosen.

The old linear map

[
R=lambda(C_F-C_A)
]

is recovered only when

[
U(c)=-lambda c.
]

Thus the additive structural gap is biologically sufficient only under constant
marginal value of decision time.

## Result 2 — natural history can prefer a different architecture than structural adaptive gain

Use exponential opportunity value

[
U_mu(c)=v e^{-mu c}.
]

For binary (n=10,m=9), relevant exact frontier points are

[
(2,3),quad(3,7),quad(4,9).
]

The structural ratio (C_F/C_A) is maximized at (h=3).

But the robust ecological envelope selects

[
h^*(mu)=4	o3	o2
]

as urgency increases, with crossings near

[
mu=0.1546968
]

and

[
mu=0.6562560.
]

Therefore

[
oxed{
argmax C_F/C_A

eq
argmax R_{m robust}
}
]

in general.

A stronger counterexample comes from the exact binary extremal family:

[
C_A=d+1,
qquad
C_F=2^d.
]

Then

[
C_F/C_A	oinfty,
]

while for every fixed (mu>0),

[
v
left[
e^{-mu(d+1)}
-
e^{-mu2^d}
ight]
	o0.
]

So structural adaptivity can become arbitrarily more dramatic while its
ecological value vanishes.

This is the second headline result.

## Result 3 — finite information constraints impose exact evolvability ceilings

On an additive architecture-value scale

[
Phi=R-K,
]

define

[
oxed{
K_{m crit}^{m robust}
=
max_h
left[
U(h)-U(I_h)
ight].
}
]

Then

[
oxed{
exists	ext{ a task in the declared }(n,m,b)	ext{ scope with }
Phi_{m robust}>0
iff
K<K_{m crit}^{m robust}.
}
]

So the theory gives an exact upper bound on the constitutive control cost that
the declared finite information architecture can repay robustly.

If world/query counts may grow without bound but cue arity remains (b),

[
oxed{
K_{m crit,robust}^{(b)}
=
max_{hge2}
left[
U(h)-U(J_b(h))
ight],
}
]

where

[
J_b(h)=rac{b^h-1}{b-1}.
]

This yields a global model-class no-go.

For

[
U(c)=e^{-0.3c},
]

the binary ceiling is

[
K_{m crit,robust}^{(2)}
approx0.290085.
]

Thus (K=0.30) cannot be repaid robustly by any finite deterministic binary
task, regardless of the number of worlds or binary query resources.

Ternary cues raise the ceiling to approximately

[
0.386328,
]

so the same cost has exact minimum robust cue arity

[
oxed{b_{min}=3.}
]

This is a model-specific arity result, not a claim about receptor count.

## Result 4 — encounter frequencies create an expected-only evolutionary regime

The robust result is frequency-free.

Expected value uses branch frequencies:

[
R_{m expected}(pi)
=
sum_x p_xU[T_pi(x)]
-
U(C_F).
]

For a minimax tree,

[
R_{m expected}
=
R_{m robust}
+
P_{m early},
]

where

[
P_{m early}
=
sum_xp_x
left[
U(T_pi(x))-U(C_A)
ight]
ge0.
]

This early-termination premium gives different absolute ceilings.

Across all finite tasks,

[
oxed{
R_{m robust}^{sup}
=
U(2)-U_infty
}
]

whereas, allowing arbitrarily skewed positive world frequencies,

[
oxed{
R_{m expected}^{sup}
=
U(1)-U_infty.
}
]

Therefore an exact expected-only regime exists:

[
oxed{
U(2)-U_infty
le
K
<
U(1)-U_infty.
}
]

For exponential value with (mu=0.3,v=1),

[
K_{m robust}^{sup}
=
e^{-0.6}
approx0.548812,
]

but

[
K_{m expected}^{sup}
=
e^{-0.3}
approx0.740818.
]

A finite binary witness with 99% encounter probability on a one-query common
state repays

[
K=0.60
]

in expectation even though no finite information architecture can repay that
cost robustly in every represented world.

This is the third biological headline.

## Result 5 — fixed finite ecology and scalable ecology have different low-urgency limits

For any fixed finite ((n,m,b)),

[
K_{m crit,robust}(mu)	o0
]

as

[
mu	o0^+
]

and as

[
mu	oinfty.
]

Thus positive-cost robust adaptivity is band-pass in a fixed finite problem.

But if task size may scale at fixed cue arity,

[
K_{m crit,robust}^{(b)}(mu)	o v
]

as

[
mu	o0^+.
]

Hence low urgency does not intrinsically erase adaptive value.

It erases adaptive value only when ecological information complexity is held
finite.

To retain a fixed fraction (1-arepsilon) of the full value as
(mu	o0), the minimum attainable resource scales obey

[
C_{A,min}
=
Theta(log(1/mu)),
]

while

[
C_{F,min},
quad
n_{min},
quad
m_{min}
=
Theta(1/mu).
]

This is a supporting asymptotic result, not the lead theorem.

## Empirical anchor — Aedes multisensory host seeking

Chandel et al. 2024 Figure 3a supplies a public 300-s, 10-FPS aggregate
host-seeking trajectory.

After transient CO2 stimulation, the +IR contrast is strongly late-weighted.

Half of the signed post-pulse IR advantage accumulates only after approximately

[
46.2 {m s}
]

after the first pulse and

[
46.5 {m s}
]

after the second.

Thus the ecological value of the same cue effect depends strongly on the
value-of-time kernel.

This result is a process-shape anchor only.

It does not identify:

- individual completion-time distributions;
- adaptive versus fixed sensory architecture;
- natural opportunity survival;
- selection coefficients.

The Figure 3a raw-video mapping remains unresolved and is explicitly blocked.

## Figures

### Figure 1 — structure is not fitness

Panel A:
one finite routing task and the distinction between (C_A) and (C_F).

Panel B:
exact frontier

[
(h,I_h).
]

Panel C:
two biological value functions (U(c)) rank frontier points differently.

### Figure 2 — natural history re-ranks the frontier

Binary (n=10,m=9).

Show the three relevant points

[
(2,3),(3,7),(4,9)
]

and the urgency-dependent optimum

[
4	o3	o2.
]

Inset:
the exact extremal family where structural ratio rises while ecological value
falls.

### Figure 3 — evolutionary feasibility ceilings

Panel A:
finite-scope (K_{m crit}^{m robust}).

Panel B:
arity-limited global ceilings for (b=2,3,4,ldots).

Panel C:
the expected-only interval between

[
U(2)-U_infty
]

and

[
U(1)-U_infty.
]

### Figure 4 — empirical process shape

Chandel Figure 3a aggregate temporal contrast.

Show cumulative post-pulse IR advantage and exponential value-kernel
sensitivity.

Label explicitly:

**process-shape anchor, not fitness validation.**

## What the paper must not claim

Do not headline:

- sequential information has value;
- deadlines alter decisions;
- adaptive policies can outperform nonadaptive policies;
- expected and worst-case decision trees differ;
- time pressure changes cue use;
- response-time distributions matter;
- logarithmic routing can beat linear provisioning.

All have substantial prior art.

## Candidate novelty statement

> The contribution is a sharp cross-layer theory: exact finite constraints on
> ecological information architecture determine an attainable
> adaptive/nonadaptive frontier, and any monotone biological value of decision
> completion lifts that frontier exactly. This yields natural-history-dependent
> architecture rankings, robust evolvability ceilings, and a precise separation
> between statewise robust value and frequency-dependent expected value.

## Discussion claim

The conceptual correction is:

> environmental complexity does not have one intrinsic adaptive value.

Its evolutionary value depends on three separable layers:

1. what decision architectures are structurally attainable;
2. where natural history assigns value to earlier completion;
3. how often each branch of the environment is encountered.

This is the paper.
