# Temporal routing recovery note v1

Status: recovered side-theory map. Source branch:
`theory/ecological-state-observability`.

## Why this line matters

The current decision-ecology paper asks when ecological diversity becomes
effective decision complexity. This side line gives the closest dynamic
extension of that question:

> Can an early cue have value because it predicts which later cue will be
> useful, even when it does not directly predict the final target?

This is not part of the current deterministic worst-case theorem and should not
be inserted merely to increase theorem count.

## Exact results

### Perfect-cue temporal routing

From the minimal four-world strict-gain core, let the binary context transition
satisfy

[
P(C_1=C_0)=ho.
]

At a two-query budget,

[
A_F^{(2)}=rac34,
qquad
A_A^{(2)}=rac34+rac{|2ho-1|}{4}.
]

Hence

[
oxed{
G_{m time}=rac{|2ho-1|}{4}.
}
]

Routing value vanishes exactly at temporal independence (ho=1/2). Both
predictable persistence and predictable alternation create contingent value;
they imply different continuation rules.

### Symmetric noisy factorization

Let the route cue have reliability (age1/2) and specialist cues reliability
(bge1/2). Then

[
oxed{
G_{m noisy}
=
rac{|2ho-1|(2a-1)(2b-1)}{4}.
}
]

Thus the contingent advantage is gated multiplicatively by:

1. temporal predictability;
2. usable early routing information;
3. usable downstream specialist information.

With accuracy value (v) and routing-control cost (k), routing is favored
under the declared model exactly when

[
|2ho-1|(2a-1)(2b-1)>rac{4k}{v}.
]

### Predictive cue usefulness

The arbitrary-binary-transition extension shows that ordinary temporal
dependence is not sufficient. Current context can predict future context while
routing gain remains zero if the same specialist cue is optimal after every
current context.

The operative ecological quantity is therefore:

> predictability of **future cue usefulness**, not environmental persistence
> or target-predictive information alone.

## Canonical branch sources

- `theory/TEMPORAL_ROUTING_THRESHOLD.md`
- `theory/NOISY_TEMPORAL_ROUTING_FACTORIZATION.md`
- `theory/PREDICTIVE_CUE_USEFULNESS_THEOREM.md`
- `theory/EVOLUTIONARY_INFORMATION_ROUTING.md`
- `theory/PRIOR_ART_EVOLUTIONARY_ROUTING.md`
- `theory/README_EVOLUTIONARY_ROUTING.md`
- `adaptive_gain/temporal_routing.py`
- `adaptive_gain/noisy_temporal_routing.py`
- `tests/test_temporal_routing.py`
- `tests/test_noisy_temporal_routing.py`

## Publication disposition

Preferred: a second behavioural/decision-ecology paper on temporal contingent
information acquisition.

Alternative: if the current Letter is later simplified further, this line is a
candidate to replace—not accompany—the eco-evolutionary no-go as the secondary
extension, because it is closer to animal decision making.

Do not combine both extensions simply to maximize scope.

## Claim ceiling

Do not claim novelty for cue hierarchies, temporal autocorrelation, information
costs, adaptive learning, value of information, or sequential choice.

The specific contribution is the exact fixed-versus-contingent value of using
present context to select a future information channel, including its temporal
and noisy collapse conditions.
