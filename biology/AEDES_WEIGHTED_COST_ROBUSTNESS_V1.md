# Aedes weighted-cost robustness v1

## Result

The prospective four-world Aedes task does **not** require equal cue costs to retain strict adaptive gain.

Let the frozen outcome matrix be

| World | R | A | B |
|---|---:|---:|---:|
| H0 | 0 | 0 | 0 |
| H1 | 0 | 1 | 0 |
| O0 | 1 | 0 | 0 |
| O1 | 1 | 0 | 1 |

with four distinct targets. Assign positive acquisition costs

- `r` to gonotrophic state cue `R`;
- `a` to host acidic cue `A`;
- `b` to oviposition odor cue `B`.

Then

`C_A = r + max(a,b)`

and

`C_F = r + a + b`.

Therefore

`g = C_F - C_A = min(a,b) > 0`.

## Why

Every fixed resolver must include all three queries:

- omit `R`: H0 and O0 remain indistinguishable;
- omit `A`: H0 and H1 remain indistinguishable;
- omit `B`: O0 and O1 remain indistinguishable.

Hence `C_F=r+a+b`.

An adaptive policy queries `R` first. In the host branch it then queries `A`; in the oviposition branch it queries `B`. Its worst path costs `r+max(a,b)`.

Starting with `A` or `B` cannot improve the worst case. One outcome leaves a three-world continuation that still requires both remaining distinctions along some path, so the resulting worst-case cost is `r+a+b`. Thus `R` is the unique optimal first query for all strictly positive costs.

## Executable audit

`adaptive_gain/aedes_gonotrophic_fixture.py` constructs both the unit-cost and weighted tasks and checks the formulas against the generic exact solver.

`tests/test_aedes_gonotrophic_fixture.py` exhaustively verifies the formula on the positive integer cost grid `r,a,b in {1,2,3,4}` and includes asymmetric stress cases.

## Biological consequence

The prospective empirical test does **not** need to justify that gonotrophic-state sensing, host-cue sensing and oviposition-cue sensing have equal physiological costs.

It still must:

1. define each acquisition cost prospectively;
2. make each cost positive under the declared scale;
3. justify that the quantities being counted are organism-level information acquisitions rather than arbitrary researcher-side labels;
4. freeze the cost convention before the outcome matrix is opened.

If costs are only ordinal or cannot be biologically operationalized, the unit-cost laboratory abstraction can still be reported as such, but it should not be interpreted as a measured energetic cost.

## Scope

This is a robustness property of one predeclared four-world task, not a new general weighted adaptive-gain theorem and not a novelty claim.