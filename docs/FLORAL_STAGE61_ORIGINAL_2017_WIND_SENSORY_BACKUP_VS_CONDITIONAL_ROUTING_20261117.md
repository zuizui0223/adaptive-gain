# Stage61 | Prior-art experimental reality check: original 2017 wind × floral odour × visual backup versus conditional sensory routing

Status: 2026-11-17 JST. **Existing published bee experiment independently sourced, elementary factorial identifiability calculated, 72-bee descriptive refit implemented. No new pollinator or plant fitness observations, and no new cue-order effect identified.**

## Publication originality firewall: do not relabel existing backup as a new principle

- Lawson, Whitney & Rands 2017 `10.1098/rsos.170996`, publicly available original data `10.5061/dryad.3g591`; Europe PMC OA `PMC5717666`.
- Original 2017 source-specific CI [44012132525](https://github.com/zuizui0223/adaptive-gain/actions/runs/44012132525) **SUCCESS**. Original `rsos170996supp2.xlsx` inner SHA256 `b3802f57516c0ebac025f363dd2943796e749ef82b9b32e15fd0deb78c98432c`, 17,470 original source bytes, paper supplement 10 original archive members; 4 workbook tabs.
- Original `2. Wind Simulation Data` sheet source range `A1:G73` = **one heading row + 72 independent individual bee rows** from four groups **18 bees each**. Columns: `condition`, `group`, `flower visits taken to reach learning criteria`, `number of correct choices made after landing`, `lands on rewarding flowers`, `colony`, `scent of rewarding flowers`. Other workbook tabs: `Chemical Interference Data` also `A1:G73`, `Scent Preference Data` `A1:D16`, and Contents. Source data has no time-ordered early and late cue queries or recorded pollen deposits.
- Published result is known: wind/chemical noise impaired odour-only learning performance, with colour backup improving foraging performance. This is original 2017 science, **not a Stage61 discovery**.
- Graver et al. 2026 `10.1242/jeb.251126` additionally show spatial-scale/timing-dependent weighting of learned colour/odor under flying Bombus. We cannot claim any use of cue sequence or sensory integration is itself new.

## True original 2017 wind design: **four** observed arms of eight possible

Represent experiments by `(W,O,V)`, 0=absent/low and 1=present/high:

| Published 2017 wind arm | W | Odour | Visual | Individual bees |
|---|---:|---:|---:|---:|
| A: no wind, scented-only flowers | 0 | 1 | 0 | 18 |
| B: windy scented-only flowers | 1 | 1 | 0 | 18 |
| C: windy scented-and-coloured flowers | 1 | 1 | 1 | 18 |
| D: windy coloured-only flowers | 1 | 0 | 1 | 18 |

The four missing arms are `(0,0,0), (0,0,1), (0,1,1), (1,0,0)`. Existing original four arms allow **only three observed intervention-edge contrasts** (subject to paper design/colony assumptions): `B-A`: wind effect with odour only; `C-B`: added visual cue under wind+odour; `C-D`: added odour under windy visual flowers. Without no-wind dual-colour+odour `(0,1,1)`, **wind × visual** interaction with odour fixed is not identified. The three-way `W×O×V` and **cue-order-driven information routing** are also not identified.

### Exact design counterexample, explicitly hypothetical and NOT original bee outcomes

To make missing-arm no-go executable, set **assumed** four rates A=3/5, B=2/5, C=7/10, D=13/20. Fill four unobserved cells with arbitrary rates in [0,1]. Existing `exact_2017_factorial_identifiability.py` exhaustively checks all 16 corner completions using exact `Fraction`, with identical observed A/B/C/D but opposite signs:

- `W×V | O=1` contrast can range **−1/10 to +9/10** (sign not identified);
- `W×O×V` additive 3-way can range **−7/4 to +9/4** (sign not identified).
- This is simple linear/experimental-design arithmetic, **not** a biological causal result and not a novel theorem; the assumed values are not measured in the original 2017 experiment. When real published endpoints are unbounded count outcomes, these toy probability intervals must NOT be transferred to source rates or count effects.

Source-opened original workbook supports a separate **four-arm descriptive reanalysis only**. `refit_2017_wind_bees_group_outcomes.py` now authenticates the inner DOCX? **No**: source **XLSX** identity, reads the 72 wind-sheet individuals, validates all four group sizes, original colony IDs, authored counts, source missingness, and produces existing-treatment per-group means and medians **without independent-colony causal tests or invented cue-order effects**. Only summary receipts are committed; original raw rows remain in ephemeral workflow memory.

## What the inherited adaptive-gain theory does and does not add

The existing finite deterministic structure in `adaptive_gain.extremal_routing_family.extremal_routing_task(2)` provides exact `C_A = r + max(v,o)`, `C_F=r+v+o` in a **constructed four-world** target game with two branch-specific terminal cues and an early branch router carrying no direct target information. Under an abstract budget (B), adaptive-only resolution is possible when `C_A<=B<C_F`. Stage58 confirmed this source-free exact cost formula for 64 integer cost triples and simulated hypothetical missing early-cue availability.

**No original 2017 bee was measured to follow that four-world route**, and the 2017 treatment data do not measure target-equivalent/branch condition or cue query sequence. The existing theorem's guaranteed error-free target resolution does **not** transfer directly to noisy real smell/vision without an explicit likelihood, decision loss and a measured observation-cost calibration. Original Crall wind-bait and Chang landing source velocities cannot be substituted as those costs or multiply into wild plant pollen benefit.

## What novel causal test would be needed instead

The claim capable of going beyond existing 2017 backup and 2026 scale-dependent cue-weighting is a **causally observed conditional next-cue policy**: first sensory/environmental cue has limited or zero *direct* information about which flower is rewarded, but conveys which subsequent visual versus scent information is useful. Under matched cue strengths, cost/effort and environment, an animal randomizes what to inspect next and thereby improves terminal task performance/plant pollen delivery over best **static modality mixture** and pure backup.

Experiment must separately manipulate (i) coarse route cue identity or order while holding direct reward information constant, (ii) late odour cue present/absent and visible guide present/absent, (iii) controlled wind strength/direction/plume/sway and irradiance/background, (iv) rewarding branch/reward timing, in a source-independent colony randomized/balanced design. Preregister trial opportunities and route-action choices, actual cue exposure time, worker and colony ID, stage D=discovery, L=landing conditional on discovery, T=pollen deposition conditional on landing, before claims of adaptive receiver payoff or plant fitness. For added ecological novelty, test across independent bee, fly, butterfly/other relevant receiver groups, *not* hard-code generic Bombus preference.

A proposed statistical model `choice_or_delay ~ early-cue × late-cue × wind/light + sensory intensity + branch × site + colony/bee` requires the actual within-individual trials; a species-level UV/VOC macro registry alone (Stage59 VOC×817 visual only 15 accepted-name overlaps, Stage60 FCP visible-photo 80 candidate taxa) cannot identify any of these conditional interaction effects.

## Next evidence gate / stop rule

Only after source-authenticated 72-bee aggregate refit (new original-data workflow) and independent QA can source means be reported; do not use existing 2017 behavioural effects as a new ecological discovery or claim a sign-identified full factorial wind×scent×vision effect. Stage61 remains Draft, `main` unchanged.
