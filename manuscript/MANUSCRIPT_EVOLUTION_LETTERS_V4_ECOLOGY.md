# Ecological structure and deadlines govern the evolutionary value of contingent sensing

## Teaser text

Organisms often must act before they can sample every useful cue. We show that contingent sensing is not favored simply by more environmental uncertainty or more available information. Its unique advantage appears under intermediate ecological deadlines, when early cues route individuals toward branch-specific information that would be too costly to acquire exhaustively. Environmental change then matters evolutionarily only when it changes this decision structure or its alignment with recurring ecological states.

## Abstract

Animals and other organisms often make decisions while information is still incomplete. Predator attacks, moving hosts, ephemeral resources and mating opportunities can impose time, energetic or exposure limits on cue sampling, while the relevance of later cues may depend on earlier observations. We develop a theory for when this contingent organization of information use becomes evolutionarily important. For a finite ecological decision, let \(C_A\) be the minimum worst-case cost of acquiring cues conditionally and \(C_F\) the minimum cost of a precommitted cue set that guarantees the same decision. Because \(C_A\le C_F\), contingent sensing has a unique performance advantage only when an ecological budget falls in the intermediate window \(C_A\le B<C_F\). Thus the unique performance opportunity for contingent sensing—and, when the resolution benefit exceeds maintenance cost, its selective advantage—is predicted to be non-monotonic with ecological constraint: absent when constraints are either too severe for any strategy to succeed or sufficiently weak for exhaustive sensing to succeed. Large adaptive advantages can arise even when every binary cue has equally frequent outcomes, showing that branch-specific cue requirements rather than marginal cue prevalence control the value of contingent information use. Across ecological states, differences in this branch structure bound how much state-dependent selection sensing can generate; insufficient contrast excludes specified oscillatory eco-evolutionary feedbacks. Finally, persistent ecological states amplify sensing-generated selection only when the selection contrast aligns with those persistent modes. The theory therefore predicts that contingent sensing should be most strongly favored in heterogeneous environments with intermediate decision deadlines, cheap early routing cues and costly branch-specific terminal cues.

**Keywords:** animal decision making; behavioral ecology; contingent information use; ecological information; eco-evolutionary feedback; sensory ecology; speed–accuracy trade-off

## Introduction

Organisms rarely make ecological decisions with unlimited time and complete information. A forager may need to identify a profitable resource before a competitor arrives, a prey animal may need to classify danger before an attack, an herbivore may need to accept or reject a host while exposed to predators, and a pollinator may need to trade accurate flower discrimination against foraging rate. Information gathering therefore has ecological opportunity costs, while limited attention and processing capacity can constrain how organisms use available information (Lima & Dill 1990; Dukas 2004; Dall et al. 2005; Trimmer & Houston 2014). The ecological value of being better informed depends on the decision that information changes (Schmidt et al. 2010). Ecological speed–accuracy trade-offs are widespread in ecologically relevant tasks, including predator and prey detection, flower choice and spatial exploration, because more reliable discrimination commonly requires additional sampling time (Chittka et al. 2003, 2009).

A recent Information Ecology framework emphasizes three linked questions—what information animals have, how they use it, and why they use it—and argues for connecting laboratory manipulation with ecological context (Bergman & Beehner 2023). Our theory addresses the junction between the latter two questions: how the sequence of cue use is organized, and under which ecological constraints that organization becomes valuable.

These costs are not determined only by how many cues are available. Natural-history decisions are often sequential and hierarchical. Decision ecology has long emphasized that real foraging decisions are not well represented as isolated binary choices: animals move through sequential foreground–background decisions nested from habitat selection to food choice (Stephens 2008). A coarse observation may first place an encounter into a broad context, after which only a subset of cues remains relevant. An herbivore, for example, may use habitat or plant identity before sampling a finer chemical cue; a prey animal may first classify the direction or type of threat before attending to a trajectory-specific cue. Work on host and resource specialization has long argued that informational complexity can increase decision time, reduce discrimination efficiency and prolong exposure to mortality risk, while sensory focusing can reduce those costs (Bernays & Wcislo 1994; Bernays 2001). Proximate models of behavior likewise emphasize that evolution acts on architectures of sensing, processing and behavioral control, not only on an optimized final action (Eliassen et al. 2016).

