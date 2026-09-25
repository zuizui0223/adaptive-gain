# Environmental routeability determines the ecological cost of heterogeneity

## Teaser text

Ecological diversity does not necessarily create ecological complexity. We show that the same number of resources, habitats or interaction states can impose radically different information costs depending on whether early cues partition the environment into branches that make later information conditionally relevant. This environmental **routeability** separates raw heterogeneity from the complexity actually experienced in ecological interactions, with consequences for niche breadth, realized interaction networks and the evolutionary effects of environmental change.

## Abstract

Environmental heterogeneity is central to ecological theory because it is expected to shape niche breadth, adaptive behavior and the maintenance of diversity. Yet heterogeneity is usually described by how many alternatives exist or how strongly environments vary, rather than by how those alternatives are organized for ecological decisions. We introduce **environmental routeability**: the extent to which early cues partition ecological alternatives so that later information is needed only within the realized branch. For a focal ecological decision, let \(C_A\) be the minimum worst-case cost of resolving the relevant alternatives by contingent cue acquisition and \(C_F\) the minimum cost of a precommitted cue set. The pair \((C_A,C_F)\) describes decision-relevant environmental complexity without treating complexity as a universal scalar. We show that ecological diversity and decision complexity can be sharply decoupled. Environments with identical numbers of alternatives and exactly balanced cue frequencies can have arbitrarily large fixed-to-contingent cost ratios when heterogeneity is hierarchically routeable. Conversely, additional ecological states need not increase effective complexity when they are equivalent for the focal action. Routeability becomes selectively consequential under intermediate ecological constraints, when \(C_A\le B\) but \(B<C_F\). These results refine the common expectation that greater environmental heterogeneity favors broader or more flexible niches: the relevant predictor is not heterogeneity alone, but whether diversity can be navigated through cheap routing cues and branch-specific information. The same logic predicts that routeability can alter the behaviorally accessible subset of interactions that are otherwise permitted by morphology, phenology and encounter opportunity, whereas persistent environmental variation matters only when it changes decision-relevant structure. Ecological complexity is therefore relational: biodiversity, environmental variance and interaction richness become costly only insofar as they create distinctions that must be resolved together.

**Keywords:** environmental heterogeneity; ecological complexity; niche breadth; generalism; adaptive foraging; ecological information; interaction networks; temporal heterogeneity

## Introduction

Environmental heterogeneity is one of ecology's most general explanations for variation in niche breadth, adaptation and diversity. Classic theory distinguishes homogeneous from heterogeneous environments and asks when specialists, generalists or plastic strategies should evolve. Experimental evolution similarly shows that broader environmental variation often, though not invariably, favors broader ecological niches and maintains fitness variation across environments (Kassen 2002). Across community ecology, resource diversity and temporal or spatial heterogeneity are also treated as forces that alter interaction structure, coexistence and ecological opportunity.

But equal amounts of heterogeneity need not pose equal ecological problems.

Consider two communities containing the same number of potential resources. In one, a coarse cue immediately separates resources into functional groups, after which only one group-specific cue is needed. In the other, each resource must be discriminated by a different cue that remains potentially relevant throughout the encounter. The communities have the same richness. They may even have the same marginal frequencies of cue outcomes. Yet a consumer can navigate the first environment by sequentially narrowing the relevant alternatives, whereas the second requires much broader information acquisition. From the standpoint of ecological interaction, the two communities are not equally complex.

This distinction has precedents in behavioral ecology but has not been elevated into a general ecological property of heterogeneous environments. Naturally occurring foraging decisions are sequential and hierarchical rather than isolated binary choices (Stephens 2008). Polyphagous herbivores can use broadly shared host cues first and more specific cues later, motivating the sequential-cues hypothesis for how generalists navigate diverse plant communities (Silva & Clarke 2020). Adaptive foraging models further show that behavioral adjustment can alter food-web structure, interaction strength and community stability (Loeuille 2010; Beckerman et al. 2010). Together, these literatures imply that the organization of environmental alternatives can matter as much as their number.

We call this property **environmental routeability**. An environment is routeable for a focal ecological task when early, relatively inexpensive observations divide ecological alternatives into branches that make different later cues relevant. Routeability is not an intrinsic scalar property of a habitat or community. It is relational: it depends on the ecological alternatives, the focal action, the available cues and their costs. The same community can therefore be highly routeable for one interaction and poorly routeable for another.

