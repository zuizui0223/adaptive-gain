# Preregisterable ecology experiment: information versus optimal waiting

**Status**: prospective experimental design, NOT a completed animal
experiment, NOT a fourth V6 main theorem, and NOT a claim that voluntary
information seeking has not previously been studied.

## Scientific question

Can an animal use an old ecological cue to decide whether to pay for
fresh information, and can the new cue affect *when the animal
acts* even when it does not change which immediate action would
be best?

The core alternative is a no-new-information controller that
already knows the old cue and can choose its action time optimally.
A credible positive answer requires beating that comparator,
not only an immediate fixed action, and ruling out the benefit
of waiting and the reward acquired while sampling itself.

## Prior-art positioning

- Dunlap, Papaj & Dornhaus (2017), Interface Focus,
  https://doi.org/10.1098/rsfs.2016.0149:
  bumblebees vary resource revisits with environmental persistence
  and payoff error costs. They already test the broad ecology of
  sampling a changing resource.
- He et al. (2026-09-22), bioRxiv preprint,
  https://doi.org/10.64898/2026.09.15.751944:
  bumblebees voluntarily visit a non-rewarding information platform,
  paying a sucrose-reward opportunity cost to obtain a cue.
  The public per-trial source
  https://github.com/Cuixiaojian21/bee_metacognition
  proves that the task is operationally feasible.
  In the authors' Free-Cue condition, receiving information is
  not the same variable as physically requesting it.
- Earlier time-memory and attention studies show that bee
  foraging timing and evidence inspection are already well
  studied; there is no priority claim for those individual
  behavioral capacities.

The untested *joint intervention*, not individual ingredients,
is the proposed novelty: an exogenously switching environmental
target, old and refreshed calibrated cues, a voluntary
re-query option, a no-information timing control and
post-query timing decisions within one design.

## Generative environmental process

On each independently randomized trial, simulate one of two
resource states X(t) in {0,1}. Assign the transition process
independently of the bee, with a logged continuous-time two-state
Markov transition generator (rates alpha and beta). Counterbalance
spatial side, cue identity and the reward assigned to each state.
Initial state at the old observation should be sampled from the
declared distribution. Log all state transitions; publish both
planned and realized transition logs.

The old cue O describes the state at time -tau; manipulate
tau with gate timing. Calibrate / manipulate old-cue error
separately from age.

The optional new visual cue Y is *non-rewarding and
non-invasive*: after the same fixed transit time r, it
reports the state at time r with independently imposed
misclassification probability epsilon. The cue port must
not allow inspection of the sucrose directly or alter
the two terminal resource states.

An animal may act immediately or wait in a predeclared
time window T, including **after it has seen Y**.
The target's state continues to change during all waiting.

The reward matrix and any incorrect-choice disutility
must be declared ex ante. The action-specific reward
contrast is not automatically reproductive fitness.

## Experimental interventions

Factorial experimental manipulations should separate:
(a) environmental persistence / transition rates,
(b) old-cue age and quality,
(c) new-cue accuracy,
(d) costs or opportunity penalties for re-query,
(e) whether query is voluntary,
(f) passive delay permitted before final action.

There must be at least three **same-timeline** intervention
conditions, randomized within a preregistered order:

1. PASSIVE: no refreshed information. The bee may
   choose when to make the terminal choice in [0,T].
2. SHAM QUERY: the same physical port, cue duration,
   light intensity, movement and handling, but the
   displayed label is sampled independently of X.
   This tests attraction and the timing/effort of
   approaching a port without gaining state information.
3. INFORMATIVE QUERY: the same port presents a label
   of current X at imposed error epsilon. No reward
   is dispensed at the port.

When estimating Bayes-optimal policy value rather than
merely observing natural preference, separately randomize
(or experimentally gate) the permissible waiting duration
to identify the response surface of reward versus elapsed
time. Observational waiting choices alone can confound
latent motivation and reward preference. In a later
free-choice phase, let each bee pick whether to request
and how long to wait.

Use the same no-query delay ceiling T for both arms,
and allow query arms the remaining horizon T-r after
the refreshed observation. This is stricter than forcing
the querying bee to act immediately after the cue.

## Two preregistered estimands

### E1. Information itself, at matched time