This motivates a distinction that is ecological rather than purely informational. A **fixed** strategy provisions enough cues to guarantee the focal decision before it knows which ecological branch it is in. A **contingent** strategy can acquire an early cue, use its outcome to discard irrelevant possibilities, and then sample only the later cue needed on that branch. Both strategies can ultimately make the same decision, yet they can differ strongly in the time, energy or exposure needed to guarantee it.

The central ecological question is: **When does the organization of information acquisition become a target of selection?** Three ingredients should matter. First, the natural history must contain branch-specific cue requirements: later cues are useful in some contexts but unnecessary in others. Second, ecological constraints must be strong enough that sampling every potentially relevant cue is costly, but not so strong that even contingent sensing fails. Third, if ecological states recur through time, they must differ in the payoff to contingent sensing for fluctuating selection to accumulate into longer-term evolutionary effects.

We formalize these ideas with a finite decision model. The mathematics yields four ecological conclusions. First, contingent sensing has an exact intermediate budget window in which it alone can guarantee the focal decision. Second, its advantage depends on conditional cue structure rather than marginal cue balance. Third, ecological variation matters for eco-evolutionary feedback only when it changes state-specific decision structure enough to generate a sufficient selection contrast. Fourth, environmental persistence matters only when the sensing-generated contrast aligns with the persistent ecological mode. Together, these results turn a theory of finite decision architecture into a set of testable predictions about ecological deadlines, heterogeneous cue environments and the evolution of contingent information use (Figs. 1–3).

## Methods

### Ecological decision episodes

We represent a focal ecological decision as a finite set of situations that an organism may encounter and a declared decision target. Situations need not correspond to every physically distinct environmental state; they represent alternatives that matter for the focal action. A cue partitions these situations according to its possible outcomes.

Cue acquisition carries a positive additive cost. Depending on the natural history, that cost can represent decision time, energetic expenditure, exposure to danger, handling opportunity, or another currency that can be placed on a common scale. We do not assume that the mathematical cost equals neural processing time in every system; empirical application requires a biologically justified mapping.

A fixed sensing strategy chooses a resolving cue set in advance. Let \(C_F\) be the minimum cost of any fixed set that guarantees the target decision. This fixed strategy is a counterfactual non-contingent benchmark; the model does not assume that natural organisms literally sample every cue simultaneously. A contingent strategy can choose later cues according to earlier outcomes. Let \(C_A\) be the minimum worst-case cost of a contingent decision tree that guarantees the same target. Because a fixed cue set is also a valid contingent strategy that simply ignores intermediate outcomes,

\[
C_A\le C_F.
\]

We denote the state-specific structural advantage by \(g_i=C_F(i)-C_A(i)\ge0\). Exact optimization, target-relevant state reduction and sharp finite structural bounds are given in the Supplement.

### Ecological deadlines expose contingent sensing

Let \(B\) be a hard or effectively hard ecological budget on the same acquisition-cost scale. Examples include time before an attack, time before a host or mate becomes unavailable, energetic capacity for sampling, or tolerated exposure while assessing a resource.

Contingent sensing can guarantee the decision when \(C_A\le B\); fixed sensing can do so when \(C_F\le B\). Therefore the unique performance advantage of contingent sensing occurs exactly when

\[
\boxed{C_A\le B<C_F.}
\]

To translate this performance difference into selection without assigning a linear fitness value to each saved unit of sampling, let target resolution provide benefit \(v\ge0\), baseline fitness be \(w_0>0\), and maintenance of contingent control carry log-cost \(\kappa\ge0\). Then contingent sensing receives the resolution benefit only inside the adaptive-only window. This threshold model is intentionally simple: it isolates the ecological consequence of completing a decision before the opportunity closes.

### Branch-specific cue structure

The advantage \(C_F-C_A\) is generated when different ecological branches require different later cues. Fixed sensing must provision all branch-specific requirements simultaneously, whereas contingent sensing first determines which branch is relevant.

To separate this structural effect from simple marginal cue statistics, we use a family of finite binary decision problems in which every cue is exactly 50/50 balanced over represented situations. Despite this global balance, fixed sensing requires exponentially many branch-specific terminal resources while a contingent strategy follows a shallow routing sequence and then acquires only one terminal cue. Thus global cue balance alone cannot bound the value of contingent sensing.

### Ecological heterogeneity and selection contrast

