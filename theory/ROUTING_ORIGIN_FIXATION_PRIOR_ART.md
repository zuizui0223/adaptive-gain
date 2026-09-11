# Prior-art audit: routing origin-fixation selection

Status: conservative side-theory prior-art audit. This note applies to the finite-population routing origin-fixation layer and does not alter the frozen Theoretical Ecology submission.

## 1. Moran fixation and origin-fixation are classical

The well-mixed Moran process has the classical one-mutant fixation probability

```text
rho(R)=(1-R^-1)/(1-R^-N)
```

for constant relative fitness `R`, with neutral limit `1/N`.

Rare-mutation/origin-fixation models then use mutation proposals multiplied by fixation probabilities to define a Markov chain over monomorphic genotype states.

Therefore no novelty can be claimed for the population process itself, for strong-selection/weak-mutation reasoning, or for the fixation-ratio identity used here.

## 2. Statistical-mechanical stationary laws are established

Sella & Hirsh (2005), *The application of statistical physics to evolutionary biology*, PNAS 102:9541-9546, DOI `10.1073/pnas.0501865102`, explicitly develops the analogy between mutation-selection-drift equilibrium and Boltzmann/statistical-mechanical stationary laws. Their treatment includes the rare-mutation genotype-state setting and the role of population size as an inverse-temperature-like parameter.

Barton & Coe (2009), *On the application of statistical physics to evolutionary biology*, Journal of Theoretical Biology 259:317-324, reviews and extends this statistical-mechanical connection, including the rare-mutation symmetric-mutation genotype distribution.

Iwasa (1988), *Free fitness that always increases in evolution*, Journal of Theoretical Biology 135:265-281, DOI `10.1016/S0022-5193(88)80243-1`, is an earlier free-fitness formulation.

Therefore do not claim novelty for:

- `pi(x) proportional to fitness(x)^(N-1)` under a suitable symmetric origin-fixation chain;
- a Gibbs/Boltzmann evolutionary equilibrium;
- population size acting as selection inverse temperature;
- entropy-fitness tradeoffs at equilibrium.

## 3. Genotype-phenotype degeneracy and phenotypic bias are established

The genotype-phenotype-map literature has long emphasized that many genotypes may realize the same phenotype, and that phenotype abundance/neutral-network size can strongly affect evolutionary outcomes.

Representative anchors include:

- Greenbury et al. (2016/2017 lineage) and the review by Schaper (2017), *Structural properties of genotype-phenotype maps*, Journal of the Royal Society Interface 14:20170275, DOI `10.1098/rsif.2017.0275`;
- Manrubia et al. (2021), *From genotypes to organisms: State-of-the-art and perspectives of a cornerstone in evolutionary dynamics*, Physics of Life Reviews;
- extensive neutral-network/quasispecies literature on robustness, evolvability and stationary weighting by genotype-network structure.

Modern reviews explicitly describe phenotype probabilities as fitness factors weighted by genotype degeneracy or sequence entropy. Hence the statement

```text
more numerous lower-fitness genotypes can outweigh a rarer high-fitness phenotype
```

is prior art.

## 4. Neutral-network topology and stationary evolutionary bias are established

Neutral quasispecies, mutational robustness, network centrality and entropy-biased exploration are mature subjects. For example, work on neutral quasispecies shows that even equal-phenotype/equal-fitness genotypes can have unequal long-run frequencies because of mutation-network structure.

The routing side model here is deliberately simpler: its local mutation proposal is symmetric and the exact stationary law depends only on realized gain and the count of routing genotypes at each gain level. That simplicity does not create priority over the broader literature.

## 5. Recent origin-fixation work reinforces the ceiling

Recent work continues to analyze long-run origin-fixation dynamics and reversibility under different population structures and selection mechanisms. This makes broad claims such as “first exact stationary mutation-selection model on an architecture graph” untenable.

The repository should therefore avoid novelty claims for:

- reversible evolutionary Markov chains;
- exact stationary genotype distributions;
- fixation-probability ratios;
- selection-versus-entropy thresholds in generic genotype spaces;
- finite-population mutation-selection balance.

## 6. What is specific here

The new ingredient is not the population genetics. It is the exact upstream routing architecture already derived from the eco-evolutionary required-gap theorem.

For the required-gap star family,

```text
k=q+1,
g(x)=min_i x_i,
x_i in {0,...,q}.
```

This produces the exact gain-layer degeneracies

```text
D_r=(q-r+1)^k-(q-r)^k.
```

The nearest lower layer to full gain contains exactly

```text
2^k-1=2^(q+1)-1
```

genotypes, while the full target contains one.

Composing that exact multiplicity with the classical origin-fixation stationary tilt gives the sharp side-model criterion

```text
theta=a^(N-1) >= 2^(q+1)-1
```

for the full required-gain layer to become stationary-modal.

The bare inequality is elementary once the routing genotype geometry is declared. Its possible research value is only that `q` is not an arbitrary phenotype label: it is inherited from the upstream eco-evolutionary phase requirement and exact finite-sensing theorem.

## 7. Safe claim ceiling

A provisional defensible sentence is:

> We compose an eco-evolutionarily required finite sensing gap with an explicit routing genotype map and a classical finite-population origin-fixation process, yielding exact gain-layer multiplicities and a sharp selection-versus-routing-degeneracy threshold for stationary occupancy of the required phase.

This is a **candidate composition**, not a priority claim.

Avoid:

- “first free-fitness theory of sensing”;
- “first mutation-selection equilibrium for decision architectures”;
- “first entropy barrier to adaptation”;
- “first finite-population theory of sensory evolution”;
- “universal selection threshold `log(2^(q+1)-1)`.”

The threshold is representation- and process-dependent.

## 8. What would strengthen the line

A companion paper would need more than the stationary formula. Stronger possibilities include:

1. a biologically justified genotype-policy mapping that fixes the local routing mutation operator;
2. a result comparing alternative encodings at the same required gap `q`;
3. a transient substitution-time theorem that is not merely a standard birth-death/coupon-collector restatement;
4. an empirical or source-derived system where the routing multiplicity and fitness increment are independently estimable.

Until then, keep the origin-fixation layer as side theory and keep the frozen submission unchanged.
