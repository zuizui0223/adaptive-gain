# Detection-effort gain/loss identity

Status: post-freeze observation-process identity. This file does **not** modify
the frozen Evolution Letters V5 theorem surface.

## Setup

Suppose a latent interaction is truly present in both adjacent periods. Let

- `q_1` = probability that the interaction is detected at least once in period 1;
- `q_2` = probability that the interaction is detected at least once in period 2.

The observed binary network records a link as present when at least one
interaction is detected in the period.

Then, even though the latent link never changes,

```text
P(observed gain) = (1 - q_1) q_2
P(observed loss) = q_1 (1 - q_2)
```

and therefore exactly

```text
P(observed gain) - P(observed loss) = q_2 - q_1.
```

So an increase in period-level detectability mechanically creates an excess of
observed gains over losses; a decrease creates an excess of observed losses.

## Census-effort special case

If each of `n` independent focal-plant censuses detects the persistent
interaction with probability `p` when it is present,

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