Ecological states such as seasons, habitats or community contexts may differ in their decision structure. For two ordered states, let \(\Delta g=g_2-g_1\) denote their contrast in contingent-sensing advantage. We allow the selection effect of that advantage to be nonlinear: selection may increase linearly, saturate or show diminishing returns. The only requirement used in the main exclusion result is that the relationship is nondecreasing and has a finite upper marginal effect \(L\) over the relevant domain; the formal definition is given in the Supplement.

### Local eco-evolutionary feedback

To ask when sensing-generated selection can alter local eco-evolutionary dynamics, we use a two-coordinate local response with evolutionary persistence \(\alpha\), ecological persistence \(\phi\), and net restoring feedback \(G\). The ecological coordinate can represent a locally changing resource, encounter or interaction state that is itself affected by evolved behavior and then feeds back onto selection on sensing. If \(B_f>0\) converts selection contrast into maximum feedback strength, the declared model implies the necessary condition

\[
\Delta g>\frac{G_{\rm osc}}{B_fL}
\]

for oscillatory return, where \(G_{\rm osc}\) is the model-specific feedback threshold. Its explicit expression and derivation are given in the Supplement. Crossing this threshold is not sufficient for oscillation; it only removes a structural impossibility.

### Recurring ecological states

Finally, ecological states may recur through time rather than alternate independently. Let them form a finite ergodic reversible Markov chain. Centered state-specific selection can be decomposed across ecological modes. Each mode contributes according to two separable quantities: its ecological persistence and the loading of sensing-generated selection onto that mode. The exact spectral expression is given in the Supplement.

## Results

### Contingent sensing is exposed by intermediate ecological constraint

The inequality \(C_A\le C_F\) divides ecological budgets into three qualitatively different regimes. When \(B<C_A\), even the best contingent sequence cannot guarantee the focal decision. When \(B\ge C_F\), both contingent and fixed strategies can do so. Only in the intermediate region

\[
C_A\le B<C_F
\]

does contingent sensing create a unique performance benefit (Fig. 1).

Under the threshold fitness model, this produces a non-monotonic prediction. Tightening an ecological deadline from a very relaxed state can first expose a selective advantage of contingent sensing, because exhaustive cue acquisition no longer fits inside the opportunity window. Tightening the deadline still further eventually removes that advantage when even the contingent sequence becomes too slow or costly. Selection for contingent sensing therefore need not increase monotonically with time pressure, predation risk or opportunity cost.

The same logic applies when a fixed organismal budget is compared across ecological states. A seasonal or habitat change can move \(C_A\) or \(C_F\) across a fixed physiological or behavioral ceiling, switching the selective value of contingent sensing without any change in the organism's nominal cue repertoire.

### Conditional cue dependence, not cue balance, generates the largest advantages

The balanced binary construction shows that global cue frequency is a poor proxy for contingent value. Every cue in the construction is equally common in its two outcomes, yet the fixed-to-contingent cost ratio grows without bound as the number of branch-specific terminal requirements increases (exact construction in Supplement).

The ecological reason is branch exclusivity (Fig. 2). An early cue need not directly settle the final action to be valuable. Its value can come from determining which later cue is worth acquiring. Fixed sensing must provision all terminal cues because it cannot condition resource use on the early observation; contingent sensing pays for routing and then only the terminal information relevant to the realized branch.

This result predicts that the evolutionary value of contingent sensing should be associated with **conditional cue dependence**—which cues become relevant after which observations—rather than with cue number, cue entropy or global cue balance alone.

### Environmental heterogeneity matters when it changes decision architecture

Raw environmental difference does not automatically generate selection on contingent sensing. Two habitats or seasons can differ strongly in temperature, community composition or cue frequencies yet present the same target-relevant branch structure and therefore the same \(C_A\), \(C_F\) and \(g\).

Conversely, a modest ecological change can have a large effect if it changes which distinctions are action-relevant, adds or removes a branch-specific cue requirement, or moves the decision across the adaptive-only budget window. The relevant form of environmental heterogeneity is therefore **heterogeneity in the decision problem**, not heterogeneity per se.

This distinction also clarifies why sensory focusing and specialization can reduce decision costs. If many ecological alternatives share a small target-relevant branch, raw natural-history complexity can be large while contingent decision complexity remains small. If instead each branch requires a different terminal cue, fixed sensory or processing burden grows rapidly. Exact finite bounds for these cases are given in the Supplement.

### Small state differences cannot generate arbitrarily strong feedback

