# Temporal routing recovery note v2

Status: recovered onto the active synthesis branch and integrated as the
secondary decision-ecology result in the current manuscript. Source lineage:
\`theory/ecological-state-observability\`.

## Why this line matters

The current paper asks when ecological diversity becomes effective decision
complexity. The temporal extension asks the dynamic version:

> Can an early cue have value because it predicts which later cue will be
> useful, even when it does not directly predict the final target?

This result is deliberately secondary to the deterministic
static-information/accessibility theorem.

## Exact results

### Perfect-cue temporal routing

From the minimal four-world strict-gain core, let

\[
P(C_1=C_0)=\rho.
\]

At a two-query budget,

\[
A_F^{(2)}=\frac34,
\qquad
A_A^{(2)}=\frac34+\frac{|2\rho-1|}{4}.
\]

Hence

\[
\boxed{
G_{\rm time}=\frac{|2\rho-1|}{4}.
}
\]

Routing value vanishes exactly at temporal independence
\(\rho=1/2\). Predictable persistence and predictable alternation both create
contingent value; they imply opposite continuation rules.

### Symmetric noisy factorization

Let the route cue have reliability \(a\ge1/2\) and specialist cues reliability
\(b\ge1/2\). Then

\[
\boxed{
G_{\rm noisy}
=
\frac{|2\rho-1|(2a-1)(2b-1)}{4}.
}
\]

Thus the contingent advantage is gated multiplicatively by temporal
predictability, usable early routing information and usable downstream
specialist information.

With accuracy value \(v\) and routing-control cost \(k\), routing is favored
under the declared model exactly when

\[
|2\rho-1|(2a-1)(2b-1)>\frac{4k}{v}.
\]

### Predictive cue usefulness

The arbitrary-binary-transition extension shows that temporal dependence is
not sufficient. Current context can predict future context while routing gain
remains zero if the same specialist cue is optimal after every current
context.

The operative ecological quantity is therefore:

> predictability of **future cue usefulness**, not environmental persistence
> or target-predictive information alone.

## Active-branch assets

- \`theory/TEMPORAL_ROUTING_THRESHOLD.md\`
- \`theory/NOISY_TEMPORAL_ROUTING_FACTORIZATION.md\`
- \`theory/PREDICTIVE_CUE_USEFULNESS_THEOREM.md\`
- \`theory/PRIOR_ART_EVOLUTIONARY_ROUTING.md\`
- \`adaptive_gain/temporal_routing.py\`
- \`adaptive_gain/noisy_temporal_routing.py\`
- \`tests/test_temporal_routing.py\`
- \`tests/test_noisy_temporal_routing.py\`
- \`validation/temporal_routing_threshold_v1.json\`
- \`validation/noisy_temporal_routing_factorization_v1.json\`

## Publication disposition

The compact temporal theorem and noisy factorization are now part of the
current Letter as a secondary extension, with derivation in the integrated
Supplement. The broader evolutionary-routing material remains available for a
future dedicated treatment.

The nonlinear eco-evolutionary no-go is not combined as a coequal main result;
it remains preserved in the Supplement.

## Claim ceiling

Do not claim novelty for cue hierarchies, temporal autocorrelation, information
costs, adaptive learning, value of information or sequential choice.

The specific contribution is the exact fixed-versus-contingent value of using
present context to select a future information channel, including its temporal
and noisy collapse conditions.
