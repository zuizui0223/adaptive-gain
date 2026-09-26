# Mutation-radius thresholds for routing accessibility

Status: side theory. This note extends the deletion-only routing mutation model and is not part of the frozen Theoretical Ecology submission.

## 1. Coordinated mutation radius

`LOCAL_ROUTING_MUTATION_ACCESSIBILITY.md` takes one elementary mutation to delete one target-irrelevant acquisition occurrence from one branch.

Here define a larger mutation event with integer edit radius

```text
rho>=1
```

that may bundle at most `rho` such elementary deletion edits in one event. The ecological task, target, cue vocabulary and cue outcomes remain fixed.

This radius is a declared genotype-policy mutation geometry. It is not PAYOFF's architecture coordinate, not Hegselmann-Krause interaction radius, and not an empirical mutation-effect distribution.

## Proposition LRM3 — exact first-benefit and direct-target jump radii

In the `k`-branch routing family, starting from the full zero-saving program:

### First strictly beneficial mutant

The exact minimum edit radius for a one-event mutant with positive realized structural gain is

```text
boxed: rho_first=k.
```

### Direct jump to realized gain r

For any

```text
1<=r<=k-1,
```

the exact minimum edit radius for one mutation event to produce

```text
g>=r
```

is

```text
boxed: rho_direct(r)=k r.
```

### Proof

Gain `r` requires every one of the `k` branch programs to be shortened by at least `r`. Therefore any direct mutation must contain at least `k r` elementary deletions. Exactly `r` deletions in each branch attain the target. Setting `r=1` gives `rho_first=k`. QED.

## 2. Strict-improvement versus neutral-permitting accessibility

If the evolutionary/search process accepts only one-event mutants with **strictly larger** realized gain, then:

```text
rho<k
-> the full program has no admissible beneficial neighbor
-> strict-improvement process is locally trapped.
```

If

```text
rho>=k,
```

a strictly improving path exists to every gain `r<=k-1`: at each event, delete one irrelevant acquisition from every branch. Each event uses exactly `k` elementary edits and raises realized gain by exactly one.

Thus radius `k` is sufficient for an `r`-event strict-improvement route to gain `r`.

By contrast, under the elementary `rho=1` model, a neutral-permitting process can traverse the plateau and reaches gain `r` in the exact shortest path length `k r` from LRM1.

So the same finite sensing landscape has qualitatively different accessibility under:

```text
strict improvement + small coordinated radius
versus
neutral accumulation + elementary mutations.
```

The generic importance of neutral drift and mutation radius is established prior art. The exact thresholds here belong only to the declared routing representation.

## 3. Required-gap specialization

For the query-minimal star family in LRM2,

```text
k=q+1,
r=q.
```

Therefore

```text
rho_first=q+1,
```

while a direct one-event jump to the full required gap needs

```text
rho_direct=q(q+1).
```

A strict-improvement route with coordinated radius `q+1` exists in exactly `q` beneficial events, one gain level per event.

Hence the side-model reachability chain can distinguish three questions:

```text
1. Does a task capable of gap q exist?
2. Is there any one-event beneficial mutant under radius rho?
3. Can the full target gap q be reached in one mutation event?
```

For the exact query-minimal star family the corresponding answers are controlled by

```text
static task:      (2q+2,q+2,q+2,2),
first benefit:    rho >= q+1,
direct full gap:  rho >= q(q+1).
```

## 4. Relation to PAYOFF small-jump accessibility

The logical correspondence to PAYOFF's hard-cutoff result is now sharper:

```text
PAYOFF:
a globally better architecture may exist but a mutation jump smaller than a declared threshold cannot cross the accessibility interface.

local routing side model:
a globally better routing program may exist but an edit-radius smaller than k cannot produce even the first strictly beneficial one-event mutant.
```

These are **parallel results in different state spaces**. Do not equate

```text
delta_escape
```

with

```text
rho_first or rho_direct.
```

No shared units or source-derived map exists between those mutation geometries.

## 5. Claim ceiling

Do not claim novelty for mutation-radius thresholds, neutral drift, local optima, fitness plateaus, or coordinated program mutations in general.

The useful new role of LRM3 is internal to the adaptive-gain research program: it converts the earlier qualitative `small jump assumption` discussion into an explicit accessibility gate on the same finite sensing structure used by the current eco-evolutionary reachability theorem.

Any biological application must justify what one routing mutation can change and therefore what `rho` means mechanistically.

## 6. Executable audit

Implementation:

```text
adaptive_gain/local_routing_mutation_radius.py
```

Tests independently enumerate every direct deletion vector for small `k` and verify that direct gain `r` appears exactly at radius `k r`. They also verify the constructive radius-`k` strict-improvement path and the required-gap specialization.
