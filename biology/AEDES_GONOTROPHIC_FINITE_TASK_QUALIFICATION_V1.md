# Aedes gonotrophic finite-task qualification v1

## Purpose

This note screens a biological route for issue #27: the reproductive-state switch in female *Aedes aegypti* from host seeking before a blood meal to suppressed host seeking and oviposition-site assessment after blood feeding.

Unlike the C. elegans SRI-36 control, this system naturally points to **different environmental distinctions in different physiological branches**. It is therefore the strongest prospective candidate identified so far for a positive finite adaptive/fixed gap.

This is a qualification/prospectus only. No empirical adaptive-gain value is claimed from the published literature.

## Biological anchors

### Gonotrophic state switch

Female *Aedes aegypti* strongly seek human hosts before blood feeding. Host attraction is suppressed for days after a blood meal while eggs develop. NPY-like receptor 7 (`npylr7`) is required for normal long-term host-seeking suppression: CRISPR-Cas9 null mutants show defective behavioral suppression. Selective NPYLR7 agonists suppress human attraction and biting.

Recent work further identifies `npylr7`-expressing rectal-pad cells that respond to RYamide and amino acids and participate in post-blood-meal reproductive physiology. This strengthens the evidence that internal nutritional/reproductive state is coupled to the behavioral switch, although NPYLR7 is not a clean branch-local switch because it also affects oocyte provisioning.

### Host branch terminal channel

The IR8a ionotropic-receptor pathway is required for normal detection of acidic human-odor volatiles. CRISPR disruption of `Ir8a` eliminates attraction to lactic acid and responses to acidic odorants and reduces attraction to humans/human odor. CO2/Gr3 interacts with this pathway; host detection is therefore a multi-cue system rather than a single-receptor channel.

Host-cue gating across the gonotrophic cycle is biologically plausible rather than merely behavioral. Classic electrophysiological work reports a reversible post-blood-meal reduction in sensitivity of lactic-acid-sensitive afferents that parallels temporary host-seeking suppression.

### Oviposition branch terminal channel — primary candidate: humidity / Ir68a

The strongest current branch-B candidate is **water-vapor / humidity sensing by Ir68a-dependent Moist Cells**.

Recent functional dissection shows:

- `Ir40a` supports Dry Cells and `Ir68a` supports Moist Cells;
- Dry and Moist Cells contribute redundantly to blood feeding;
- gravid females rely specifically on `Ir68a`-dependent Moist Cells to seek water-filled oviposition containers;
- `Ir68a` mutants are profoundly defective in locating water-filled containers, often depositing no eggs in the search assay;
- when placed directly next to water, the same mutants lay eggs normally.

This separates **site-finding information** from egg-production or egg-laying ability and gives a cleaner terminal behavioral requirement than broad olfactory co-receptor disruption.

Humidity is not literally absent from the host branch: Moist Cells can contribute redundantly to blood feeding. The relevant adaptive-gain claim is therefore narrower. `B` need only be required for the declared gravid-branch target distinction under the frozen task; it need not be an anatomically exclusive sensor that is never used elsewhere.

Gravid females also show strong state-dependent humidity seeking on the days when they search for oviposition sites, providing an independent behavioral link between gonotrophic state and the value of this information source.

### Secondary oviposition candidate: geosmin / Orco

Geosmin attracts gravid females to oviposition sites, and the preference is lost in `Orco` mutants. It remains a useful secondary candidate or replication cue. However, current evidence is weaker for gonotrophic-state-specific peripheral gating of this exact odor channel. More generally, some oviposition-odor-sensitive afferents show similar peripheral sensitivity in gravid and nongravid females. Therefore **behavioral switching must not be equated with state-dependent cue acquisition**.

## Candidate q=1 finite task

The cleanest prospective task uses two physiological branches and one environmental distinction within each branch.

Declare three organism-level information sources:

- `R`: gonotrophic/reproductive state, pre-blood host-seeking versus gravid/oviposition state;
- `A`: host-associated acidic-cue channel, operationalized prospectively by an IR8a-dependent lactic-acid/host-odor distinction under a fixed background;
- `B`: oviposition-site cue, with **Ir68a-dependent water-vapor/humidity sensing as the primary candidate** and an independently validated chemical cue such as geosmin as a secondary option.

A minimal frozen laboratory task would contain:

| World | R | A | B | predeclared target |
|---|---:|---:|---:|---|
| H0 | 0 | 0 | 0 | continue host search |
| H1 | 0 | 1 | 0 | approach/accept host |
| O0 | 1 | 0 | 0 | continue oviposition-site search |
| O1 | 1 | 0 | 1 | accept site / oviposit |

