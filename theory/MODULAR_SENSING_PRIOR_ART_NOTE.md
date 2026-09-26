# Modular sensing / decision-network prior-art note

Status: side-theory novelty guard for issue #13 and draft PR #14.

## Why this note exists

A future topology-to-sensing map

```text
psi: architecture topology T -> finite sensing task S(T)
```

would connect PAYOFF architecture accessibility to adaptive-gain structural reachability. But the generic idea that biological or neural network topology affects information processing, cue integration, decision making, modularity or evolvability is already established.

Therefore a future bridge cannot claim novelty merely because a modular network processes environmental inputs differently from a nonmodular one.

## Existing neighboring theory

Relevant prior-art families include:

- modular neural-network design and evolution;
- evolution of biological network modularity under performance / connection-cost tradeoffs;
- proximate architectures for sensing and decision making in animals;
- cue integration and multiple information channels;
- sensory-motor / neural circuit modularity.

Representative anchors include:

- Happel & Murre 1994, *Design and evolution of modular neural network architectures*, Neural Networks 7:985-1004, DOI 10.1016/S0893-6080(05)80155-8;
- Clune, Mouret & Lipson 2013, *The evolutionary origins of modularity*, Proceedings of the Royal Society B 280:20122863;
- Tosh 2016, *Can computational efficiency alone drive the evolution of modularity in neural networks?*, Scientific Reports 6:31982;
- Eliassen et al. 2016, *From sensing to emergent adaptations: Modelling the proximate architecture for decision-making*, Ecological Modelling 326:90-100, DOI 10.1016/j.ecolmodel.2015.09.001;
- Kuijper et al. 2021, *The evolution of social learning as phenotypic cue integration*, Philosophical Transactions of the Royal Society B 376:20200048, DOI 10.1098/rstb.2020.0048.

These literatures already make structure-to-information-processing connections in several forms.

## Consequence for issue #13

The source-derived map `psi(T)` must do more than assign 'more modular = more sensing flexibility'. That would be both biologically under-justified for PAYOFF and too close to established modular-processing intuitions.

A publishable bridge would need a sharper object, for example:

1. a declared topology rule that determines which cue dependencies are physically feasible;
2. exact adaptive/fixed costs `C_A(T), C_F(T)` from that rule;
3. a nontrivial structural-gap landscape `g(T)` on the mutation graph;
4. a predeclared downstream phase threshold `q`;
5. exact regime-capable set `V_q` and accessibility quantities `d_q,B_q`;
6. at least one result that distinguishes
   - structurally impossible regimes (`V_q=empty`),
   - structurally possible but topology-distance-limited regimes,
   - structurally possible but fitness-valley-separated regimes.

The candidate novelty would then be the **exact composition of mutation accessibility with finite deterministic sensing reachability**, not network modularity or cue integration by themselves.

## Current claim ceiling

Until such a map is built, use only:

> Existing modular-network and sensing theory suggests that architecture can matter for information processing, but the current PAYOFF topology does not yet specify organismal cue-routing resources. A source-derived topology-to-sensing map remains an open bridge problem.

Do not use:

> We discovered that modularity enables adaptive sensing.

or any equivalent broad priority claim.
