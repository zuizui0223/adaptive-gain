# Aedes target-partition sensitivity v1

## Why this audit is necessary

The prospective Aedes four-world outcome matrix can support a robust positive structural gap only if the target actions are declared at the biologically appropriate resolution **before** the finite-task solver is run.

The cue matrix alone does not determine the target partition.

## Same cue matrix, two target semantics

The frozen cue outcomes are

| World | gonotrophic state R | host cue A | oviposition cue B |
|---|---:|---:|---:|
| H0 | 0 | 0 | 0 |
| H1 | 0 | 1 | 0 |
| O0 | 1 | 0 | 0 |
| O1 | 1 | 0 | 1 |

### Four ecological actions

Declare

- H0 = continue host search;
- H1 = approach / accept host;
- O0 = continue oviposition-site search;
- O1 = accept site / oviposit.

These are four distinct behavioral programs. For positive costs `(r,a,b)`:

`C_A = r + max(a,b)`

`C_F = r + a + b`

`g = min(a,b) > 0`.

The state cue is mandatory for the fixed resolver because H0 and O0 have identical terminal-cue outcomes but require different search programs.

### Coarsened accept/reject actions

If the same worlds are instead collapsed to

- H0, O0 = generic reject;
- H1, O1 = generic accept,

then the fixed strategy can ignore gonotrophic state and use only `A+B`:

`C_F = a+b`.

The adaptive optimum is

`C_A = min(a+b, r+max(a,b))`,

so

`g = max(0, min(a,b)-r)`.

Under equal unit costs, this gives

`C_A=C_F=2`, `g=0`.

Thus a unit-cost positive gap disappears if the behavioral targets are only generic accept/reject.

## Biological admission rule

The four-target version is licensed only if the experiment independently establishes that the no-cue and positive-cue responses belong to distinct gonotrophic behavioral programs, rather than being researcher-renamed copies of a common binary action.

Acceptable evidence should be specified prospectively and may include:

- distinct action sequences (host-search continuation versus oviposition-search continuation; host approach/blood-feeding versus site acceptance/egg laying);
- different downstream motor programs or behavioral endpoints;
- a predeclared ecological utility/action ontology independent of the cue matrix.

The target ontology must not be chosen because the four-target encoding yields `g>0`.

## Falsification rule

If the empirically defensible target space is only generic accept/reject, record the coarsened task as the canonical result. Under unit costs that is an `ADMITTED_ZERO_GAP` result.

Do not rescue a zero-gap result by relabeling state-specific copies of the same behavior after inspecting the solver output.

## Executable audit

`adaptive_gain/aedes_gonotrophic_fixture.py` contains both target partitions.

`tests/test_aedes_gonotrophic_fixture.py` verifies:

- robust positive gap for the four-action partition;
- exact collapse to `g=0` for the unit-cost generic accept/reject partition;
- the weighted coarsened formula `g=max(0,min(a,b)-r)` over a finite positive-cost grid.

## Interpretation

This sensitivity is a feature, not an inconvenience. It identifies exactly which biological claim must be measured before the Aedes candidate can count as a positive adaptive-gain realization:

> gonotrophic context must change the target decision program, not merely the label attached to a common binary response.