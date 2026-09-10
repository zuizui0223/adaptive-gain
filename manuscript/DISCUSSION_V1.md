# Discussion v1

The central result of this study is not that rapid short-term evolution can coexist with long-term stasis. That pattern is already well established. The new claim is narrower: when state-dependent selection is generated through a finite information structure, the range of evolutionary dynamics available to the system is itself constrained upstream. Finite sensing structure limits how large a structural selection contrast can be, recurrent community dynamics determine how those state-indexed rewards persist or cancel through time, and endogenous feedback determines whether change is restored, oscillates, or accumulates. The resulting picture is therefore one of evolutionary reachability rather than unrestricted parameter choice.

## Finite information structure couples evolutionary amplitude to temporal fate

Most phenomenological models of fluctuating selection can vary the amplitude of selection and its temporal autocorrelation independently. That flexibility is useful, but it leaves open what ecological structure generated those parameters. In the present framework, state-specific reward amplitudes and temporal recurrence are indexed by the same recurrent community states. The finite sensing problem associated with a state constrains the available structural reward, while the transition operator on those states determines how the rewards recur. This creates an upstream coupling between amplitude and temporal filtering.

The structural-temporal ceiling makes that coupling explicit. A finite upper bound on structural reward range limits instantaneous selection variance, while the spectral persistence of the community chain limits how strongly that variation accumulates through time. Slow community modes therefore matter only when the structurally generated reward vector projects onto them. Community persistence by itself is not an evolutionary timescale: only persistence in ecologically relevant contrasts that carry selection reward contributes to long-run evolutionary fluctuation.

This distinction also clarifies why temporal autocorrelation and information constraints should not be treated as interchangeable explanations. Information structure restricts the amplitude that can be generated at each state. Recurrence determines how that amplitude is filtered through time. The long-run outcome depends on both, and neither term can generally substitute for the other.

## Required evolutionary dynamics imply required information complexity

The reverse direction is equally important. Instead of asking only what dynamics a given sensing system produces, one can ask what information structure is required before a desired dynamical regime is reachable. A local feedback phase that requires a minimum feedback gain also requires a minimum structural gap. The finite sensing theory then converts that gap into lower bounds on world number, query resources, and productive-frontier obligations.

For binary sensing these requirements collapse to a single exact first corner. Under higher query arity, however, the notion of a single minimum becomes inadequate. Higher arity can reduce adaptive depth and the number of required query/frontier resources without reducing the minimum number of ecological alternatives that must be represented. The natural result is therefore a Pareto frontier between world complexity and information-channel complexity. This asymmetry is biologically useful: a richer cue can compress the number of sequential distinctions needed to act, but it does not necessarily remove the ecological heterogeneity that makes those distinctions necessary.

The productive frontier survives the translation from combinatorics to ecology precisely because it carries this downstream weight. We do not interpret the frontier as a new biological object in its own right. Rather, it records the irreducible separation obligations that any fixed information strategy must satisfy. A cap on those obligations limits the adaptive gap and can therefore rule out downstream feedback regimes. In this sense the frontier is useful only where it constrains evolutionary reachability; its internal proof machinery need not appear in the main ecological narrative.

## Stasis has at least two dynamically distinct origins

A second consequence is that small long-term net change should not be treated as a single dynamical phenomenon. Temporally opposing selection can produce cancellation stasis even when evolutionary activity within each cycle is large. In the idealized periodic case, the full-cycle map is the identity: there is no net directional accumulation, but perturbations are not actively removed. The stasis is neutral.

Restoring stasis is different. Endogenous eco-evolutionary feedback creates an attracting equilibrium, so perturbations decay. Both mechanisms can yield little long-term net change, yet one preserves deviations and the other erases them. The distinction is therefore dynamical rather than semantic. It also separates two interpretations of evolutionary time. Cancellation stasis reflects repeated directional inconsistency across time. Restoring stasis reflects an endogenous return force generated by the coupled ecological-evolutionary system.

This distinction matters for the interpretation of macroevolutionary stasis. A lineage may appear bounded over long intervals because short-term responses repeatedly cancel, because ecological feedback restores the phenotype toward an attractor, or because both processes operate at different timescales. The present theory does not identify which mechanism generated any particular empirical record, but it shows that the mechanisms are not mathematically interchangeable.

