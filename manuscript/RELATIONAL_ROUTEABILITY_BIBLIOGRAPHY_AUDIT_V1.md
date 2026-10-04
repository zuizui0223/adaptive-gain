# Relational routeability bibliography audit v1

Date: 2026-10-02
Status: current source-verification receipt for `MANUSCRIPT_RELATIONAL_ROUTEABILITY_V0_4_INFORMATION_ACCESS.md`. The current main manuscript contains 29 references; all 29 are cited in the main text. Yuan et al. (2026) is cited only in the Supplement, where its full bibliographic information is given locally.

## Verified core ecology references

### Bernays & Wcislo 1994
Elizabeth A. Bernays & William T. Wcislo.
"Sensory Capabilities, Information Processing, and Resource Specialization."
The Quarterly Review of Biology 69(2):187–204.
DOI: 10.1086/418539.

Role:
Established precursor for information-processing costs, decision time, host/resource specialization, and ecological risk.

### Bernays 2001
E. A. Bernays.
"Neural limitations in phytophagous insects: implications for diet breadth and evolution of host affiliation."
Annual Review of Entomology 46:703–727.
DOI: 10.1146/annurev.ento.46.1.703.

Role:
Established precursor for neural/information-processing constraints on generalists versus specialists.

### Silva & Clarke 2020
Rehan Silva & Anthony R. Clarke.
"The sequential cues hypothesis: a conceptual model to explain host location and ranking by polyphagous herbivores."
Insect Science 27:1136–1147.
DOI: 10.1111/1744-7917.12719.

Role:
Direct ecological precursor for sequential common/specific cue use in host location.
The present manuscript must not claim novelty for sequential cue use itself.

## Earlier information-fitness references verified but not cited in the current manuscript

Donaldson-Matasci et al. (2010) and Rivoire & Leibler (2011) were verified during earlier framings but are not cited in the current decision-ecology manuscript. They remain background provenance, not part of the 30-reference submission bibliography.

## Verified adaptive-acquisition references

### Contardo, Denoyer & Artières 2016
Gabriella Contardo, Ludovic Denoyer & Thierry Artières.
"Recurrent Neural Networks for Adaptive Feature Acquisition."
Neural Information Processing, ICONIP 2016, pp. 591–599.
DOI: 10.1007/978-3-319-46675-0_65.

Role:
Established adaptive acquisition of features with feature-specific costs.

### Janisch, Pevný & Lisý 2020
Jaromír Janisch, Tomáš Pevný & Viliam Lisý.
"Classification with Costly Features as a Sequential Decision-Making Problem."
Machine Learning 109(8):1587–1615.
DOI: 10.1007/s10994-020-05874-8.

Role:
Especially close operational precursor.
Information about a sample is acquired at a cost under average/hard per-sample budgets and framed as sequential decision making.

### Nan & Saligrama 2017
Feng Nan & Venkatesh Saligrama.
"Adaptive Classification for Prediction Under a Budget."
Advances in Neural Information Processing Systems 30.

Role:
Established budget-constrained adaptive prediction.
Use as prior art for adaptive resource allocation, not as an exact structural predecessor.

## Verified Boolean-function entropy-profile prior art

### Forré 1990
Réjane Forré.
"Methods and instruments for designing S-boxes."
*Journal of Cryptology* 2:115–130.
DOI: 10.1007/BF00190799.

Role:
Defines an entropy profile for Boolean functions from conditional entropies of
the output given subsets of input variables. This is direct prior art for the
static all-subset conditional-entropy object. It blocks any novelty claim for
\(S\mapsto H(T\mid Q_S)\) or, with fixed \(H(T)\),
\(S\mapsto I(T;Q_S)\) itself.

### Youssef & Tavares 2004
A. M. Youssef & Stafford E. Tavares.
"Decision trees of cryptographic Boolean functions."
*Canadian Conference on Electrical and Computer Engineering* 1:401–404.
DOI: 10.1109/CCECE.2004.1345040.

Role:
Studies univariate and multivariate linear decision trees as cryptographic
complexity measures and also discusses an entropy profile of Boolean
functions. This blocks rhetoric suggesting that entropy profiles and decision
trees have never been considered together.

Boundary:
The current targeted search did not locate an earlier result showing that two
tasks with the same complete Shannon entropy vector have different **optimal
adaptive worst-case query costs**, nor the direct-product amplification of
that difference. This remains a conservative "no exact predecessor located"
statement, not a categorical priority proof.

## Verified PID / active-acquisition collision

### Li, Dhali & Bouma 2026
Jie Li, Maruf A. Dhali & Hjalmar R. Bouma.
"When Does Synergy Help Active Feature Acquisition? A PID-Based Study."
arXiv:2609.32301, submitted 26 September 2026.

Role:
Direct current prior art for connecting pairwise PID/synergy, realized-value
conditional information, state-dependent active feature acquisition and hard
budgets. The paper also includes a controlled fixed-total-pair-information
analysis. It blocks any claim that the present program is the first to connect
synergy or realized-value conditional information to sequential acquisition.

Boundary:
The repository's distinct theorem-level claim is narrower: identical physical
cue matrices and identical complete Shannon entropy vectors can coexist with
different exact optimal worst-case adaptive resolution costs.

## Verified extra-entropic analogue

### Sun & Jafar 2019
Hua Sun & Syed A. Jafar.
"On the Capacity of Computation Broadcast."
arXiv:1903.07597.

Role:
Provides explicit examples where problems with the same entropy for all subsets can have different operational capacities.
This blocks broad claims that the present theory is the first to show that entropy can miss operationally relevant structure.

## Novelty boundary after verification

The manuscript must treat as prior art:

- information-processing constraints on niche breadth;
- sequential ecological cue use;
- information-fitness theory;
- adaptive/costly feature acquisition;
- complete static conditional-entropy / mutual-information profiles of Boolean
  functions;
- decision-tree analyses adjacent to Boolean-function entropy profiles;
- PID/synergy-guided active feature acquisition;
- realized-value conditional acquisition scores;
- budget-constrained prediction;
- the general possibility that equal entropic structure does not determine an operational quantity.

The candidate contribution remains the exact ecological composition:

same physical cue environment
+ same target prevalence/entropy
+ same total available target information
+ different focal action map
-> sharply different adaptive/fixed guaranteed-resolution geometry
-> exact difference in feasible access regime under one common ecological budget.

## Remaining bibliography work

- all current 29 main-text references are cited; verify any additional citations introduced during later target-journal polishing;
- if Sun & Jafar is cited in the final manuscript, decide whether to cite the arXiv paper or a later archival version if one exists;
- preserve conservative wording around priority.