This perspective suggests a different question from the usual "does more heterogeneity favor flexibility?" Instead we ask:

> **When does ecological diversity translate into decision-relevant complexity, and when can hierarchical environmental structure prevent that translation?**

We use an exact finite decision model to answer this question. The existing mathematical results yield five ecological conclusions. First, ecological diversity and decision complexity are not equivalent: environments with the same richness and cue marginals can differ without bound in the advantage provided by contingent routing. Second, additional ecological states can be effectively free when they are equivalent for the focal action, so species richness or environmental state richness need not increase decision burden. Third, routeable heterogeneity creates a mechanism by which broad niche use can remain compatible with finite sensing or sampling budgets. Fourth, routeability can filter which otherwise permitted ecological interactions remain behaviorally accessible within those budgets, adding an information constraint between compatibility and realized interaction. Fifth, temporal persistence matters only when recurrent environmental states differ in decision-relevant structure. The main ecological result is therefore not a new property of organisms, but a new distinction among environments: **heterogeneity can be routeable or non-routeable, and that distinction governs its effective ecological cost.**

## Methods

### Ecological alternatives and focal actions

We represent an ecological environment by a finite set of alternatives relevant to a focal interaction. These alternatives can be resource types, host states, predator contexts, habitat states, interaction partners or other conditions that may require different actions. The target specifies which distinctions change the focal ecological response.

This target dependence is essential. Two resources can be taxonomically distinct yet equivalent for an accept/reject decision. Conversely, two individuals of the same resource species can occupy different decision classes if their state changes the appropriate response. We therefore distinguish **raw ecological diversity** from **decision-relevant diversity**.

Cues partition ecological alternatives according to their outcomes. Acquiring a cue has a positive additive cost that can represent time, energy, exposure, handling opportunity or another common ecological currency. The model does not require that this cost be neural processing time.

### Contingent and non-contingent environmental resolution

Let \(C_F\) be the minimum cost of a precommitted cue set sufficient to resolve the focal ecological target. Let \(C_A\) be the minimum worst-case cost when later cues can depend on earlier outcomes. Because any fixed cue set is also a valid contingent strategy that simply ignores intermediate outcomes,

\[
C_A\le C_F.
\]

The pair \((C_A,C_F)\) is our task-specific description of effective environmental complexity. We deliberately do not collapse it into a universal scalar. \(C_A\) describes how costly the environment is when its branch structure can be exploited; \(C_F\) describes the burden when all potentially relevant information must be provisioned before the realized branch is known.

The routeability advantage for a focal state is

\[
g=C_F-C_A.
\]

Large \(g\) means that environmental branches make different later information relevant. Small \(g\) means that most relevant information is shared across branches.

### Decision-equivalent ecological states

Raw ecological states can differ without changing the focal decision problem. The exact target-relevant reduction identifies when two represented states have the same target and the same remaining cross-target discrimination requirements. Such states can be collapsed without changing the optimal contingent resolution cost.

Ecologically, this defines **decision-equivalence classes**. Adding species, resource states or environmental variants inside an existing equivalence class can increase raw diversity without increasing the contingent complexity of the focal interaction.

### Ecological constraints

Let \(B\) be an ecological budget on the same cost scale. Depending on the system, \(B\) may represent time before an opportunity closes, tolerated exposure to enemies, energetic sampling capacity or another hard or effectively hard constraint.

The routeability of an environment changes realized performance only when

\[
C_A\le B<C_F.
\]

Below \(C_A\), even contingent routing cannot complete the focal interaction. Above \(C_F\), routeability is unnecessary because all relevant information fits within the budget.

### Recurrent environmental states

Environmental contexts can recur through seasons, habitats or community states. We model recurrence as a finite ergodic reversible Markov chain. The long-run effect of state-dependent selection separates into environmental persistence and the alignment of selection with persistent ecological modes. The formal spectral result is given in the Supplement.

## Results

### Ecological diversity and effective complexity can be decoupled

The first result is that raw heterogeneity is not a bound on the value of routeability.