The off-branch terminal stimulus is held at a preregistered baseline in the laboratory task rather than retrospectively coded as irrelevant.

For this exact matrix with four distinct targets:

- adaptive policy: query `R`, then `A` if `R=0` or `B` if `R=1`;
- fixed policy: all three information sources are required;
- with positive acquisition costs `(r,a,b)`, the exact solver gives

`C_A = r + max(a,b)`

`C_F = r + a + b`

`g = min(a,b) > 0`.

Equal physiological costs are therefore not required. The costs must still be defined prospectively and have defensible organism-level semantics.

This is a predeclared testable witness, not a claim that published mosquitoes already instantiate the task.

## Why this is stronger than the C. elegans SRI-36 control

The SRI-36 result changes the receptor/neuron implementation of the **same diacetyl distinction** across state. Under the natural context-by-diacetyl task, that gives no automatic extra finite cue and therefore no positive gap.

The mosquito candidate instead uses:

- a host-associated acidic-odor distinction in the pre-blood branch;
- a water/oviposition-site distinction in the gravid branch.

Thus the two terminal queries have different ecological jobs rather than being two molecular implementations of one environmental variable.

## Issue #27 G1-G7 ledger

| Gate | Status | Current interpretation |
|---|---|---|
| G1 — declared ecological/internal contexts | **strong** | Pre-blood host-seeking and post-blood/gravid states are experimentally defined and behaviorally distinct. |
| G2 — context-dependent downstream modules | **strong/partial** | Host-cue responsiveness is suppressed after blood feeding; lactic-acid-sensitive peripheral afferents can be reversibly down-regulated; gravid females develop a strong oviposition-site/humidity-seeking program. Yet `Ir68a` Moist Cells also contribute redundantly to blood feeding, and complete state-specific acquisition of A versus B has not been shown. |
| G3 — heritable regulatory substrate | **strong/partial** | CRISPR-accessible `npylr7`, `Ir8a`, `Ir68a`, `Ir40a`, `Ir93a`, `Orco`, and `Gr3` loci provide causal handles. The full state-to-channel routing map is not one known branch-local cis-regulatory switch. |
| G4 — mutation locality | **partial** | Defined null alleles exist, but natural one-step mutational transitions among complete sensory policies are not known. Experimental knockouts are not automatically natural mutation edges. |
| G5 — pleiotropy / coupling audit | **partial** | NPYLR7 affects reproductive physiology; Ir8a belongs to an integrated host-cue system; Ir68a contributes to humidity-dependent blood feeding as well as oviposition-site seeking; broad co-receptors affect many channels. These changes must be encoded as coupled moves unless cross-context assays demonstrate locality. |
| G6 — proposal bias / neutral mutation measure | **not qualified** | Relative natural proposal rates and a neutral stationary measure over sensory-policy genotypes are unavailable. Stationary population claims remain prohibited. |
| G7 — phenotype map | **strong at component level; coherent task unmeasured** | Ir8a loss alters acidic-odor/human attraction; Ir68a loss profoundly disrupts locating water-filled oviposition containers while sparing egg laying when placed at the site; NPYLR7 loss disrupts host-seeking suppression. The complete frozen four-world `C_A,C_F` matrix has not been measured in one prospective experiment. |

Overall status: **partial representation with the strongest prospective positive-gap task screened so far**.

## Target ontology gate

The four-target interpretation has independent biological support: host seeking and gravid oviposition-site search are distinct gonotrophic behavioral programs with different sensory ecology, temporal organization and terminal motor actions.

Nevertheless this remains an empirical admission gate. If H0 and O0 cannot be operationally distinguished as different search programs in the prospective assay, the task must be coarsened to generic accept/reject targets. The executable control then gives, for costs `(r,a,b)`,

`g = max(0, min(a,b) - r)`,

and therefore unit costs give `g=0`.

The target ontology may not be chosen after viewing the solver result.

## Main hard stops before calling a positive gap biological

### 1. `R` must be an organismal information source with declared cost

Gonotrophic state cannot be inserted as a free abstract label. The experiment must define what physiological signal makes that state available to the decision system and what acquisition cost means. NPYLR7 is a mechanistic candidate, not automatically the query itself.

### 2. Both terminal channels must be measured in both branches

The task must assay host-cue and oviposition-site-cue responses in pre-blood and gravid mosquitoes. If both channels remain equally sampled in both states and only downstream motor output changes, the interpretation becomes context-dependent action selection rather than demonstrated contingent sensory acquisition.

