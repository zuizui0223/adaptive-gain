# Main figures for the Theoretical Ecology manuscript

This directory contains the four main-text figures specified by `manuscript/FIGURE_PLAN_V1.md`. The committed SVG files are generated deterministically by `generate_main_figures.py`.

## Files

- `figure1_state_space.svg` — the same ecological states index contingent sensing reward and temporal recurrence.
- `figure2_reachability.svg` — principal reverse reachability result, binary exact corner, bounded-arity Pareto trade-off, and arity asymmetry.
- `figure3_extremal_envelope.svg` — structural-temporal extremal ceiling and the two exact sources of slack.
- `figure4_long_time_outcomes.svg` — directional accumulation, neutral cancellation, monotone restoration, and model-compatible oscillatory restoration.
- `generate_main_figures.py` — standard-library-only SVG generator with assertions for all plotted numerical fixtures.

## Regeneration

From the repository root:

```bash
python manuscript/figures/generate_main_figures.py
```

No third-party plotting package is required. The script writes the four SVGs next to itself. The numerical fixtures and committed SVG checksums are frozen in `validation/theoretical_ecology_main_figures_v1.json`.

PNG previews were rendered only for visual QA and are not part of the committed submission surface. Figure generation changes no theorem, formula, model domain, or manuscript prose.
