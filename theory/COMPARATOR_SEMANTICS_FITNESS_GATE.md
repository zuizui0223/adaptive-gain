# Comparator semantics as an evolutionary fitness gate

Status: side theory on branch theory/opportunity-fitness-process-v1. This note generalizes the Aedes context-semantics warning. It does not change the finite theorem C_A<=C_F. It identifies which biological architecture class C_F actually compares against.

## 1. Three distinct architecture classes

A finite decision task can be embedded in at least three biologically different comparator classes.

### U — universal fixed acquisition

One precommitted resolving bundle is used across all represented ecological states.

Its minimum runtime acquisition cost is

\[
C_U=C_F.
\]

This is the comparator used by the core adaptive-gain theorem.

### A — outcome-contingent routing

Later acquisitions depend on earlier outcomes.

Its minimum worst-path runtime cost is

\[
C_A\le C_U.
\]

The structural gap

\[
g=C_U-C_A
\]

is therefore a runtime advantage of contingent routing relative to one universal fixed acquisition program.

### P — context-preindexed repertoire

A biologically available context is known before the focal acquisition policy is committed, and that context selects a branch-specific fixed program.

If context classes are z in Z and T_z is the branch-local task, define

\[
C_P
=
\max_z C_F(T_z)
\]

when the context is externally or internally available without being charged as a focal acquisition.

This is not the same comparator as C_U.

The central warning is

\[
\boxed{
C_A<C_U
\not\Rightarrow
C_A<C_P.
}
\]

Thus strict adaptive gain does not by itself identify an evolutionary advantage over every biologically available architecture.

## 2. Canonical two-branch task

Let a context/router R have positive acquisition cost r. In branch 0, terminal cue A with cost a resolves the target. In branch 1, terminal cue B with cost b resolves the target. Assume all costs are positive.

For one integrated decision architecture,

\[
C_A=r+\max(a,b),
\]

whereas a universal fixed resolver needs all three information sources,

\[
C_U=r+a+b.
\]

Hence

\[
\boxed{
C_U-C_A=\min(a,b)>0.
}
\]

But if the context is already known before focal policy commitment, the preindexed repertoire needs only the relevant terminal program:

\[
\boxed{
C_P=\max(a,b).
}
\]

Therefore

\[
\boxed{
C_P<C_A<C_U.
}
\]

The same finite environment supports opposite pairwise conclusions depending on the biological comparator:

- A beats U in runtime acquisition;
- P beats A in runtime acquisition.

This is exactly why a positive integrated Aedes fixture cannot establish selection for routing unless the within-architecture status of gonotrophic state is biologically justified.

## 3. Fitness comparison under opportunity closure

Let S(c) be the probability that the ecological opportunity remains available through runtime cost c. Let baseline fitness be w0>0, timely-resolution value v>=0, and architecture-specific log maintenance costs be kappa_U, kappa_A, and kappa_P.

For a deterministic completion cost C_j, define

\[
W_j
=
e^{-\kappa_j}
[w_0+vS(C_j)].
\]

Then the exact pairwise log selection coefficient is

\[
\boxed{
s_{i:j}
=
\log\frac{w_0+vS(C_i)}
{w_0+vS(C_j)}
-(\kappa_i-\kappa_j).
}
\]

For the canonical ordering C_P<C_A<C_U and strictly decreasing S,

\[
\log\frac{w_0+vS(C_A)}
{w_0+vS(C_U)}
>0
\]

but

\[
\log\frac{w_0+vS(C_A)}
{w_0+vS(C_P)}
<0.
\]

So with equal maintenance costs,

\[
\boxed{
A\text{ is favored over }U
\quad\text{but disfavored relative to }P.
}
\]

A can beat P only if its maintenance advantage is large enough to overcome P's runtime advantage:

\[
\boxed{
\kappa_P-\kappa_A
>
\log
\frac{w_0+vS(C_P)}
{w_0+vS(C_A)}.
}
\]

This is an architecture-cost statement, not a routing theorem.

## 4. Process interpretation

The evolutionary chain therefore contains a comparator gate before any population dynamics:

\`\`\`text
finite ecological decision structure
        ->
which architecture classes are biologically available?
        |
        +-- universal fixed U
        +-- contingent routing A
        +-- context-preindexed repertoire P
        ->
runtime completion distributions
        ->
opportunity-dependent performance
        ->
architecture-specific maintenance/developmental cost
        ->
pairwise fitness and selection
\`\`\`

The routeability theorem determines one runtime contrast inside this larger process. It does not choose the biologically correct comparator.

## 5. Acquisition cost and constitutive architecture cost must remain separate

The query costs entering C_A and C_U are per-decision acquisition costs: time, sampling effort, exposure, handling opportunity, or another currency paid when information is acquired.

They are not automatically the constitutive costs of possessing sensory receptors, neural circuitry, memory, or endocrine gating.

Those constitutive costs belong in kappa_j or an equivalent architecture-cost term.

This distinction matters especially when several sensors are maintained continuously but only one is behaviorally consulted in a given context. A fixed genotype can possess both channels while paying only one runtime acquisition cost in each preindexed state.

Therefore the statement

\[
C_U-C_A>0
\]

must never be translated directly as

\[
\text{adaptive architecture has higher fitness}
\]

without declaring both comparator semantics and architecture overheads.

## 6. Relation to PAYOFF

This comparator gate clarifies the relation to PAYOFF.

adaptive-gain can provide runtime-dependent performance values for a declared pair of architectures.

PAYOFF supplies the broader logic

\[
\Phi=R-K,
\]

where K is architecture-specific cost.

For evolutionary use, the relevant R and K must be defined for the same pairwise comparison. Changing from A versus U to A versus P changes both the runtime benefit and potentially the architecture-cost contrast.

Thus there is no universal scalar "adaptive gain" that can be inserted into PAYOFF without a declared comparator.

## 7. Empirical implication

A routeability experiment must distinguish two causal questions:

1. Does the organism use early information to alter later information acquisition?
2. Could the same observed behavior be generated by a context-preindexed repertoire whose branch policy is selected before the focal decision begins?

Evidence for question 1 does not automatically answer question 2.

Useful measurements include:

- timing of the context signal relative to policy commitment;
- whether terminal channels are behaviorally available outside their focal context;
- switching latency after experimental context manipulation;
- costs of maintaining multiple terminal channels;
- costs of the routing/control machinery itself;
- whether context manipulation changes relative terminal-channel dependency rather than only downstream motivation.

## 8. Claim boundary

The exact finite theorem remains

\[
C_A\le C_U.
\]

The evolutionary claim ceiling is narrower:

> contingent routing is selectively favored only relative to a biologically declared comparator after runtime performance and architecture-specific costs are both included.

This is a gate, not a new claim that preindexed repertoires are always available or always cheaper.
