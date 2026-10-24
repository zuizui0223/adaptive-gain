# Reproduce the exact future-wind-forecast results

Python 3.11+ standard library only. This package includes the original standalone
`stochastic_weather.py` and `deadline_mixture.py` from the previously verified
2026-10-23 32-world wind-deadline analysis, plus independent forecast code.
No network or ecological data access is needed; all quantities are synthetic.

```bash
python -m unittest -v test_wind_forecast
python run_analysis.py
```

Expected: `Ran 12 tests`, `OK`; output generated in `results/summary.json`,
`results/48_context_comparisons.csv`, and `results/SHA256_MANIFEST.json`.
A new independent exact Bayes posterior solver tests 36 combinations at d=2,
K=3/4 without the production's grouped-likelihood and baseline+hit shortcuts.
The full official GitHub reusable module is
`adaptive_gain/wind_forecast_routing.py` on analysis branch
`analysis/wind-next-step-forecast-20261024`, with a dedicated GitHub Actions
workflow that passed new and prior model tests.

All scientific interpretation and limits are in `RESULTS_JA_20261024.md`.