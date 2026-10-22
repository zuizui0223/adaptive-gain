# Reproduce the exploratory wind route-composition/speed decomposition

Source: Burnett, Badger & Combes (2022), Dryad DOI [10.25338/B8Z34Q](https://doi.org/10.25338/B8Z34Q). Original `Bee_route_choice_in_wind.csv` SHA256 `2361dccb523b97f1e5e542fc492d302a5e7c290cdde72eb2dfb2ce021153d6f7`, 548 flights, 58 bees. The original experiment randomized obstacle height between bees and initially assigned wind within bees. No ecological species-to-species interactions or adaptive cue queries are measured.

Run from a checkout of `analysis/wind-route-benefit-decomposition-20261022`:

```bash
python -m pip install 'numpy==2.3.5' 'pandas==2.2.3'
python research/wind_route_experiment/source_gate.py
cd research/wind_route_experiment
python -m unittest -v test_route_cost_decomposition
cd ../..
python research/wind_route_experiment/route_cost_decomposition.py \
  --source wind_route_original/Bee_route_choice_in_wind.csv \
  --out wind_route_components_results --reps 9999
python research/wind_route_experiment/independent_route_cost_audit.py \
  --source wind_route_original/Bee_route_choice_in_wind.csv \
  --summary wind_route_components_results/summary.json \
  --out wind_route_components_results/independent_audit.json
```

Verified in isolated [GitHub Actions 39770112060](https://github.com/zuizui0223/adaptive-gain/actions/runs/39770112060): source SHA256 matched, **7/7 new tests passed**, 9,999 whole-bee bootstrap draws and separate raw-row audit succeeded. The inherited route/field local tests also passed (total **16/16**) when the original Balfour field CSVs were present. These are focused tests only: unrelated repository-wide CI has not been declared green.

Primary descriptive decomposition: high obstacles **98 and 127mm** (11+10 = 21 bees). Equal-wind-per-bee and equal-obstacle-stratum weighting. `Δμ=route composition C+within-observed-route P` exactly; wind changes are **0.043999 m/s = −0.006129 m/s + 0.050129 m/s**. Percentile 95% bee-cluster intervals: total [−0.01529, 0.10994], C [−0.01300, 0.00544], P [−0.00926, 0.11153], each containing zero. Within-dataset sensitivity with 69mm adds 11 bees but wind-within-obstacle route has only three films. Whole-bee leave-one-out changes main C only between −0.00773 and −0.00356 but does not establish a general population direction.

**Causal warning:** `route` is a post-wind outcome and individual bee route selection can affect which speeds enter each conditional group. C and P are an **algebraic partition** with no identified natural direct/indirect causal effects. Do not infer accessible plant resources, predators/competitors, information access order, fitness, or `C_A<C_F`. The choice of 98/127mm as well-supported routes was after reviewing source support, so this is exploratory, not prospectively confirmatory.

This work is a new quantitative decomposition of already published data, not a new independent field experiment or universal ecological law.
