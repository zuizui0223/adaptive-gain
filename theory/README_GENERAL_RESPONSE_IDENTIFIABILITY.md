# General-response identifiability branch

This dependent branch asks which parts of the generalized eco-evolutionary
feedback model can actually be recovered from an observed local evolutionary
trajectory.

```text
phenotype / evolutionary transient
        |
        v
trace T + determinant D
        |
        v
identifiability ridge E(T,D)
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

Read `GENERAL_RESPONSE_IDENTIFIABILITY.md` for the derivation.

Executable layer:

- `adaptive_gain/general_response_identifiability.py`
- `tests/test_general_response_identifiability.py`
- `validation/general_response_identifiability_v1.json`

The generalized local invariants are

\[
T=\alpha+\phi,
\qquad
D=\alpha\phi+(1-\phi)G.
\]

Thus an ideal local scalar recurrence identifies only two quantities:

\[
x_{t+2}=T x_{t+1}-D x_t.
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

The earlier inverse branch is recovered by imposing the parent response law

\[
\alpha=1.
\]

Then

\[
\phi=T-1
\]

and the ridge collapses to one point.

The strongest generalized nonidentifiability result is:

\[
\boxed{
\text{stable }T\ge1
\Rightarrow
G(\phi)\to+\infty\text{ as }\phi\to1^-.
}
\]

So without an independent persistence measurement, a stable long transient can
be compatible with arbitrarily large generalized loop gain.  In that regime the
time series alone cannot place a finite upper bound on the structural sensing
gap through the generalized feedback mechanism.

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

and the gain diverges further as memory approaches one.

This changes the empirical ladder from the parent inverse:

1. free coupled trajectory -> estimate `(T,D)`;
2. independently measure either evolutionary persistence `alpha` or community
   memory `phi`;
3. recover the other persistence term and generalized gain `G`;
4. independently factor ecological/selection response;
5. only then compare with the exact finite sensing gap and its structural bounds.

The biological message is therefore not merely that evolution and ecology have
different timescales.  Their apparent timescales can be **locally confounded in
the same observed trajectory**.  Experimental separation of evolutionary memory
from ecological memory is required before assigning a long transient to one or
the other.

Independent validation used 200,000 random stable generalized-response systems;
alternative decompositions reproduced the same trace/determinant to machine
precision, with zero failures of the high-trace unbounded-gain criterion and zero
violations of the finite identified envelope when `T<1`.

Prior-art boundary: second-order trace/determinant inversion and generic parameter
nonidentifiability are standard.  The repository-specific consequence is the
boundary they impose on reversing the exact finite sensing-gap theory from an
observed eco-evolutionary transient.