Ecological states that differ only weakly in contingent-sensing advantage cannot generate arbitrarily strong local feedback through this mechanism. If the largest structurally permitted contrast remains below the necessary threshold \(G_{\rm osc}/(B_fL)\), then the requested oscillatory return is impossible for every sensing-to-selection relationship in the declared nondecreasing bounded-marginal class.

The biological interpretation is an exclusion principle. Observing strong or oscillatory eco-evolutionary feedback would rule out any explanation in which the available ecological states produce too little contrast in contingent-sensing advantage, unless additional mechanisms outside the model are invoked. Conversely, satisfying the structural threshold does not establish sensing as the cause; it only shows that the architecture is large enough not to be excluded.

### Environmental persistence amplifies only aligned sensing-generated selection

Slow ecological change alone does not guarantee persistent evolutionary consequences. The spectral decomposition shows that a persistent ecological mode contributes strongly only when the state-specific selection generated by sensing has a substantial projection onto that mode.

Two systems can therefore have the same environmental autocorrelation yet very different evolutionary consequences. In one, the slowly recurring states may be exactly those in which contingent sensing is strongly favored or disfavored. In the other, the same slow mode may connect states with nearly identical sensing payoffs. The first produces strong long-run amplification; the second does not.

The prediction is an interaction between ecological persistence and state-specific decision structure, rather than a main effect of persistence alone (Fig. 3).

## Discussion

### Contingent information use is an ecological trait, not simply an information quantity

The main result is that the evolutionary value of contingent sensing depends on the ecology of the decision episode. Information must be sampled before an opportunity closes, and different cues must become relevant in different branches. Under those conditions, the sequence in which cues are acquired becomes biologically consequential.

This shifts emphasis away from treating environmental information as a scalar resource. Formal information-fitness theory has established that uncertainty reduction can alter growth or selection (Donaldson-Matasci et al. 2010; Rivoire & Leibler 2011; Moffett & Eckford 2022), while statistical decision approaches emphasize that information is useful through the actions it changes (Dall et al. 2005; Schmidt et al. 2010). Organisms, however, encounter that information through particular sensory and behavioral sequences. The present theory identifies a case in which two organisms can have access to the same cue repertoire and face the same final decision, yet differ in fitness because one can condition later sampling on earlier observations.

The exact budget window makes this ecological dependence especially clear. Contingent sensing is not predicted to be most valuable under the harshest possible constraints. Its unique value is maximal in a middle regime: the environment is restrictive enough that acquiring every potentially useful cue is infeasible, but permissive enough that a routed sequence still succeeds. This is closely aligned with empirical work on speed–accuracy trade-offs, where organisms adjust information sampling according to the cost of time and errors (Chittka et al. 2003, 2009).

### Relation to speed–accuracy and value-of-information theory

The present mechanism is complementary to two established ways of thinking about information. Speed–accuracy theory asks how additional sampling time changes decision quality, and value-of-information approaches ask whether reducing uncertainty improves the expected outcome of an action (Chittka et al. 2009; Donaldson-Matasci et al. 2010; Rivoire & Leibler 2011). Both make clear that more information is not automatically worth acquiring.

Our additional question is whether **the identity of the next useful cue depends on what has already been observed**. When every extra sample has the same role, contingent routing offers little beyond an ordinary stopping problem. When early observations make different later cues relevant on different branches, however, the organism can avoid paying for information that belongs to unrealized branches. The ecological novelty is therefore conditional acquisition of heterogeneous cues, not a new claim that information has costs or that animals trade speed against accuracy.

### Relation to sequential decision ecology

Sequential organization itself is not the novelty of the present theory. Behavioral ecology already treats many foraging problems as hierarchical sequences rather than isolated binary choices (Stephens 2008), and the sequential-cues hypothesis explicitly proposes that generalist herbivores move from broadly shared host cues to more specific host-ranking cues (Silva & Clarke 2020). These frameworks establish that ecological decisions can unfold in stages.

Our contribution is to identify when that staging becomes an **exclusive ecological advantage of contingent acquisition**. The crucial comparison is not sequential versus non-sequential behavior in the abstract, but whether earlier observations allow an organism to avoid paying for later information associated with unrealized branches. Combined with a finite ecological deadline, this yields a specific prediction that prior sequential-cue frameworks do not supply: the unique performance opportunity for contingent sensing appears only in the intermediate region where a routed sequence still completes the decision but a precommitted resolving cue set does not. The same branch structure then determines how strongly ecological states can differ in sensing-mediated selection.

### What evolves: cue order, stopping and conditional deployment