Importantly, branch specificity means **required for the branch-specific target distinction**, not necessarily anatomically silent in the other branch. Ir68a illustrates why this distinction matters.

### 3. Off-branch baselines must be prospective

For the four-world star, the unused terminal stimulus is experimentally clamped to baseline in the opposite branch. That domain restriction must be frozen before computing the gap and reported explicitly; it is not evidence that the organism never senses the cue outside that branch.

### 4. Query costs need biological operationalization

Equal costs are not mathematically required. Candidate cost definitions include standardized sampling episodes, time, neural/energetic activation, or an explicitly declared laboratory resource scale. Whatever convention is chosen must be fixed before the outcome matrix is opened.

### 5. Genetic perturbations must be audited across both behavioral branches

Every `npylr7`, `Ir8a`, `Ir68a`, `Ir40a`, `Ir93a`, `Orco`, or downstream regulatory perturbation used as a policy edge must be tested for host seeking, oviposition-site search, locomotion, reproductive state and both terminal sensory responses. Broad co-receptor or endocrine perturbations should be encoded as coupled moves.

## Prospective experiment

### Freeze

Before collecting the full matrix, preregister:

1. age, mating state and blood-meal timing;
2. physiological criterion for `R=0/1`;
3. exact host-cue stimulus and background for `A`;
4. exact oviposition-site stimulus for `B` — primary design: humidity/water-vapor gradient;
5. four target actions and scoring thresholds;
6. cue-acquisition cost convention;
7. off-branch baseline stimuli;
8. exclusion/failure criteria.

### Measure

For each world and genotype:

- internal-state marker / behavioral state;
- peripheral/neural response to `A`;
- peripheral/neural response to `B`;
- host-search / host-approach output;
- oviposition-site-search / site-acceptance output.

For the primary B candidate, separately distinguish site finding from egg-laying ability, following the logic of the published Ir68a container-seeking assay.

### Open once

After the matrix is frozen, compute exact `C_A` and `C_F`. Keep zero-gap, unresolved or rejected outcomes as terminal receipts; do not redesign the four worlds after seeing the result.

### Genetics only after task admission

Use genetic perturbations to determine whether the admitted task has a defensible genotype-policy map. Do not use successful behavioral knockouts to retroactively define the queries.

## Population ceiling

Even a successful positive-gap laboratory task plus a qualified genotype-policy support graph would not identify stationary evolutionary occupancy or waiting time. Those claims remain blocked without relative mutation bias, a population process and an absolute rate scale, exactly as shown by the downstream nonidentifiability side theory.

## Literature anchors

- Duvall L.B. et al. 2019. *Small-Molecule Agonists of Ae. aegypti Neuropeptide Y Receptor Block Mosquito Biting*. Cell 176:687-701.e5. DOI: 10.1016/j.cell.2018.12.004.
- Frank K. et al. 2026. *A signaling hub in the mosquito rectum coordinates reproductive investment after blood feeding*. Current Biology. DOI: 10.1016/j.cub.2026.02.042.
- Raji J.I. et al. 2019. *Aedes aegypti mosquitoes detect acidic volatiles found in human odor using the IR8a pathway*. Current Biology 29:1253-1262.e7. DOI: 10.1016/j.cub.2019.02.045.
- *Functional dissection of mosquito humidity sensing reveals distinct Dry and Moist Cell contributions to blood feeding and oviposition*. 2024. PMID: 39159375.
- *Humidity sensors that alert mosquitoes to nearby hosts and egg-laying sites*. 2023. Identifies Ir93a-dependent hygrosensation in host proximity and oviposition-site seeking.
- *Post-biting behavioral reprogramming underlies reproductive efficiency in Aedes aegypti mosquitoes*. 2025. Tracks the transition to gravid humidity seeking and oviposition behavior.
- Melo N. et al. 2020. *Geosmin attracts Aedes aegypti mosquitoes to oviposition sites*. Current Biology 30:127-134.e5. Secondary candidate cue.

## Verdict

Among candidates screened so far, the Aedes gonotrophic switch remains the clearest **prospective positive-gap architecture** because different physiological branches require different ecological distinctions.

The most defensible primary B channel is now Ir68a-dependent humidity / water-container seeking, not geosmin. The key unresolved question is no longer whether branch-B has a causal sensory handle, but whether a prospective experiment can demonstrate the full context-contingent information-use task under predeclared cue, target and cost semantics.