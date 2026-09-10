# Running natural-history example v1

## Purpose

This is an illustrative mapping from the finite-sensing notation to ecological natural history. It is not an empirical claim and not an observation-design proposal. Its only role is to make `world`, `query`, `arity`, adaptive branching, fixed information burden, and recurrent community state biologically legible in the manuscript.

## Example: a flower-visiting insect making a state-contingent foraging decision

Consider an insect that encounters a local flowering patch. Its evolutionary problem is not assumed to be "identify the plant species" in the taxonomic sense. The relevant task is to distinguish ecological alternatives that require different actions: approach, land, continue handling, or reject.

### Represented alternatives (`worlds`)

A finite world can encode combinations such as:

- a rewarding floral resource with low handling cost;
- a rewarding resource whose reward is only revealed after landing;
- a visually similar but unrewarding flower;
- a floral context with elevated predation/competition risk;
- another state that is behaviorally equivalent for the declared action.

Only alternatives that matter to the declared decision need to be represented separately.

### Queries as naturally ordered opportunities for information

Possible cues can become available at different interaction stages:

1. **distant visual cue** — colour, size, or display structure available before approach;
2. **near-range cue** — odour or local visual structure available after approach;
3. **contact cue** — information revealed after landing or touching the flower;
4. **handling/reward cue** — nectar or handling information available only after interaction has begun.

The theory does not require all organisms to use this exact order. The point is that natural history supplies a finite repertoire of distinctions and may make some cues useful only along particular branches of interaction.

### Adaptive versus fixed information

An adaptive policy need not acquire every cue in every encounter. A distant cue may resolve one branch immediately; ambiguous alternatives may require approach and contact; only some landed flowers may require handling information. The worst-case adaptive cost is `C_A`.

A fixed information requirement asks a different structural question: which declared cue resources would have to be available together to guarantee the same target distinction without conditioning acquisition on earlier outcomes? Its minimum size is `C_F`.

The structural gap

\[
g=C_F-C_A
\]

therefore does not mean "the insect gains g units of fitness." It means that the declared ecological decision contains `g` units of avoidable fixed-information burden under the chosen unit-cost representation. A separate ecological lift is required before this structural quantity affects selection.

### Productive obligations

Suppose one pair of alternatives can only be distinguished by the near-range odour cue, another only by a contact cue, and a third only by a handling cue. These are examples of irreducible separation obligations. If no other declared cue can discharge them, they contribute to the productive frontier and hence to the fixed burden.

The frontier is therefore best understood as a bookkeeping device for distinctions that the finite ecology makes unavoidable, not as a new sensory organ or measured trait.

## Community state changes the sensing problem

The surrounding community can change which alternatives and distinctions matter. For example:

- a pollinator-rich state may make floral reward discrimination the dominant task;
- a competitor-rich state may increase the relevance of rapid rejection;
- a predator-rich state may make an early risk cue behaviorally decisive;
- changes in floral composition may create or remove visually confusable alternatives.

Thus community state `i` can change the finite sensing structure and hence its structural gap `g_i`.

The same community state also has temporal persistence and transition probabilities. The theoretical model therefore uses the same state index for

1. the finite information problem that produces `g_i`, and
2. the recurrence process that determines how often `g_i` reappears through time.

This is the biological meaning of the common state space in the main theorem.

## Why this example is intentionally schematic

The paper does not claim that flower visitors literally implement optimal decision trees or that all cues are deterministic. Nor does it propose how to measure the cues experimentally. The example only demonstrates how a natural-history sequence such as

`distant cue -> approach -> near cue -> landing/contact -> handling`

can define a finite branching information structure whose combinatorial constraints are then linked to evolutionary dynamics.

Other systems — host choice, prey assessment, predator recognition, mate assessment, habitat selection — can be mapped in the same way when a finite set of ecologically meaningful alternatives and cues can be declared.