The evolving trait in this framework need not be the presence or absence of a sensory organ. It can be a behavioral or regulatory rule that changes **when** a cue is sampled, whether sampling stops after an early outcome, or which sensory channel is deployed next. Limited attention, learned sampling sequences and conditional behavioral control are therefore natural empirical counterparts of contingent architecture (Dukas 2004; Eliassen et al. 2016).

This also clarifies the fixed comparison. \(C_F\) is a counterfactual benchmark for a strategy that cannot use earlier outcomes to avoid later acquisition costs; it is not a claim that real organisms literally inspect every cue simultaneously. Selection on contingent sensing could act through faster stopping, conditional attention, sequential motor routines, or developmental/regulatory allocation of sensory effort. The model groups these proximate routes by the ecological consequence they share: branch identity changes which later information must be paid for.

### Branch structure gives a natural-history meaning to “complexity”

The balanced-cue result shows why counting cues is insufficient. What matters is whether cue relevance is shared across all situations or segregated among ecological branches. A cheap early observation can have little direct relationship with the final action yet have high decision value because it tells the organism which expensive cue to ignore.

This distinction suggests a natural-history program. Instead of asking only how many cues animals use, studies can record the **sequence and conditionality** of cue acquisition. Does an individual always inspect odor after color, or only after a particular visual category? Does a predator cue trigger a second sampling step only in a subset of contexts? Do host-choice behaviors terminate early after one cue in some branches but continue to chemical or tactile assessment in others? These conditional transitions are the empirical counterpart of the branch structure in the model.

Host choice provides a particularly clear setting. Bernays & Wcislo (1994) and Bernays (2001) argued that broad resource use can increase informational and processing demands, with consequences for decision time and exposure to natural enemies. More specifically, the sequential-cues hypothesis for polyphagous herbivores proposes that broadly shared host cues first route search into host habitat, after which more specific cues guide continued search and host ranking (Silva & Clarke 2020). That natural-history sequence is almost exactly the ecological structure represented by an early routing cue followed by branch-specific terminal information. Our result does not imply that contingent sensing explains specialization in general. It instead adds a conditional possibility: when a generalist can use cheap early cues to route encounters into smaller branch-specific repertoires, contingent sensing can reduce the cost of generalism. When branch-specific terminal cues proliferate and cannot be cheaply routed, the burden of broad resource use remains high. This yields a testable connection among diet breadth, cue sequencing and decision time.

These natural-history mappings are illustrative rather than fitted demonstrations. Pollinator decisions provide another natural system. Bumblebees show both between-individual and within-individual speed–accuracy trade-offs in flower discrimination (Chittka et al. 2003). The present theory predicts that the strongest advantage of contingent sampling should occur not simply in the hardest discrimination task, but where coarse early flower information can rule out most fine-scale sampling while a deadline or foraging opportunity prevents exhaustive inspection. Similar logic can apply to predator assessment, mate choice or prey discrimination. Cue-response sensory ecology has already used sequential stages such as vigilance, cue detection and response to organize predictions for animal responses to fire (Michel et al. 2023), illustrating how natural-history decisions can be decomposed into measurable sensory stages. The present mappings nevertheless remain hypotheses until the relevant cue sequences and costs are measured.

### Environmental variability should be measured at the level of decisions

A common intuition is that variable environments favor more flexible information use. Our results refine that intuition. Variation matters only when it changes what the organism must distinguish, which cues are conditionally useful, or where the ecological budget lies relative to decision cost.

This gives a concrete reason why broad environmental variance may be a weak predictor of information-use evolution. A habitat may vary strongly in abiotic conditions while preserving the same decision branches. Another system may show little abiotic variation yet switch between community states that change which cues identify safe hosts, profitable flowers or dangerous predators. The latter can generate stronger selection on contingent architecture. An instructive empirical precedent comes from host-searching cabbage white butterflies: increasing the number of distractor plant species did not by itself induce more specialized search, and accuracy benefits of specialization depended on the focal resource (Steck & Snell-Rood 2018). Raw complexity alone therefore need not predict the decision strategy that evolves.

The target-relevant reduction results in the Supplement formalize the same point from another direction. Ecologically descriptive differences need not be distinct decision states if they lead to identical future discrimination requirements for the focal action. This is not a claim that those differences are biologically unimportant in general; it is a statement that ecological complexity is task-dependent.

### Temporal ecology determines whether sensing-generated selection accumulates

