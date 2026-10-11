# Chandel Figure 3a Phase A result

Status: public-data descriptive result. This is a timing-process anchor, not an empirical adaptive-gain or fitness result.

## Source recovered

The one-off GitHub Actions fetch succeeded and retrieved the Nature Source Data Figure 3 workbook directly from Springer Nature.

Frozen workbook:

- DOI: `10.1038/s41586-024-07848-5`;
- sheet: `Figure 3a`;
- 3,000 frames;
- 10 FPS;
- 300 s;
- SHA-256: `75b2f22b1b5c83f1cf5f855a9f682de5965300d7db46db5c221cc5dcc4d880c5`.

The sheet contains the published aggregate mean instantaneous host-seeking activity for the no-IR and IR zones across the 18 trials described in the paper.

## Pulse schedule

The manuscript states that Figure 3a used two 30-s CO2 pulses.

The public controller `Arduino_CO2_Release/PushbottonCO2_LongPulse.ino` implements exactly a 300-s sequence:

```text
0-60 s     CO2 off
60-90 s    CO2 on
90-180 s   CO2 off
180-210 s  CO2 on
210-300 s  CO2 off
```

This schedule also matches the two response rises in the source time series.

## Descriptive epoch means

| Epoch | No IR | IR | IR - no IR | IR / no IR |
| --- | ---: | ---: | ---: | ---: |
| 0-60 s, pre-pulse | 7.42 | 10.51 | +3.09 | 1.42 |
| 60-90 s, pulse 1 | 25.47 | 32.51 | +7.04 | 1.28 |
| 90-180 s, post 1 | 24.34 | 52.06 | +27.72 | 2.14 |
| 180-210 s, pulse 2 | 33.62 | 59.87 | +26.25 | 1.78 |
| 210-300 s, post 2 | 32.45 | 88.53 | +56.07 | 2.73 |

The most important feature is therefore not simply greater activity in the IR zone. The IR contrast expands after CO2 removal.

## Pulse versus post-pulse persistence

For the no-IR zone:

[
rac{	ext{post 1 mean}}{	ext{pulse 1 mean}}
=
0.956
]

and

[
rac{	ext{post 2 mean}}{	ext{pulse 2 mean}}
=
0.965.
]

The post-pulse activity is therefore approximately the same as the activity during the preceding pulse.

For the IR zone:

[
rac{	ext{post 1 mean}}{	ext{pulse 1 mean}}
=
1.601
]

and

[
rac{	ext{post 2 mean}}{	ext{pulse 2 mean}}
=
1.479.
]

Thus mean host-seeking activity is actually higher over each post-pulse interval than during the corresponding CO2 pulse.

This is consistent with the paper's qualitative statement that IR sustains host seeking after CO2 cessation.

## Smoothed peak timing

Using a centered 5-s moving average:

### First post-pulse interval

No IR:

[
t_{m peak}=96.6 {m s},
]

or 6.6 s after CO2 cessation.

IR:

[
t_{m peak}=111.0 {m s},
]

or 21.0 s after cessation.

### Second post-pulse interval

No IR:

[
t_{m peak}=215.3 {m s},
]

or 5.3 s after cessation.

IR:

[
t_{m peak}=243.8 {m s},
]

or 33.8 s after cessation.

The IR-zone response is therefore not just larger. Its aggregate peak is displaced substantially later into the post-pulse period.

## Repeated-pulse amplification

The second versus first pulse mean ratio is:

[
1.32
]

for no IR and

[
1.84
]

for IR.

For the post-pulse periods the ratio is:

[
1.33
]

for no IR and

[
1.70
]

for IR.

The source data therefore contain both persistence after transient CO2 stimulation and stronger response after repeated stimulation.

## Process interpretation

This result changes how the new opportunity-fitness theory should be empirically framed.

A single scalar such as mean decision time would miss the observed effect because the cue combination changes the **shape through time** of behavioral availability.

The appropriate process object is a temporal performance curve

[
F_j(t)
quad	ext{or more generally}quad
P_j(t),
]

weighted by the ecological value of being active or completing the focal action at each time.

This is exactly the logic of the proposed overlap kernel:

[
Delta R
=
int
Delta P(t),m(t),dt.
]

For Figure 3a, the public workbook supplies a population-level (Delta P(t))-like behavioral response profile. It does not supply an individual completion-time CDF.

## What this result does not show

Figure 3a alone does not identify:

- individual first-entry or decision-completion latencies;
- variance among the 18 trials at each frame;
- an adaptive versus fixed sensing architecture;
- the correct evolutionary comparator;
- the ecological value-of-time kernel;
- direct fitness consequences.

The result is therefore an empirical **process-shape anchor**, not closure of the fitness theory.

## Next empirical gate

The strongest next use of the Chandel archive is raw-video reprocessing of a frozen subset to obtain individual or track-level event-time distributions while correcting the public tracking-code issues already registered in `CHANDEL_TRACKING_CODE_AUDIT_V1.md`.

That would move the empirical object from aggregate IHSI trajectory to an actual completion/event-time distribution.
