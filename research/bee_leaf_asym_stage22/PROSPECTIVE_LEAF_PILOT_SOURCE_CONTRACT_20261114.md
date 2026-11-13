# Stage22 prospective blinded leaf-channel pilot: machine-readable source contract

**No real pilot has been conducted.** This is an inspectable mock-only measurement schema intended to make future experimental requirements unambiguous.

For each actually tested animal and original trial, a valid future record would need original colony ID, bee ID, trial ID, source U/V label, hidden true leaf bit, actual subject-reported bit, cue-on time, report timestamp, and correctness-feedback timestamp, with video confirmation. The source must also verify that R was not shown, no alternative U/V source was available and no reward-position/odor cue was visible. Otherwise the record does not estimate isolated leaf recognition. One animal with many frames is **one repeated individual**, not many independent animals.

The 2×2 matrix for EACH U and V must be recovered:

| | Observed 0 | Observed 1 |
|---|---:|---:|
| Source true 0 | P(report0|true0) | P(report1|true0) |
| Source true 1 | P(report0|true1) | P(report1|true1) |

Source class frequencies must be known and uncertainty carried through to optimal-access gain, with colony-level clustering. A single pooled correct-answer proportion is NOT an adequate measure of these four conditional parameters. Since Stage22's hidden U has prior P(U1)=.2, an animal that always reports U0 could score 80% on naturally sampled trials while providing no useful discrimination. A fully randomized, class-balanced sensory pilot makes that failure visible; stimulus choice and learning must be separately audited in a real experiment.

Mock quality gate \`pilot_leaf_class_gate.py\` produces 80 entirely fabricated rows (two invented colonies × one invented bee each × two leaf sources × two true bits × ten), tests timestamps, leakage flags and original source identifiers, and emits only source-grain aggregates. It deliberately includes true-bit-specific asymmetry:

- Fictional colony 1: V0 recognition 100%, V1 recognition 90% → idealized gain .008.
- Fictional colony 2: V0 recognition 90%, V1 recognition 100% → idealized gain .002.

These are **injected mock classification outcomes**, not a real bee population comparison. In an actual pilot, never require exactly symmetric errors; rather, estimate every class-specific rate and interval, then use the correct four-channel model under independently measured q and query costs.

The theorem should not be promoted from “conditional model predicts value” to “bees benefit from selecting information” until actual animal-origin requests, target-choice accuracy and calibrated intake are recorded under a prospectively fixed causal comparison. A toy positive number is not a biological experiment.