The recurrence result connects individual decision ecology to longer evolutionary time scales. Environmental persistence is often invoked as a condition for adaptation to variable environments, but persistence alone is insufficient here. The states that persist must also differ in the selection they impose on contingent sensing.

This distinction is important for seasonal or spatially recurring environments. A slowly switching habitat mosaic can generate little long-run effect if all habitats reward the same sensing architecture. Conversely, a moderately persistent cycle can have a large effect if its dominant mode repeatedly contrasts states on opposite sides of the adaptive-only budget window.

The same logic provides a practical empirical target: estimate not only environmental transition rates, but also state-specific decision costs or fitness effects. The relevant quantity is the covariance-like alignment between ecological recurrence and the selection contrast created by sensing.

### Empirical tests

The theory can be tested without fitting the full eco-evolutionary feedback model. A first experiment can identify a focal decision with a measurable stopping rule, reconstruct the order in which cues are sampled, and estimate the minimum contingent and fixed cue sets needed for reliable discrimination. Rapid advances in onboard sensors and field tracking now make it increasingly feasible to monitor individual decisions together with sensory opportunity, social context and the surrounding environment in the wild (Goldshtein & Yovel 2024). A second manipulation can vary the ecological budget—available decision time, exposure duration, handling opportunity or energetic cost—and ask whether the fitness or performance advantage of contingent sensing peaks in the predicted intermediate region.

Across populations or environments, the theory predicts that contingent sensing should be associated with branch-specific cue repertoires and with shifts in the adaptive-only budget window. A particularly strong test would compare systems with similar marginal cue frequencies but different conditional cue dependence. The balanced-cue result predicts that these systems can differ sharply in the value of contingent sampling despite similar one-cue statistics.

At a larger scale, recurrent ecological states can be characterized by a transition matrix and state-specific sensing payoffs. The model predicts that long-run evolutionary effects should depend on whether high-contrast sensing states align with the slow ecological modes, not simply on environmental autocorrelation.

### Limits and scope

The model deliberately treats cues as deterministic and asks for guaranteed target resolution. Natural sensory systems are noisy, individuals can tolerate errors, and organisms may optimize expected rather than worst-case outcomes. Extending the theory to noisy Bayesian decisions, graded accuracy, continuous sampling time and individual heterogeneity is an important next step.

The ecological budget must also be justified independently for each system. \(B\) can represent time, energy, exposure or opportunity only when those quantities can reasonably be mapped onto cue-acquisition cost. Real opportunities will often close gradually rather than at a perfectly hard threshold; such soft deadlines should smooth the edges of the three-region response and require a separate extension rather than being treated as exactly equivalent to the present model. Likewise, the local feedback result is a reachability bound, not a claim that sensing architecture alone generates observed cycles. Mutation, migration, drift, demographic stochasticity and multivariate genetics remain outside the present model.

These limits are useful because they define what empirical evidence would strengthen the theory. The most informative data are not generic measurements of environmental uncertainty, but records of cue order, conditional sampling, stopping decisions, costs of delay, and fitness consequences of crossing ecological deadlines.

## Conclusion

Contingent sensing should evolve not simply where organisms face more information, but where natural history makes some information conditionally relevant and where ecological constraints prevent exhaustive sampling. The theory predicts a middle zone of ecological constraint in which contingent cue acquisition has a unique fitness opportunity, identifies branch-specific cue structure as the source of that advantage, and shows how differences among recurring ecological states can either amplify or extinguish its evolutionary consequences. This places the ecology of information on a concrete structural footing: what matters is not only what organisms can sense, but **which cue they need next, how long they have to decide, and which ecological states make that sequence pay**.

## Data and code availability

