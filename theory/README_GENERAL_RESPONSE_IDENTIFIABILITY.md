# General-response identifiability branch

This dependent branch asks which parts of the generalized eco-evolutionary
feedback model can actually be recovered from an observed local evolutionary
trajectory.

For the full hierarchy from static sensing structure through exogenous timescale
filtering, endogenous feedback, generalized evolutionary response, and inverse
identifiability, read `ECO_EVOLUTIONARY_TIMESCALE_THEORY_MAP.md` first.

The inverse now has two distinct gates before structural interpretation:

```text
phenotype / evolutionary transient
        |
        v
Gate 1: scalar mode observability
        R = x0*x2 - x1^2
        |
        | R != 0
        v
trace T + determinant D
        |
        v
Gate 2: biological identifiability ridge E(T,D)
        |
        +--> independent alpha  -> phi, G
        |
        +--> independent phi    -> alpha, G
        |
        v
selection / ecological factorization
        |
        v
finite sensing structure Delta_g
```

Read in this order:

1. `ECO_EVOLUTIONARY_TIMESCALE_THEORY_MAP.md`
   - fixes the logical hierarchy of static sensing structure, exogenous temporal
     filtering, endogenous feedback, the parent inverse, the generalized
     evolutionary response, and the generalized identifiability boundary;
   - separates exact general claims from special-case claims and open empirical
     layers;
   - gives the forward and inverse research spines in one place.

2. `SCALAR_TRANSIENT_OBSERVABILITY.md`
   - states when one observed scalar trajectory can recover the second-order
     invariants at all;
   - derives the four-point rank condition

     \[
     R=x_0x_2-x_1^2;
     \]

   - shows a pure single eigenmode has `R=0` even with an arbitrarily long time
     series;
   - distinguishes exact non-observability from near-degenerate numerical
     conditioning.

3. `GENERAL_RESPONSE_IDENTIFIABILITY.md`
   - assumes `(T,D)` have passed the first gate;
   - derives the exact `(alpha,phi,G)` equivalence ridge;
   - recovers the earlier `alpha=1` inverse as a special case;
   - proves stable high-trace transients can leave generalized loop gain
     unbounded above;
   - states the independent persistence measurement needed to collapse the
     ridge.

Executable layers:

- `adaptive_gain/general_response_scalar_observability.py`
- `adaptive_gain/general_response_identifiability.py`
- `tests/test_general_response_scalar_observability.py`
- `tests/test_general_response_identifiability.py`
- `validation/general_response_scalar_observability_v1.json`
- `validation/general_response_identifiability_v1.json`

## Gate 1 — does the scalar trajectory expose two local modes?

Every scalar coordinate obeys

\[
x_{t+2}=T x_{t+1}-D x_t.
\]

Four points identify `(T,D)` only when

\[
\boxed{R=x_0x_2-x_1^2\ne0.}
\]

Then

\[
\boxed{
T=\frac{x_0x_3-x_1x_2}{R},
\qquad
D=\frac{x_1x_3-x_2^2}{R}.
}
\]

For two real modes

\[
x_t=c_1r_1^t+c_2r_2^t,
\]

\[
\boxed{R=c_1c_2(r_1-r_2)^2.}
\]

So the gate closes if one mode is absent or the modes coincide.  More data on
the same pure mode do not reveal the missing timescale.

## Gate 2 — can the observed invariants be assigned biologically?

The generalized local invariants are

\[
T=\alpha+\phi,
\qquad
D=\alpha\phi+(1-\phi)G.
\]

For every feasible candidate community memory,

\[
\boxed{\alpha(\phi)=T-\phi}
\]

and

\[
\boxed{
G(\phi)=\frac{D-T\phi+\phi^2}{1-\phi}
}
\]

produce exactly the same transient geometry.

The earlier inverse branch is recovered by imposing

\[
\alpha=1,
\]

which collapses the ridge to

\[
\phi=T-1.
\]

The strongest generalized nonidentifiability result is

\[
\boxed{
\text{stable }T\ge1
\Rightarrow
G(\phi)\to+\infty\text{ as }\phi\to1^-.
}
\]

So even after both local modes are visible, transient geometry alone can fail to
place any finite upper bound on generalized feedback gain.

The repo-native collision

\[
T=1.8,
\qquad D=0.825
\]

is simultaneously compatible with

```text
(alpha, phi, G)
(1.00, 0.80, 0.125)
(0.90, 0.90, 0.150)
(0.81, 0.99, 2.310)
```

and the compatible gain diverges further as `phi -> 1-`.

## Revised empirical ladder

1. design a perturbation that exposes two local modes and pass the `R != 0`
   observability gate;
2. recover the free-system invariants `(T,D)`;
3. independently measure either evolutionary persistence `alpha` or community
   memory `phi`;
4. recover the other persistence term and generalized gain `G`;
5. independently factor ecological and selection response;
6. only then compare with the exact finite sensing gap and its structural bounds.

The biological message is therefore stronger than saying evolution and ecology
have different timescales:

\[
\boxed{
\text{one observed long trajectory need not reveal either timescale separately.}
}
\]

It can fail first because only one mode is visible, and second because even two
visible modes identify only their combined local eigenstructure.

Independent validation includes 200,000 random stable generalized-response
systems for the identifiability ridge and 200,000 random two-real-mode
trajectories for the Hankel visibility identity.  These are deterministic
algebraic checks, not statistical guarantees under field noise.

Prior-art boundary: second-order recurrence identification, Hankel rank, and
generic parameter nonidentifiability are standard.  The repository-specific
consequence is the two-stage boundary they impose on reversing exact finite
sensing structure from an observed eco-evolutionary transient.
