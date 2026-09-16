# Mathematical integration design for Evolution Letters V3

Date: 2026-09-16
Status: approved direction; implements the user's request to use the repository's mathematical results more broadly without inventing new theorem families.

## Goal

Reframe the Evolution Letters manuscript from a single no-go result supported by hidden combinatorics into a coherent theory of how finite adaptive sensing defines an eco-evolutionary possibility space, while retaining one biological headline and preserving the frozen V2 submission surface as a fallback.

## Claim hierarchy

The V3 paper has one headline and five mathematical roles.

**Headline:** finite sensing architecture defines which eco-evolutionary regimes are feasible, selectively favored, and temporally expressed within the declared model class.

1. **Foundation — exact adaptive gain.** Use the exact finite deterministic objects `C_A` and `C_F`, the containment theorem `C_A<=C_F`, and the exact adaptive-only budget interval `C_A<=B<C_F`.
2. **Reduction — decision-relevant coarse graining.** Use world-twin quotients, target-relevant query dominance, and the adaptive two-sided Bellman kernel to show that raw natural-history distinctions can be compressed without changing the exact adaptive optimum when they are irrelevant to the declared target.
3. **Extremal geometry — sharp architecture requirements.** Retain the binary sharp corner, bounded-arity Pareto frontier, and the exactly-balanced binary unbounded-gain construction. The balanced construction is used to show that marginal cue balance does not control adaptive value; branch/resource geometry does.
4. **Evolutionary lift — two independent biological bridges.** Keep the monotone-Lipschitz nonlinear no-go theorem and add the hard-budget selection lift based on `C_A<=B<C_F`. The latter demonstrates state-dependent selection without assuming a linear cost-to-fitness map.
5. **Temporal/diagnostic consequences.** Retain spectral recurrence filtering and the model-conditional result that compatible oscillatory return excludes zero feedback while not identifying its magnitude.

## Main-text boundary

The main text should not become a catalogue of proofs. It should contain only mathematics that changes the biological interpretation:

- definitions of `C_A`, `C_F`, `g_i` and `Delta g`;
- the exact budget window;
- the sharp binary/Pareto architecture threshold;
- one balanced-query unbounded theorem statement as a structural counterexample;
- the nonlinear no-go theorem;
- the budget-gated evolutionary-selection result;
- the spectral recurrence formula and alignment interpretation;
- the feedback-existence diagnostic as a boundary result.

Kernel proofs, exhaustive enumeration, private-pair constructions, certificate machinery, recurrence details, and equality audits stay in Supplement/Theorem Atlas.

## Theorem Atlas

Create `manuscript/MATHEMATICAL_ATLAS_V1.md` as the canonical map from repository mathematics to paper roles. Every listed result gets one of four dispositions:

- `MAIN`: biological interpretation changes if omitted;
- `SUPPLEMENT`: necessary proof/reproducibility support;
- `COMPANION`: mathematically substantial but would split the EL narrative;
- `ARCHIVE`: validated implementation/provenance only.

The Atlas must explicitly include the foundation theorem, safe-query compression, world-twin quotient, adaptive two-sided kernel, binary and bounded-arity extremals, balanced-unbounded family, budget-gated selection, nonlinear no-go, structural-spectral envelope, and feedback-identifiability results.

## Biological interpretation

The ecological mapping is:

- represented worlds -> biologically relevant alternatives;
- queries -> available cues/sensory operations;
- adaptive path -> contingent cue acquisition;
- fixed bundle -> precommitted cue repertoire sufficient under every represented alternative;
- budget `B` -> time, energy, exposure, handling, developmental, or opportunity ceiling;
- state-specific gap `g_i` -> avoidable fixed information burden in ecological state `i`;
- between-state `Delta g` -> structural source of state-dependent selection contrast;
- ecological eigenmodes -> recurrence/persistence structure that filters selection through time.

The balanced-query theorem supports a specific biological message: global cue prevalence/balance is not the causal structural quantity controlling adaptive value. Branch-exclusive resource requirements can yield arbitrarily large adaptive advantage even when every binary cue is exactly 50/50 balanced over represented alternatives.

The kernel results support a second message: natural history can contain many distinctions that are irrelevant to the declared decision target. Exact target-relevant quotienting defines which distinctions must be retained before making ecological inference from sensing architecture.

## Claim ceiling

V3 must continue to say:

- necessary no-go bounds are not generic sufficiency;
- finite deterministic architecture is not Shannon information;
- balanced-unbounded is an existence result, not the fixed-`(n,m)` sharp maximum;
- the budget-gated lift is conditional on a hard ecological budget and threshold payoff;
- kernel equivalence is for deterministic exact target resolution with positive additive query costs and worst-path objective;
- spectral persistence matters only with reward-mode alignment;
- feedback-existence diagnostics do not identify feedback magnitude or sensing causality.

## Preservation rule

Do not overwrite or delete the frozen V2 manuscript, V2 Supplement, validated figures, or V2 readiness ledger. Create V3 surfaces alongside them until the expanded manuscript passes its own claim, format, and length checks.
