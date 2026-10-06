# Chandel Figure 3a value-of-time sensitivity

Status: public-data descriptive process result. This is **not** a fitness estimate and not an empirical adaptive-gain receipt.

## Why this analysis

The first Phase A analysis showed that +IR host-seeking activity persists after each CO2 pulse. The opportunity-fitness theory makes a stronger process prediction:

> the ecological value of a cue effect depends on **when through time** that effect occurs.

Figure 3a is suitable for a first descriptive test because it provides the full 3000-frame aggregate mean IHSI trajectory.

## Main result — the IR advantage is late-weighted

For the first 90-s post-pulse interval, the signed IR-minus-no-IR advantage has half of its total area only after

[
\boxed{46.2\ {m s}}
]

after CO2 cessation.

For the second post-pulse interval, the corresponding half-area time is

[
\boxed{46.5\ {m s}}.
]

The positive-advantage temporal centroids are similarly late:

[
47.5\ {m s}
]

after the first pulse and

[
45.8\ {m s}
]

after the second.

So the public data do not show merely an immediate increase that then decays. Much of the +IR contrast is expressed tens of seconds after the transient CO2 cue has ended.

## How much advantage appears early?

### First post-pulse interval

Cumulative fraction of total signed IR advantage:

- first 10 s: **3.37%**;
- first 30 s: **25.58%**;
- first 45 s: **48.46%**;
- first 60 s: **67.29%**;
- first 75 s: **84.65%**.

### Second post-pulse interval

- first 10 s: **6.25%**;
- first 30 s: **28.21%**;
- first 45 s: **48.04%**;
- first 60 s: **68.42%**;
- first 75 s: **88.85%**.

Thus a short ecological opportunity window would miss most of the aggregate behavioral advantage that appears in the full 90-s post-pulse interval.

## Value-of-time kernel sensitivity

As a descriptive sensitivity analysis, weight the post-pulse IR-minus-no-IR trajectory by

[
w_	au(t)=e^{-t/	au}
]

and normalize the weights within the 90-s interval.

This is **not** a fitted natural opportunity distribution. It asks how strongly the same observed behavioral trajectory would count under different time-value scales.

### First post-pulse interval

Unweighted mean contrast:

[
27.72.
]

Exponentially weighted mean contrast:

| value timescale (	au) | weighted IR-no-IR contrast |
| ---: | ---: |
| 5 s | 10.39 |
| 10 s | 15.40 |
| 20 s | 21.17 |
| 30 s | 23.67 |
| 60 s | 26.03 |
| 120 s | 26.99 |

### Second post-pulse interval

Unweighted mean contrast:

[
56.07.
]

| value timescale (	au) | weighted IR-no-IR contrast |
| ---: | ---: |
| 5 s | 34.29 |
| 10 s | 39.71 |
| 20 s | 47.37 |
| 30 s | 50.91 |
| 60 s | 54.21 |
| 120 s | 55.39 |

## Biological interpretation

This is the first real-data demonstration of the process distinction motivating the new theory:

[
oxed{
	ext{magnitude of a cue effect}

eq
	ext{ecological value of that cue effect}.
}
]

The same +IR behavioral effect can contribute very differently depending on whether the relevant ecological opportunity decays over roughly 5 s, 30 s, or 120 s.

For this dataset the reason is clear: the +IR contrast is strongly expressed at later post-pulse times.

This does **not** imply that IR has low fitness value under natural host seeking. The natural value-of-time kernel has not been measured here.

The result instead shows why the kernel is an empirically necessary object.

## Relation to the fitness-process spine

The theory writes a generic performance contrast as

[
Delta R
=
int Delta P(t)m(t)dt,
]

where

- (Delta P(t)) is the architecture- or cue-dependent performance difference through time;
- (m(t)) is the ecological marginal value of earlier completion/activity.

Figure 3a supplies a population-level (Delta P(t))-like object.

It does not supply (m(t)).

Therefore the present result closes only one side of the overlap mechanism.

## Claim ceiling

Do not interpret this analysis as evidence for:

- individual completion-time distributions;
- an adaptive versus fixed sensing architecture;
- a natural host-defense deadline;
- a selection coefficient;
- direct reproductive fitness.

The result is a **temporal localization receipt**: it demonstrates with public data that a biologically important multisensory cue effect has a strongly nonuniform distribution through time, so scalar effect size alone cannot determine its ecological value.

## Next gate

The clean next empirical target is one of:

1. a natural or experimentally manipulated opportunity-duration distribution (B);
2. individual-level host-seeking/probing completion curves from reprocessed raw video;
3. both, allowing direct estimation of (P(Tle B)).

The frame-preserving tracker added on this branch is intended for gate 2.