## Oscillation has a different mechanistic status from monotone return

The generalized local model also reveals a sharp asymmetry between monotone and oscillatory restoration. Stable monotone return can admit a decomposition with zero feedback: the observed local eigenvalues may be assigned entirely to intrinsic evolutionary persistence and community persistence. Thus monotone return by itself does not establish that eco-evolutionary feedback generated the trajectory.

A complex local eigenpair is different. Within the declared model class, the characteristic polynomial is then strictly positive on every admissible real community-persistence value, which forces positive feedback gain in every compatible decomposition. The magnitude remains unidentified, but zero feedback is algebraically impossible. Oscillation is therefore not merely a visually distinctive transient. It is the one local regime considered here in which feedback existence is forced by the model structure itself.

This result should not be overgeneralized. Complex eigenvalues do not prove that finite sensing structure caused the feedback, nor do they identify the detailed ecological pathway. The result is conditional on the generalized local model. Its value is narrower: it separates a regime in which feedback can be eliminated by reparameterization from one in which it cannot.

## Natural history enters upstream, not as an after-the-fact interpretation

The framework is most useful when finite sensing tasks are grounded in natural history. An ecological state determines which alternatives are biologically relevant, which cues can distinguish them, and which distinctions must be resolved before an action can occur. Those ingredients define the finite task from which the structural bounds are derived. Natural history therefore enters before evolutionary dynamics are calculated.

Examples could include state-dependent foraging, predator recognition, mate assessment, host choice, or pollinator responses in which different cues become available at different stages of interaction. The main theory does not require a particular sensory modality or taxon. What matters is that the declared task has a finite set of biologically meaningful alternatives and a finite cue repertoire. The biological interpretation of worlds, queries, and productive obligations should therefore be stated explicitly for any application.

## Relation to existing theory

The present framework should be read as a composition of established components rather than a replacement for them. Evolutionary ecology already contains extensive theory on information use, limited attention, sampling costs, learning, cue reliability, plasticity, fluctuating selection, and eco-evolutionary feedback. Computer science and test theory already contain separating systems, optimal decision trees, multiway tests, and adaptivity gaps. Dynamical-systems theory already supplies the local stability and spectral results used here.

The contribution is the exact ecological reachability composition. Finite information complexity is used to bound structurally generated selection; recurrence of the same community states determines temporal filtering; and downstream dynamical requirements are translated back into minimum or Pareto-minimal information structures. The resulting theorems answer a different question from the component literatures: not whether information, temporal autocorrelation, or feedback matter, but which evolutionary regimes are structurally reachable under declared finite information constraints.

## Limitations

Several restrictions are deliberate. The sensing theory is finite, deterministic, and guaranteed-resolution, with unit costs in the sharp information-complexity results. Structural gaps are connected to selection or feedback through declared lifts rather than derived from a mechanistic physiological model. The sharp structural-temporal ceiling assumes a finite ergodic reversible community chain. The local feedback results concern deterministic linearization around an equilibrium and do not constitute a global bifurcation theory. The framework does not include mutation, migration, drift, multivariate quantitative genetics, demographic stochasticity, noisy cue likelihoods, or finite-sample inference.

These limitations define the current theorem rather than obvious targets for immediate extension. The main point is that even in this stripped-down setting, finite information structure is enough to impose nontrivial and sometimes sharp restrictions on evolutionary amplitudes, temporal fluctuation, and feedback reachability. Extensions to noisy or continuous sensing should therefore preserve the reachability question rather than simply add realism.

## Conclusion

Evolutionary time is often described in terms of how quickly traits change or how long those changes persist. The present results suggest a more structural perspective. Before asking how selection accumulates through time, one can ask what selection contrasts the organism's finite information system can generate at all. Before assigning a feedback phase, one can ask whether the required gain is compatible with the available information complexity. Finite information structure thereby becomes an upstream constraint on evolutionary time: it limits the amplitude that can be produced, the long-run fluctuation that can be sustained, and the feedback regimes that are reachable within the declared ecological system.