We construct finite binary environments in which every cue has exactly balanced outcomes across represented ecological alternatives. Despite identical marginal balance, the cost of a precommitted resolving cue set grows exponentially with routing depth, whereas a contingent strategy follows a shallow sequence and then acquires only the terminal information needed for the realized branch.

Thus environments can have the same number of cue outcomes, the same marginal cue balance and the same focal target size yet differ strongly in how much information must be acquired on any realized ecological path. The distinction is architectural: whether later information is shared among branches or segregated among them (Fig. 1).

This result motivates the core ecological distinction:

> **heterogeneity is routeable when ecological alternatives can be progressively partitioned so that unrealized branches stop generating information costs.**

The converse is non-routeable heterogeneity, in which many distinctions remain jointly relevant regardless of earlier observations.

### Species richness need not increase decision complexity

The target-relevant reduction gives a second ecological result. Raw increases in ecological state richness need not increase the complexity of a focal interaction.

If newly added states fall into an existing decision-equivalence class, they can be collapsed without changing \(C_A\). For example, adding several host species that all trigger the same action and have the same future discrimination requirements can increase host richness while leaving the optimal contingent decision unchanged. By contrast, adding a single ecological alternative that creates a new branch-specific requirement can increase effective complexity.

This means that richness and complexity can move independently. A species-rich community can be behaviorally simple for a focal consumer if many species are interchangeable at the relevant decision scale. A species-poor community can be difficult if each alternative requires a distinct terminal cue.

The ecological unit relevant to information burden is therefore not necessarily the species, habitat type or environmental state. It is the **decision-equivalence class** generated by the focal interaction (Fig. 2).

### Routeability changes the information cost of broad niche use

Environmental heterogeneity is often expected to favor generalism or plasticity, but empirical and theoretical results show that the relationship is not automatic (Kassen 2002). Our results identify a structural modifier of that relationship.

A generalist using many resources does not necessarily need to process information about all resources on every encounter. If resources are organized hierarchically—habitat first, then host group, then host state—a sequence of cheap routing cues can reduce the realized information burden even when total resource richness is high. This is the logic proposed for polyphagous herbivores by the sequential-cues hypothesis (Silva & Clarke 2020), but the present result makes the ecological condition explicit: generalism is informationally cheaper when resource heterogeneity is routeable.

This does not imply that routeability alone causes generalism. Energetic trade-offs, antagonistic pleiotropy, competition, learning, genetic constraints and resource profitability can all limit niche breadth. The prediction is narrower:

> **for otherwise comparable heterogeneous environments, broader niche use should be less constrained by information acquisition when ecological alternatives can be partitioned through cheap early cues.**

The opposite case also matters. In non-routeable environments, increasing resource richness can translate more directly into information burden because many terminal distinctions remain simultaneously relevant. Thus the same increase in environmental heterogeneity can have different evolutionary consequences depending on how that heterogeneity is organized.

### Routeability filters otherwise permitted interactions

Community ecology already distinguishes potential from realized interactions. In mutualistic networks, phenological mismatch, morphological mismatch and accessibility can create forbidden links even when two species co-occur (Olesen et al. 2011; Maruyama et al. 2014). Adaptive foraging can further alter food-web topology, interaction strengths and community stability (Loeuille 2010; Beckerman et al. 2010). The present framework adds a different filter after those compatibility constraints: among interactions that are otherwise ecologically permitted, information needed to identify, rank or handle an alternative may still be too costly to acquire within the opportunity window.

Consider a consumer with many resources that are already compatible in morphology, phenology and encounter opportunity. A permitted link can still be behaviorally inaccessible if the information needed to identify, rank or handle that resource cannot be acquired within the ecological budget. In a routeable community, early cues can eliminate irrelevant resource branches, allowing more of the otherwise permitted interaction set to remain behaviorally accessible. In a non-routeable community, the same nominal resource richness can exceed the information budget, so some permitted links cannot be reliably resolved before the opportunity closes.

This yields a community-level prediction:

> **among otherwise permitted interactions, the behaviorally accessible fraction should depend on the routeability of the resource environment.**

The prediction concerns a constraint on adaptive interaction, not a claim that sensing alone determines food-web structure (Fig. 3). Competition, morphology, energetics and spatial co-occurrence remain necessary determinants of realized interactions. Routeability specifies when the information burden of a diverse community does or does not become an additional limiting factor.

