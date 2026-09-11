# Theoretical Ecology submission metadata v1

## Scientific metadata — FROZEN FOR FINALIZATION

**Title**

Finite sensing structure constrains eco-evolutionary feedback regimes

**Abstract**

Use the Abstract in `manuscript/MANUSCRIPT_V1.md` unchanged unless a portal character/word limit requires a formatting-only adjustment. Current internal count is approximately 190 words.

**Keywords**

- Adaptive information use
- Decision trees
- Evolutionary stasis
- Fluctuating selection
- Temporal autocorrelation

**Article type**

Research/theoretical article; confirm the exact portal label at upload.

**Main figures**

1. `manuscript/figures/figure1_state_space.svg`
2. `manuscript/figures/figure2_reachability.svg`
3. `manuscript/figures/figure3_extremal_envelope.svg`
4. `manuscript/figures/figure4_long_time_outcomes.svg`

Figure legends are controlled in `manuscript/FIGURE_LEGENDS_V1.md`.

**Supplement**

`manuscript/SUPPLEMENT_V1.md`

## Frozen reproducible baseline

Figure-inclusive release ref:

`release/theoretical-ecology-submission-with-figures-v1`

Commit:

`789d9ef993148258d22222b2c83e45164fbc09d3`

Tree:

`f565d90b6b3c4d7095af84b69b3ece322a61164c`

Post-merge CI:

`34500493463` — Python 3.10, 3.11, and 3.12 all passed full pytest plus both repository audit scripts.

The four SVGs are checksum-frozen and exactly reproducible through `manuscript/figures/generate_main_figures.py`; see `validation/theoretical_ecology_main_figures_v1.json`.

## Scientific claim hierarchy — DO NOT ALTER DURING METADATA ENTRY

1. principal reachability theorem: required local dynamical regime -> required structural gap -> minimum/Pareto-minimal finite sensing architecture;
2. supporting structural-temporal extremal envelope;
3. diagnostic model-compatible oscillation result;
4. mechanistic cancellation-versus-restoration proposition.

Do not use unqualified `minimum information` as the novelty claim. The manuscript concerns finite deterministic sensing/decision/separation structure, not a Shannon-information lower bound.

## Author-controlled title-page fields — UNRESOLVED

The following must be deliberately verified before final upload and are not inferred by this repository workflow:

- final author list and order;
- publication spelling/romanization of each author name;
- affiliation(s) current at submission;
- corresponding author;
- correspondence email/address;
- ORCID(s), if supplied;
- funding statement;
- competing-interests declaration;
- author-contribution statement.

See `manuscript/SUBMISSION_DECLARATIONS_V1.md`.

## Final-upload checklist

Before clicking submit:

- confirm portal article type;
- copy the exact title and abstract from the frozen manuscript;
- enter author-controlled metadata only from verified information;
- attach four main SVG figures in numerical order;
- attach the Supplement if requested as a separate file;
- use the controlled figure legends;
- verify reference rendering after conversion by the submission system;
- verify mathematical symbols after PDF conversion;
- record the exact submitted commit/tree and any permanent code archive DOI.
