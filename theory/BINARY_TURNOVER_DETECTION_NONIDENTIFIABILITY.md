# Binary network turnover does not identify latent turnover

Status: post-freeze observation-process witness. This file does **not** modify
the frozen Evolution Letters V5 theorem surface and does not claim novelty for
the general occupancy/detection confounding problem.

## Question

Suppose an ecological interaction network is reduced to one binary link state
per dyad in each of two periods. Does the full observed 2 x 2 transition table

- stable absent;
- observed gain;
- observed loss;
- stable present

identify even the **direction** of the corresponding latent link-prevalence
change when detection is imperfect?

No.

## Dynamic latent-state observation model

Let

- `psi` = latent link prevalence in period 1;
- `gamma` = colonization probability for a latent-absent link;
- `epsilon` = extinction probability for a latent-present link;
- `q_1`, `q_2` = period-level probabilities of detecting a latent-present
  link at least once.

Assume no false positives and conditionally independent period-level detections
given the latent states.

The latent prevalence in period 2 is

```text
psi_2 = psi (1-epsilon) + (1-psi) gamma.
```

The observed period marginals are

```text
m_1 = psi q_1
m_2 = psi_2 q_2,
```

and

```text
P(11) = psi (1-epsilon) q_1 q_2.
```

The remaining observed transition cells are fixed by the two marginals and
`P(11)`.

## Exact opposite-direction witness

Consider the same observed binary transition table in both models:

```text
P(00) = 3/5
P(01) = 1/5   # observed gain
P(10) = 1/10  # observed loss
P(11) = 1/10
```

Hence observed link prevalence increases from

```text
m_1 = 1/5
m_2 = 3/10.
```

### Model A: latent prevalence increases

```text
psi       = 1/4
gamma     = 7/18
epsilon   = 1/6
q_1       = 4/5
q_2       = 3/5
```

Then

```text
psi_2 = 1/2
Delta psi = 1/2 - 1/4 = +1/4.
```

### Model B: latent prevalence decreases

```text
psi       = 1/2
gamma     = 1/8
epsilon   = 3/8
q_1       = 2/5
q_2       = 4/5
```

Then

```text
psi_2 = 3/8
Delta psi = 3/8 - 1/2 = -1/8.
```

Both models generate **exactly the same observed 2 x 2 transition table**.

Crucially, every parameter in both witnesses is **strictly interior**:
`0 < psi, gamma, epsilon, q_1, q_2 < 1`. The non-identifiability is therefore
not a boundary artifact of perfect detection, zero extinction, zero
colonization, or deterministic state change.

Thus the observed table cannot identify even the sign of latent link-prevalence
change without additional information about detection.

## Why this is not a new occupancy theorem

The need to distinguish occupancy/state from detection is foundational in the
occupancy literature, and repeated surveys are a standard route to
identification. See, for example:

- MacKenzie & Royle (2005), *Journal of Applied Ecology*,
  DOI: 10.1111/j.1365-2664.2005.01098.x.
- Bailey et al. (2014), *Methods in Ecology and Evolution*,
  DOI: 10.1111/2041-210X.12100.
- Valente et al. (2017), *Methods in Ecology and Evolution*,
  DOI: 10.1111/2041-210X.12840.

The narrower purpose here is to make the identification failure explicit in the
language of **network link gain and loss**, with an exact opposite-direction
witness that can be checked mechanically.

## Relation to the Villavicencio result

Villavicencio contains repeated 5-min censuses, so it has more information than
the binary two-period table in this witness. Those repeated observations are
exactly why detection sensitivity can be diagnosed.

However, the richer beta-binomial observation model is preferred in all six
primary transitions and makes latent transition estimates hit the frozen state
boundary in all six. Thus the empirical data illustrate the same conceptual
boundary: binary link turnover alone is insufficient, and even repeated
detections do not guarantee a stable latent-transition estimate when the
observation model is uncertain.

## Claim ceiling

- This is not a new V5 theorem family.
- Do not claim novelty for generic occupancy/detection confounding.
- The exact contribution is the binary-network opposite-direction witness and
  its role as an explicit rewiring-identification boundary.
- It does not say latent turnover can never be identified; repeated detections,
  validated observation models, experiments, or independent state information
  can supply the missing information.