### Ecological constraints expose the cost of non-routeable heterogeneity

Routeability has no unique performance effect when ecological constraints are either extremely severe or very weak. Its effect is exposed at intermediate budgets.

If \(B<C_A\), neither routeable contingent sampling nor a precommitted strategy can guarantee the focal decision. If \(B\ge C_F\), both can. Only when \(C_A\le B<C_F\) does environmental branch structure change whether the focal interaction can be completed.

This gives a non-monotonic ecological prediction. Increasing time pressure, enemy exposure or opportunity cost can first make environmental routeability important and then make it irrelevant again once even the routed strategy becomes infeasible.

The same community can therefore shift between effectively simple and effectively difficult states without changing species richness. A change in phenology, predator abundance, resource residence time or encounter rate can move the ecological budget relative to the same underlying branch structure.

### Temporal heterogeneity matters when it changes decision-relevant structure

Environmental autocorrelation alone does not determine the long-run evolutionary effect of heterogeneity.

Persistent environmental modes contribute strongly only when the states connected by those modes differ in the decision-relevant payoff of routeability. A slowly alternating habitat mosaic can therefore have little effect if each habitat belongs to the same decision-equivalence structure for the focal interaction. Conversely, a less persistent environmental cycle can matter strongly if it repeatedly moves the system between states with different branch structures or across the routeability-sensitive budget window.

The relevant temporal variable is therefore not persistence alone but **persistence of decision-relevant heterogeneity** (Fig. 3).

## Discussion

### Heterogeneity is not the same as complexity

The central ecological conclusion is that heterogeneity and effective complexity are different properties.

Ecology commonly quantifies heterogeneity through species richness, environmental variance, habitat diversity or the number of resource states. Those quantities describe how many alternatives exist or how different they are. They do not describe how many distinctions must remain simultaneously unresolved during an ecological interaction.

Routeability supplies that missing dimension. In a highly routeable environment, early information compresses the set of relevant alternatives, and later costs are paid only for the realized branch. In a poorly routeable environment, the same raw diversity remains jointly relevant. Consequently, two communities with the same richness can present very different effective complexity to the same focal interaction.

This is a relational view of ecological complexity. Complexity does not reside solely in the environment or solely in the organism. It emerges from the mapping among environmental alternatives, ecological actions and the cues that connect them.

### Biodiversity need not imply information burden

One implication is that biodiversity need not scale monotonically with the information burden of ecological interaction.

If additional species are decision-equivalent for a focal consumer, pollinator, predator or host selector, richness can rise without increasing contingent resolution cost. This is stronger than saying that organisms can generalize across similar species. The exact reduction shows why: distinctions that never affect the focal action or future discrimination requirements are formally irrelevant to the decision problem.

This perspective suggests a distinction between **taxonomic richness** and **interaction-relevant richness**. The two will coincide only when each added ecological state creates a new distinction that must be resolved. Otherwise, biodiversity can be compressed into fewer functional decision classes.

This distinction is related to, but not identical with, ecological functional redundancy. Functional-redundancy theory already separates the number of species from the number or distribution of functions represented in a community and shows that richness itself need not predict the ecological consequences of redundancy (Biggs et al. 2020; Ricotta & Pavoine 2025). Decision equivalence is narrower and explicitly relational: two species can be functionally distinct in the ecosystem yet equivalent for one focal action if they impose the same target and future discrimination requirements.

The present theory therefore adds an information-based reason why species identity, ecological function and interaction-relevant richness need not coincide. Multiple species can occupy the same decision-equivalence class even when they remain ecologically distinct in other respects.

### Routeability refines the heterogeneity–niche breadth hypothesis

Heterogeneous environments are often expected to favor broader niches, versatile phenotypes or plasticity. Kassen's review of experimental evolution emphasized both the general support for this expectation and its important exceptions (Kassen 2002). Environmental routeability provides one reason those exceptions should exist.

Two equally heterogeneous resource environments can differ in whether broad resource use requires broad simultaneous information processing. If early cues group resources into progressively smaller sets, high richness can remain compatible with modest realized sampling costs. If every resource requires an independent terminal distinction, the same richness directly increases the information burden of generalism.

