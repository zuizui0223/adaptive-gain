# Routing population side-theory index v1

Status: recovery/index note. The exact results below live on divergent routing
population branches and are deliberately excluded from the current
decision-complexity Letter.

## 1. Local routing mutation geometry

Source branches:
- `theory/local-routing-mutation-accessibility`
- `theory/routing-neutral-plateau-dynamics`
- `theory/routing-full-target-mesoscopic`

For the (k)-branch routing representation:

- exact local pruning distance to realized gain (r): (kr);
- first strictly beneficial coordinated mutation radius: (k);
- direct one-event radius to gain (r): (kr);
- query-minimal required-gap specialization (k=q+1): full gain (q) is
  (q(q+1)) elementary edits away;
- first (k-1) elementary edits are neutral for worst-path gain;
- uniform branch proposals give first-gain mean (kH_k);
- full-target progress lumps exactly to an occupancy histogram Markov chain;
- for (q=2,k=3,r=2), the exact mean full-target waiting time is
  (347/36) proposal attempts.

These are mutation-operator-specific accessibility statements, not biological
generation times.

## 2. Origin-fixation routing occupancy

Source:
`theory/routing-origin-fixation-selection`.

Under the declared symmetric local proposal and Moran origin-fixation process,

[
pi(x)propto	heta^{g(x)},
qquad
	heta=a^{N-1}.
]

For branch-product genotype space ({0,ldots,q}^k) with
(g(x)=min_i x_i), gain-layer multiplicity is

[
D_r=(q-r+1)^k-(q-r)^k.
]

The sharp aggregate-modal threshold is

[
oxed{	heta_c=2^k-1.}
]

The later sharp corollary branch gives the complete modality trichotomy:
below threshold nonmodal, at threshold exactly the top two layers tie, above
threshold the full layer is uniquely modal.

## 3. Stationary majority threshold

Source:
`theory/routing-stationary-majority-threshold`.

The full-gain stationary majority boundary is the unique positive root of

[
	heta^q=sum_{s=1}^q A_s	heta^{q-s},
qquad
A_s=(s+1)^k-s^k.
]

For (qge2),

[
2^k-1<	heta_{1/2}(q,k)<2(2^k-1).
]

Thus aggregate modality and majority occupancy are distinct estimands.

## 4. Representation and mutation-bias boundaries

Sources:
- `theory/routing-representation-dependence`
- `theory/routing-reversible-mutation-certificate`
- `theory/routing-stationary-nonidentifiability`
- `theory/routing-rate-scale-nonidentifiability`
- `theory/downstream-population-nonidentifiability-ceiling`

Exact counterexamples show that the upstream required gain (q) and phenotype
fitness schedule do not identify:

1. shortest mutational accessibility;
2. stationary phase occupancy;
3. absolute phase-entry time.

Even on one fixed gain-path support, unspecified reversible neutral mutation
bias can realize any strictly positive stationary gain distribution after
selection. Holding support and stationary law fixed, an overall proposal-rate
scale changes expected hitting times exactly as (1/epsilon).

## 5. Publication disposition

This line should remain a separate theory paper or research reserve.

Its strongest candidate-specific mathematics is the routing-induced layer
multiplicity and sharp architecture-dependent modal/majority thresholds.
Moran fixation, origin-fixation stationarity, mutation bias, neutral networks,
weakest-link fitness and selection-versus-degeneracy competition are prior art.

A biological application requires an independently justified genotype-policy
map, mutation locality, neutral proposal bias and population process. Until
then, these results are exact representation-specific mathematics, not evidence
about the evolution of real sensory architectures.
