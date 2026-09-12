# Downstream population nonidentifiability ceiling

## Purpose

This note closes the routing/population side line. The flagship theorem identifies a phenotype-level requirement

`required local regime -> required structural gap q -> minimum/Pareto finite sensing phenotype`.

That upstream result does **not** identify how quickly a population can reach the required phenotype, how much stationary mass the phase receives, or how long phase entry takes in biological time. Those conclusions require additional model declarations.

This is a claim-boundary result, not a novelty claim for genotype-phenotype maps, mutation bias, reversible mutation-selection equilibrium, or Markov-chain time scaling.

## C1 — accessibility is not identified by q plus phenotype fitness

Fix any required gap `q>=1`, the gain set `{0,...,q}`, and any phenotype fitness schedule `W(g)`.

For every integer `D>=1`, construct a finite connected genotype graph as follows.

1. Create a path `p_0--p_1--...--p_D`.
2. Let `p_0` be the declared start genotype.
3. Assign gain zero to `p_0,...,p_{D-1}` and gain `q` to `p_D`.
4. For every intermediate gain `r=1,...,q-1`, attach one leaf of gain `r` to `p_0`.

Every gain level `0,...,q` is represented. The only gain-`q` genotype is `p_D`, and the attached intermediate-gain leaves do not create a shortcut. Therefore the shortest full-phase distance is exactly

`d(start, full)=D`.

Because `D` is arbitrary, `q` and the phenotype fitness schedule do not identify mutational accessibility.

The implementation in `adaptive_gain/downstream_population_nonidentifiability.py` constructs the graph exactly, and the tests verify the distance by an independent BFS over a grid of `(q,D)` values.

## C2 — stationary occupancy is not identified even after local support is fixed

PR #26 and PR #29 already establish the stronger fixed-support result.

Fix

- one genotype per gain level `0,...,q`;
- the same local path support `0<->1<->...<->q`;
- the same phenotype-selection tilt `theta`.

For any strictly positive target stationary distribution `p`, choose neutral reversible measure

`mu_r proportional to p_r theta^(-r)`.

Then the selected origin-fixation stationary law is exactly `pi=p`.

Hence even after raw multiplicity and local mutation support are fixed, unknown relative mutation bias leaves stationary phase occupancy nonidentified over the positive simplex.

Canonical `q=2, theta=2` witnesses on the same path support give full-phase masses `7/10` and `1/10` solely by changing neutral mutation bias.

## C3 — absolute waiting time is not identified after occupancy is fixed

PR #32 adds the final timing coordinate. Hold fixed

- `q`;
- gain map;
- path support;
- neutral reversible measure;
- selected stationary distribution;
- phenotype-selection tilt.

Multiply every adjacent neutral proposal edge by a common `epsilon in (0,1]`, putting the removed mass on self-loops. The selected transition matrix obeys

`P_epsilon=(1-epsilon)I+epsilon P_1`.

Stationary proportions and support distances are unchanged, while every expected target hitting time in proposal-attempt units obeys

`H_epsilon=H_1/epsilon`.

Thus an overall proposal/mutation-rate scale is a separate required input. Proposal attempts must not be translated into generations without an empirical rate model.

## Combined ceiling

The side theory therefore separates three downstream coordinates that the flagship phenotype theorem does not determine:

| downstream quantity | extra declaration required | exact no-go result |
|---|---|---|
| mutational accessibility | genotype-policy map + mutation support graph + start state | same `q` and phenotype fitness permit any positive shortest full-phase distance `D` |
| stationary phase occupancy | neutral mutation measure / relative proposal bias + population process | on one fixed path support, any positive stationary gain law can be realized |
| absolute waiting-time scale | overall proposal/mutation-rate scale | same support and occupancy permit `H` to scale as `1/epsilon` |

A concise declaration ladder is therefore

1. phenotype gap and fitness schedule;
2. genotype-policy map and mutation support graph;
3. neutral mutation measure or relative proposal bias;
4. absolute proposal or mutation-rate scale;
5. population process connecting mutation and selection.

Each rung licenses a different class of downstream statement. None can be inferred merely because the upstream sensing phenotype has a required structural gap.

## Strong conclusion

The flagship result is a **structural reachability theorem at the phenotype/sensing level**. It does not imply evolutionary accessibility or population occupancy.

Formally,

`required regime -> q -> finite sensing phenotype requirement`

does not identify

`mutation distance`, `stationary phase mass`, or `waiting time`.

Those become identifiable only after the relevant downstream representation and process are declared.

## Biological qualification gate

Issue #27 remains the hard biological gate. A routing genotype or mutation graph must not be interpreted as biology merely because the mathematics is exact. A biological application requires evidence for the context-dependent modules, heritable regulatory substrate, mutation locality, pleiotropic coupling, phenotype map, and where relevant mutation/proposal bias.

Without that qualification, the downstream stack is best read as an identifiability boundary showing what the flagship theorem does **not** authorize.

## Prior-art ceiling

Do not claim novelty for

- generic genotype-phenotype representation dependence;
- arbitrary graph constructions or shortest-path control;
- neutral networks or representation-dependent evolvability;
- reversible mutation-selection equilibrium;
- mutation bias and stationary abundance bias;
- origin-fixation theory;
- Markov-chain laziness or time rescaling.

The repository-specific contribution of this note is organizational: it closes the inference boundary downstream of the adaptive-gain phenotype theorem with exact witnesses for accessibility, occupancy and timing.

## Hard stop

This mathematical side line should stop here unless a biological genotype-policy system passes issue #27 qualification. Further abstract encodings would not strengthen the flagship paper and would only add representation-specific examples beyond an already complete nonidentifiability ceiling.