The prediction is therefore not simply "heterogeneity favors generalism." It is:

> **heterogeneity favors broad ecological use more readily when it is routeable.**

This prediction links niche breadth to the internal structure of resource diversity, rather than only to its magnitude. It also explains why sequential cue use can be ecologically important without assuming that generalists possess unlimited sensory capacity.

### Routeability adds an information filter to adaptive-foraging ecology

Adaptive foraging links individual behavior to community structure because consumers modify diet and interaction strength in response to ecological conditions. Such adaptation can stabilize food webs and change realized topology (Loeuille 2010; Beckerman et al. 2010). Yet adaptive-foraging models often begin after the set of behaviorally available alternatives has already been specified.

Environmental routeability operates one step earlier. It determines whether the information needed to discriminate among those alternatives can be acquired within the ecological opportunity window.

This creates a three-step distinction. Species pairs first enter a broad set of possible encounters. Established compatibility constraints such as morphology, phenology and spatial overlap then define a **compatibility-permitted network**; forbidden links are excluded at this stage (Olesen et al. 2011; Maruyama et al. 2014). Routeability acts only on this last transition from compatibility-permitted to **behaviorally accessible** links: an otherwise permitted interaction can remain inaccessible when the information needed to identify, rank or handle the partner exceeds the ecological opportunity window.

The framework therefore predicts that two communities with similar richness and similar compatibility-constrained interaction sets can differ in the fraction of those links that is behaviorally accessible because one community is more hierarchically navigable. This is a community-level prediction derived from the finite decision structure, not a separate theorem or an empirical demonstration. It is also distinct from a forbidden link: the interaction is biologically possible, but its reliable realization is constrained by decision-relevant information cost.

### Environmental change matters when it changes ecological distinctions

The theory also changes how environmental variation should be interpreted.

A large abiotic change may have little effect on routeability if it leaves the focal decision-equivalence classes unchanged. Conversely, a subtle change in community composition can matter strongly if it introduces a new branch-specific distinction or collapses an old one.

Thus the ecologically important quantity is not raw environmental distance. It is whether environmental change alters the distinctions that have to be resolved together.

This provides a sharper interpretation of temporal and spatial heterogeneity. The same variance can be biologically consequential or nearly invisible depending on its alignment with decision-relevant structure.

### Ecological consequences across scales

The routeability perspective produces a hierarchy of ecological consequences from the same structural result.

At the resource level, it determines whether many alternatives can be navigated cheaply. At the niche level, it modifies the information cost of broad resource use. At the community level, it constrains which potential interactions can be behaviorally realized. Across time, it determines whether recurrent environmental change repeatedly alters those accessible alternatives. In eco-evolutionary settings, only sufficiently large contrasts in routeability can contribute strong state-dependent feedback through this mechanism.

The mathematics therefore does not primarily say that organisms should "measure more" or "sense better." It says that **the ecological organization of alternatives determines how much of environmental diversity must be processed at once.**

### Scope

Environmental routeability is task-specific. A community can be routeable for host acceptance but not for predator discrimination, and the same cue can be cheap in one species and expensive in another. The framework therefore does not define a universal scalar ranking of communities from simple to complex.

The exact model also assumes deterministic cue outcomes, additive acquisition costs and guaranteed target resolution. Noise, probabilistic errors, continuous sampling and expected-loss decisions remain important extensions.

Finally, the niche-breadth and food-web consequences developed here are ecological predictions derived from the structural results, not empirical demonstrations. Their value is that they identify a previously missing axis of heterogeneity that can explain why equal amounts of environmental diversity need not have equal ecological effects.

## Conclusion

Environmental heterogeneity has ecological consequences only through the distinctions it forces interacting organisms to resolve. When those distinctions are hierarchically routeable, high diversity can remain low in effective decision complexity; when they are not, modest diversity can impose large information burdens. The same principle separates taxonomic richness from interaction-relevant richness, refines when heterogeneous environments can support broad niches, constrains the subset of potential interactions that can be behaviorally realized, and filters which forms of temporal variation matter evolutionarily.

The resulting ecological claim is simple:

> **diversity is not complexity; the structure of heterogeneity determines its ecological cost.**

## Data and code availability

