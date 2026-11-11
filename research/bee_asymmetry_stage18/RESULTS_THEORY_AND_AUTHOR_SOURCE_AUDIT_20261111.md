# Stage18 Results: Distinguishing conditional routing from conditional stopping

**Math proven and code-verified 2026-11-11; ZERO live bees tested.**

Stage17's fully symmetric R,U,V task does not produce a branch-content-dependent stopping decision: after either observed R result, querying the appropriate leaf has the same information value. The Stage18 asymmetric U prior gives a direct positive mathematical instance of root-dependent stopping.

| Model | q | normalized cost c | Root0 optimal | Root1 optimal | Contingent optional net | Precommit optional net | Difference |
|---|---:|---:|---|---|---:|---:|---:|
| Asymmetric low cost | .2 | .10 | Request U | Request V | .900 | .850 | +.050 |
| **Asymmetric intermediate cost** | **.2** | **.25** | **SKIP** | **Request V** | **.775** | **.650** | **+.125** |
| Asymmetric very costly | .2 | .50 | SKIP | SKIP | .650 | .650 | 0 |
| Symmetric original | .5 | .25 | Request U | Request V | .750 | .625 | +.125 |

The sharp maximum of the asymmetry family is 1/8 at c=1/4 when q<=1/4; for q>=1/4 it is (q+1/2)/6 at c=(q+1/2)/3. Thus q=.2 produces root-conditioned stopping but a smaller maximum benefit (.125) than symmetric q=.5 (1/6).

**Decomposition at q=.2,c=.25:** mandatory-first access advantage +.100 normalized reward units; allowing first-request SKIP increases the advantage by +.025 to +.125. This is a change in the model choice set, NOT an experimentally measured cognitive process. The extra SKIP increment is not universally positive across costs.

**Evidence:** [Stage18 dedicated workflow #42967801326](https://github.com/zuizui0223/adaptive-gain/actions/runs/42967801326), 13 source-free/verification tests, including an independently written posterior dynamic program covering 8-world states; read-only provenance-matched original author bee information-request CSV source audit. A source-validation output is not a new effect estimate. The source author's 192/192 easy-vs-hard and 181/192 strictly monotone source trends are PRIOR AUTHOR data, with no colony IDs in this CSV and no root-contingent choice between distinct U/V cue channels.

**Scientific gate:** Do not add root-dependent U priors to the frozen Stage17 design without a separately registered alternative, calibrated individual learning of these priors, source-verified voluntary SKIP/U/V acts and full original reward/latency telemetry. No biological proof or calibrated leaf cost exists yet.
