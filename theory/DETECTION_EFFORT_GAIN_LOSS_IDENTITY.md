# Detection-effort gain/loss identity

Status: post-freeze observation-process identity. This file does **not** modify
the frozen Evolution Letters V5 theorem surface.

## Setup

For any two binary observations `Y_1,Y_2`,

```text
P(Y_1=0,Y_2=1) - P(Y_1=1,Y_2=0)
= P(Y_2=1) - P(Y_1=1).
```

This is a probability-conservation identity and requires **no independence
assumption**.

Now suppose a latent interaction is truly present in both adjacent periods.
Let

- `q_1` = marginal probability that the interaction is detected at least once in period 1;
- `q_2` = marginal probability that the interaction is detected at least once in period 2.

Then, even if period-level detection events are correlated,

```text
P(observed gain) - P(observed loss) = q_2 - q_1.
```

If period-level detections are additionally conditionally independent given
the persistent latent link, the individual transition probabilities factor as

```text
P(observed gain) = (1 - q_1) q_2
P(observed loss) = q_1 (1 - q_2).
```

So an increase in period-level detectability mechanically creates an excess of
observed gains over losses; a decrease creates an excess of observed losses.

## Directional odds identity

Under the additional period-level conditional-independence assumption, and
whenever both observed-gain and observed-loss probabilities are non-zero,

```text
P(observed gain) / P(observed loss)
= [(1-q_1) q_2] / [q_1 (1-q_2)]
= odds(q_2) / odds(q_1).
```

Equivalently,

```text
log[P(observed gain) / P(observed loss)]
= logit(q_2) - logit(q_1).
```

Thus, for a persistent latent link, the observed gain:loss direction is exactly
the period-level **detectability odds ratio**. This is stronger than saying
sampling effort is merely correlated with turnover: the binary observation map
itself converts a detectability change into directional apparent turnover.

## Census-effort special case

If each of `n` conditionally independent focal-plant censuses detects the
persistent interaction with probability `p` when it is present,

```text
q(n) = 1 - (1 - p)^n.
```

For fixed `0 < p < 1`, `q(n)` is strictly increasing in `n`. Hence:

```text
n_2 > n_1  =>  P(observed gain) > P(observed loss)
n_2 = n_1  =>  P(observed gain) = P(observed loss)
n_2 < n_1  =>  P(observed gain) < P(observed loss).
```

This is an observation-process identity, not an ecological transition theorem.

The beta-binomial robustness result in Villavicencio shows why the independent-
census formula for `q(n)` should not be treated as the true observation model.
Crucially, the more general binary conservation identity above survives that
relaxation: any change in marginal observed-presence probability creates a
gain-minus-loss imbalance, regardless of the within- or between-period
dependence structure.

## Interpretation

The identity explains why unequal effort can generate directional observed-link
turnover even for a completely persistent latent network. It does not imply
that every observed gain/loss is false. When true latent transitions and
time-varying detectability both occur, observed binary direction is a mixture of
ecological state change and observation-state change.

The Villavicencio effort audit uses this identity only as a diagnostic of the
binary observation map. It does not promote model-based latent states to truth.

## Claim ceiling

- Do not call this a new V5 theorem family.
- Do not infer the biological fraction of observed turnover from the identity.
- Do not assume independent per-census detection is the true observation model.
- Use it to show why binary gain/loss direction is not identified when
  period-level detection probabilities differ.