No empirical datasets were generated or analyzed for this theoretical study. Source code and exact mathematical support are publicly available in the \`zuizui0223/adaptive-gain\` repository. A permanent archival DOI will be added when available.

## Author contributions

**AUTHOR INPUT REQUIRED.** Final author list and CRediT roles must be approved before submission and must not be inferred from repository activity.

## Funding

**AUTHOR INPUT REQUIRED.** Funding or no-specific-funding status must be verified by the final author(s).

## Conflict of interest statement

**AUTHOR INPUT REQUIRED.** The final declaration must be approved by the author(s).

## Acknowledgements

Add only if applicable after final author review.

## References

- Beckerman, A. P., Petchey, O. L. & Morin, P. J. 2010. Adaptive foragers and community ecology: linking individuals to communities and ecosystems. *Functional Ecology* 24:1–6. https://doi.org/10.1111/j.1365-2435.2009.01673.x.
- Biggs, C. R. et al. 2020. Does functional redundancy affect ecological stability and resilience? A review and meta-analysis. *Ecosphere* 11:e03184. https://doi.org/10.1002/ecs2.3184.
- Bernays, E. A. & Wcislo, W. T. 1994. Sensory capabilities, information processing, and resource specialization. *The Quarterly Review of Biology* 69:187–204. https://doi.org/10.1086/418539.
- Bernays, E. A. 2001. Neural limitations in phytophagous insects: implications for diet breadth and evolution of host affiliation. *Annual Review of Entomology* 46:703–727. https://doi.org/10.1146/annurev.ento.46.1.703.
- Dall, S. R. X., Giraldeau, L.-A., Olsson, O., McNamara, J. M. & Stephens, D. W. 2005. Information and its use by animals in evolutionary ecology. *Trends in Ecology & Evolution* 20:187–193. https://doi.org/10.1016/j.tree.2005.01.010.
- Kassen, R. 2002. The experimental evolution of specialists, generalists, and the maintenance of diversity. *Journal of Evolutionary Biology* 15:173–190. https://doi.org/10.1046/j.1420-9101.2002.00377.x.
- Jordano, P. 2016. Sampling networks of ecological interactions. *Functional Ecology* 30:1883–1893. https://doi.org/10.1111/1365-2435.12763.
- Loeuille, N. 2010. Consequences of adaptive foraging in diverse communities. *Functional Ecology* 24:18–27. https://doi.org/10.1111/j.1365-2435.2009.01617.x.
- Maruyama, P. K., Vizentin-Bugoni, J., Oliveira, G. M., Oliveira, P. E. & Dalsgaard, B. 2014. Morphological and spatio-temporal mismatches shape a neotropical savanna plant–hummingbird network. *Biotropica* 46:740–747. https://doi.org/10.1111/btp.12170.
- Olesen, J. M., Bascompte, J., Dupont, Y. L., Elberling, H., Rasmussen, C. & Jordano, P. 2011. Missing and forbidden links in mutualistic networks. *Proceedings of the Royal Society B* 278:725–732. https://doi.org/10.1098/rspb.2010.1371.
- Poisot, T., Stouffer, D. B. & Gravel, D. 2015. Beyond species: why ecological interaction networks vary through space and time. *Oikos* 124:243–251. https://doi.org/10.1111/oik.01719.
- Ricotta, C. & Pavoine, S. 2025. What do functional diversity, redundancy, rarity, and originality actually measure? A theoretical guide for ecologists and conservationists. *Ecological Complexity* 61:101116. https://doi.org/10.1016/j.ecocom.2025.101116.
- Schmidt, K. A., Dall, S. R. X. & Van Gils, J. A. 2010. The ecology of information: an overview on the ecological significance of making informed decisions. *Oikos* 119:304–316. https://doi.org/10.1111/j.1600-0706.2009.17573.x.
- Silva, R. & Clarke, A. R. 2020. The “sequential cues hypothesis”: a conceptual model to explain host location and ranking by polyphagous herbivores. *Insect Science* 27:1136–1147. https://doi.org/10.1111/1744-7917.12719.
- Stephens, D. W. 2008. Decision ecology: foraging and the ecology of animal decision making. *Cognitive, Affective, & Behavioral Neuroscience* 8:475–484. https://doi.org/10.3758/CABN.8.4.475.