At fixed state transition schedule, old report O=o,
elapsed time and handling intervention, compare
expected terminal reward with an informative refreshed
cue against sham independent cue. This isolates the
added signal information conditional on the accessible
decision strategy, not "being in the port" or simply
allowing the environment to change.

The effect must be estimated on identical randomized
decision-time strata or with a valid sequential
randomization weighting scheme; conditioning only on
the realized, self-chosen waiting time may introduce
selection bias.

### E2. Conditional re-query policy premium

Estimate the optimized expected payoff for:
- P(o): no new cue, best old-report-dependent passive
  waiting/action policy;
- Q(o): buy a calibrated new cue, and thereafter optimize
  post-query timing/action using the two reports;
- C(o): choose max(P(o),Q(o)) after observing old report.

Predefine

G = E_o[max(P(o),Q(o))]
    - max(E_o[P(o)],E_o[Q(o)]).

G>0 establishes an ecological opportunity for
conditional acquisition relative to THESE two
declared comparator programs, not natural selection.
The per-query cost is included in Q and must not be
counted a second time. A constitutive control-cost
difference is a separate genetic / developmental
question.

Fit the candidate policies on training subjects/
sessions and evaluate them on untouched held-out
subjects/colonies with randomized data. Use
individual/colony cluster uncertainty. If any
reported positive policy value appears only when
the same trials both select and evaluate a policy,
treat it as exploration, not confirmation.

## Heterogeneous timing prediction

The dynamic theory contains an illustrative witness
with alpha=beta=.2, old-cue age=.1,
new sampling duration=.03, terminal delay=.02,
maximum wait=.5, opportunity hazard=.01,
correct-response reward contrasts r0:r1=1:4,
query cost K=.005, and new-cue error=.10.

After old report O=0, buying the new signal is preferred.
Both possible refreshed labels select action 0 if the
animal MUST choose immediately after the fixed terminal
delay. Yet the optimal **post-query waiting** differs:
d(Y=0)=0; d(Y=1)=.47. The latter delayed decision may
ultimately select a different final action after the
ecological state evolves. This is a mechanistic timing
prediction, not a claim that actual bees follow it.

Do not transplant these dimensionless parameters into
bee trials. Calibrate the relevant state switching,
sensory discrimination, survival and reward scales
independently before locking empirical predictions.

## Required data dictionary

Every individual encounter must retain at minimum:
- subject_id and colony_id, session_id, trial_id, block;
- randomized trial_type, quality assignment, old-cue age;
- timestamped true state sequence from experiment controller;
- old-cue label, old-cue presentation timestamp;
- query availability and query attempt/landing (not
  merely that information was delivered);
- refreshed label Y (or independent sham), cue delivery timestamp;
- query duration, any movement/sham handling time and cost;
- first eligible action time, chosen additional waiting duration,
  actual terminal action time and correct final state;
- final choice, reward/loss, failures/aborted opportunities;
- known assignment probabilities at every randomized stage.

The distinction between information DELIVERED versus actively
REQUESTED is mandatory; see
validation/bee_2026_active_information_schema_audit_v1.json.

## Falsification / failure gates

- A positive QUERY-versus-PASSIVE contrast that disappears
  against SHAM is evidence for timing/handling, not
  information.
- Absence of any old-cue-dependent query decision in held-out
  subjects falsifies that population's predicted
  selective-control mechanism under the tested conditions,
  even if the optimal mathematical policy has positive G.
- If absolute performance increases as a signal becomes
  strictly Blackwell less informative at fixed timing,
  cost and reward, the stated sensor-quality model fails
  or its manipulation was not a true garbling.
- If the supposedly non-invasive query changes the
  underlying resource or target state, the experiment
  identifies a sensing *intervention*, not an
  information-only effect.
- Strong positive values emerging only from in-sample
  policy fitting are not a biological replication.
- Absent heritable alternative architectures, constitutive
  control costs and reproductive consequences, no
  evolutionary selection coefficient is identified.

Status: PROSPECTIVE. No wet-lab execution, calibrated
natural parameters, effect-size pilot or defensible
sample-size target yet. Relevance to Evolution Letters
V6 is limited to prospective process interpretation;
do not expand its three frozen headline results.