No empirical datasets were generated or analyzed for this theoretical study. Source code implementing the finite decision model, exact adaptive and fixed resolution, threshold selection, structural bounds, feedback reachability and ecological recurrence results is publicly available in the \`zuizui0223/adaptive-gain\` repository. A permanent archival DOI should be added at submission if one has been minted by then.

## Author contributions

**AUTHOR INPUT REQUIRED.** Final author list and CRediT roles must be approved before submission and must not be inferred from repository activity.

## Funding

**AUTHOR INPUT REQUIRED.** Funding or no-specific-funding status must be verified by the final author(s).

## Conflict of interest statement

**AUTHOR INPUT REQUIRED.** The final declaration must be approved by the author(s).

## Acknowledgements

Add only if applicable after final author review.

## References

- Bernays, E. A. & Wcislo, W. T. 1994. Sensory capabilities, information processing, and resource specialization. *The Quarterly Review of Biology* 69:187–204. https://doi.org/10.1086/418539.
- Bernays, E. A. 2001. Neural limitations in phytophagous insects: implications for diet breadth and evolution of host affiliation. *Annual Review of Entomology* 46:703–727. https://doi.org/10.1146/annurev.ento.46.1.703.
- Bergman, T. J. & Beehner, J. C. 2023. Information Ecology: an integrative framework for studying animal behavior. *Trends in Ecology & Evolution* 38:1041–1050. https://doi.org/10.1016/j.tree.2023.05.017.
- Chittka, L., Dyer, A. G., Bock, F. & Dornhaus, A. 2003. Bees trade off foraging speed for accuracy. *Nature* 424:388. https://doi.org/10.1038/424388a.
- Chittka, L., Skorupski, P. & Raine, N. E. 2009. Speed–accuracy tradeoffs in animal decision making. *Trends in Ecology & Evolution* 24:400–407. https://doi.org/10.1016/j.tree.2009.02.010.
- Dall, S. R. X., Giraldeau, L.-A., Olsson, O., McNamara, J. M. & Stephens, D. W. 2005. Information and its use by animals in evolutionary ecology. *Trends in Ecology & Evolution* 20:187–193. https://doi.org/10.1016/j.tree.2005.01.010.
- Donaldson-Matasci, M. C., Bergstrom, C. T. & Lachmann, M. 2010. The fitness value of information. *Oikos* 119:219–230. https://doi.org/10.1111/j.1600-0706.2009.17781.x.
- Dukas, R. 2004. Causes and consequences of limited attention. *Brain, Behavior and Evolution* 63:197–210. https://doi.org/10.1159/000076781.
- Eliassen, S., Andersen, B. S., Jørgensen, C. & Giske, J. 2016. From sensing to emergent adaptations: modelling the proximate architecture for decision-making. *Ecological Modelling* 326:90–100. https://doi.org/10.1016/j.ecolmodel.2015.09.001.
- Goldshtein, A. & Yovel, Y. 2024. Onboard sensors reveal new insights into animal decision-making. *Annual Review of Ecology, Evolution, and Systematics* 55:115–131. https://doi.org/10.1146/annurev-ecolsys-102722-125640.
- Lima, S. L. & Dill, L. M. 1990. Behavioral decisions made under the risk of predation: a review and prospectus. *Canadian Journal of Zoology* 68:619–640. https://doi.org/10.1139/z90-092.
- Michel, A., Johnson, J. R., Szeligowski, R., Ritchie, E. G. & Sih, A. 2023. Integrating sensory ecology and predator-prey theory to understand animal responses to fire. *Ecology Letters* 26:1050–1070. https://doi.org/10.1111/ele.14231.
- Moffett, A. S. & Eckford, A. W. 2022. Minimal informational requirements for fitness. *Physical Review E* 105:014403. https://doi.org/10.1103/PhysRevE.105.014403.
- Rivoire, O. & Leibler, S. 2011. The value of information for populations in varying environments. *Journal of Statistical Physics* 142:1124–1166. https://doi.org/10.1007/s10955-011-0166-2.
- Schmidt, K. A., Dall, S. R. X. & Van Gils, J. A. 2010. The ecology of information: an overview on the ecological significance of making informed decisions. *Oikos* 119:304–316. https://doi.org/10.1111/j.1600-0706.2009.17573.x.
- Silva, R. & Clarke, A. R. 2020. The “sequential cues hypothesis”: a conceptual model to explain host location and ranking by polyphagous herbivores. *Insect Science* 27:1136–1147. https://doi.org/10.1111/1744-7917.12719.\n- Steck, M. K. & Snell-Rood, E. C. 2018. Specialization and accuracy of host-searching butterflies in complex and simple environments. *Behavioral Ecology* 29:486–495. https://doi.org/10.1093/beheco/ary001.\n- Stephens, D. W. 2008. Decision ecology: foraging and the ecology of animal decision making. *Cognitive, Affective, & Behavioral Neuroscience* 8:475–484. https://doi.org/10.3758/CABN.8.4.475.
- Trimmer, P. C. & Houston, A. I. 2014. An evolutionary perspective on information processing. *Topics in Cognitive Science* 6:312–330. https://doi.org/10.1111/tops.12085.
