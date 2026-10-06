# Natural-history-dependent robust evolutionary resource frontier

Status: theorem extension on branch \`theory/opportunity-fitness-process-v1\`.

This note inverts the sharp value envelope.

The forward theorem asks:

> given finite information resources, how much biological value can adaptivity
> generate?

The inverse theorem asks:

> given the constitutive cost of adaptive control, how much information
> structure is minimally required before adaptivity has positive net value in
> every represented world, without knowing world frequencies?

This gives the earlier structural-gap thresholds a direct biological
microfoundation.

## 1. Setup

Let

\[
U(c)
\]

be any finite nonincreasing biological value of guaranteed completion at cost
\(c\).

Let

\[
K\ge0
\]

be the additive constitutive architecture cost of contingent control relative
to the declared universal fixed comparator.

For a task with completion costs \((C_A,C_F)\), define the robust worst-state
architecture margin

\[
\Phi_{\rm robust}
=
U(C_A)-U(C_F)-K.
\]

This is the net value guaranteed in the slowest adaptive branch relative to the
state-independent fixed bundle. It is not, in general, the expected value under
a particular world-frequency distribution.

Fix adaptive depth

\[
h=C_A.
\]

## 2. Required fixed burden at depth h

Define

\[
\boxed{
J_K(h)
=
\min
\left\{
j\in\mathbb Z_{\ge h}:
U(h)-U(j)>K
\right\},
}
\]

with

\[
J_K(h)=\infty
\]

if no such finite \(j\) exists.

\(J_K(h)\) is the minimum fixed completion cost that makes adaptive completion
at depth \(h\) worth its architecture cost.

Because \(U\) is nonincreasing,

\[
\boxed{
U(h)-U(j)>K
\iff
j\ge J_K(h)
}
\]

whenever \(J_K(h)<\infty\).

So the biology supplies a **depth-specific required fixed burden**.

## 3. Theorem RF1 — exact robust criterion inside a finite structural scope

For world count \(n\), query count \(m\), and maximum query arity \(b\), define

\[
I_h
=
\min\{m,F_b(n,h)\}.
\]

The sharp structural frontier gives the exact best fixed burden attainable at
adaptive depth \(h\):

\[
(C_A,C_F)=(h,I_h).
\]

Therefore positive **worst-state** architecture value exists at depth \(h\) if and only if

\[
\boxed{
I_h\ge J_K(h).
}
\]

Consequently a task with positive adaptive net value in every represented
world exists somewhere in the entire finite scope if and only if

\[
\boxed{
\exists h:
\min\{m,F_b(n,h)\}
\ge
J_K(h).
}
\]

This is equivalent to the forward condition

\[
K<K_{\rm crit}^{\rm robust},
\]

but it exposes the required structural resources rather than the maximum
payable architecture cost.

## 4. Two independent resource requirements

At one declared depth \(h\), the condition

\[
I_h\ge J_K(h)
\]

requires both

\[
\boxed{
m\ge J_K(h)
}
\]

and

\[
\boxed{
F_b(n,h)\ge J_K(h).
}
\]

Thus natural history creates a joint resource requirement:

- enough distinct query resources to make the fixed comparator sufficiently
  expensive; and
- enough represented-world/tree geometry to make that burden structurally
  realizable at depth \(h\).

This separates "more sensors" from "enough state structure for those sensors to
become branch-exclusive."

## 5. Exact binary resource corner

For binary queries,

\[
F_2(n,h)
=
\min(n-1,2^h-1).
\]

Let

\[
j_h=J_K(h)<\infty.
\]

A positive-value binary witness at depth \(h\) exists if and only if

\[
\boxed{
j_h\le 2^h-1.
}
\]

When this holds, the componentwise minimum world/query counts are

\[
\boxed{
n_h^*=j_h+1,
\qquad
m_h^*=j_h.
}
\]

The exact witness has

\[
(C_A,C_F)=(h,j_h).
\]

The overall binary evolutionary resource frontier is the nondominated set of

\[
\boxed{
(j_h+1,j_h)
}
\]

across feasible adaptive depths.

Unlike the old gap threshold, different depths can require different
\(j_h-h\).

## 6. Linear completion value recovers the old integer gap theorem

Take

\[
U(c)=-\lambda c,
\qquad
\lambda>0.
\]

Then

\[
U(h)-U(j)
=
\lambda(j-h).
\]

Positive architecture value requires

\[
\lambda(j-h)>K.
\]

Define

\[
\boxed{
q_K
=
\left\lfloor\frac{K}{\lambda}\right\rfloor+1.
}
\]

Then

\[
\boxed{
J_K(h)=h+q_K.
}
\]

The required gap is independent of absolute depth.

The binary resource corner becomes

\[
\boxed{
n_h^*=h+q_K+1,
\qquad
m_h^*=h+q_K,
}
\]

provided

\[
h+q_K\le2^h-1.
\]

Minimizing over \(h\) recovers the repository's earlier exact binary structural
corner for a required integer gap \(q\).

Thus the old \(q\)-threshold theorem is the constant-marginal-value special
case of RF1.

## 7. Exponential opportunity value makes the required gap depth dependent

Take

\[
U(c)=v e^{-\mu c},
\qquad
v>0,
\quad
\mu>0.
\]

At adaptive depth \(h\),

\[
U(h)-U(j)
=
v e^{-\mu h}
\left[
1-e^{-\mu(j-h)}
\right].
\]

A necessary condition for any finite fixed burden to pay architecture cost is

\[
\boxed{
K<v e^{-\mu h}.
}
\]

If this fails, then

\[
\boxed{
J_K(h)=\infty.
}
\]

So sufficiently deep adaptive routes cannot maintain positive **worst-state**
net value regardless of how expensive fixed resolution becomes. A skewed world
distribution can still produce positive expected value through earlier branches.

When

\[
K<v e^{-\mu h},
\]

define

\[
r_h
=
\frac{K e^{\mu h}}{v}
\in[0,1).
\]

The minimum required additive structural gap

\[
q_h=J_K(h)-h
\]

is

\[
\boxed{
q_h
=
\left\lfloor
-\frac{1}{\mu}
\log(1-r_h)
\right\rfloor
+1.
}
\]

Therefore

\[
\boxed{
J_K(h)
=
h+
\left\lfloor
-\frac{1}{\mu}
\log
\left(
1-\frac{K e^{\mu h}}{v}
\right)
\right\rfloor
+1.
}
\]

Unlike the linear model, the required gap increases with absolute adaptive
depth.

Natural history therefore penalizes "late savings": saving ten queries after an
already-long route can be less useful than saving a few queries early.

## 8. Corollary RF1.1 — exact maximum viable adaptive depth under exponential opportunity loss

A finite required fixed burden exists only if

\[
K<v e^{-\mu h}.
\]

Equivalently,

\[
h
<
\frac{1}{\mu}
\log\frac{v}{K}.
\]

For \(0<K<v\), the largest integer adaptive depth that can possibly repay the
architecture cost is

\[
\boxed{
h_{\max}^{\rm viable}
=
\left\lceil
\frac{1}{\mu}
\log\frac{v}{K}
\right\rceil
-1.
}
\]

This ceiling is independent of how many fixed query resources are available.

No amount of branch-exclusive fixed burden can rescue the **worst-state** margin
of an adaptive route whose guaranteed completion value has fallen below its
constitutive control cost.

## 9. Corollary RF1.2 — natural history turns one structural threshold into a Pareto set

Under a linear lift, one integer gap

\[
q_K
\]

summarizes the evolutionary requirement.

Under nonlinear time value, each adaptive depth has its own

\[
J_K(h).
\]

Therefore the minimum evolutionary architecture is generally not one scalar
complexity threshold.

It is a resource Pareto frontier over:

- adaptive depth;
- represented worlds;
- query resources;
- query arity.

This is the inverse form of the result that natural history re-ranks the exact
structural frontier.




## 8b. Exact bounded-arity depth corner

The binary closed form is a special case of an exact bounded-arity construction.

For a declared adaptive depth \(h\), let

\[
j_h=J_K(h).
\]

Positive value at that depth is possible only if

\[
j_h
\le
J_b(h)
=
\frac{b^h-1}{b-1},
\]

the full \(b\)-ary internal-node ceiling.

When this holds, define

\[
\boxed{
n_b^*(h,j_h)
=
\min
\left\{
n:
F_b(n,h)\ge j_h
\right\}.
}
\]

Then the exact componentwise minimum resource requirements at that depth are

\[
\boxed{
n=n_b^*(h,j_h),
\qquad
m=j_h.
}
\]

The protected-spine witness at those counts attains

\[
(C_A,C_F)=(h,j_h)
\]

and therefore positive net architecture value.

This provides an exact finite algorithm for the evolutionary resource frontier
at arbitrary bounded cue arity.

### Arity changes the minimum viable sensing depth

Take again

\[
U(c)=e^{-0.3c},
\qquad
K=0.25.
\]

At depth \(h=2\),

\[
J_K(2)=5.
\]

Binary and ternary trees satisfy

\[
J_2(2)=3,
\qquad
J_3(2)=4,
\]

so neither can generate enough fixed burden at two adaptive steps.

But for four-outcome cues,

\[
J_4(2)=5,
\]

so depth two becomes feasible.

The exact minimum resources are

\[
\boxed{
b=4:
\quad
h=2,\ n=8,\ m=5.
}
\]

By contrast, for \(b=2\) or \(b=3\), the first viable depth is

\[
\boxed{
h=3,\ n=8,\ m=7.
}
\]

Thus increased cue arity can reduce both the minimum adaptive depth and the
number of distinct query resources required to pay the same constitutive
control cost.

The claim is about the declared discrete query model. It should not be read as
a universal prediction that sensory systems with more receptor states are
always fitter.


## 9a. Canonical binary example — natural history creates a minimum information architecture

Take

\[
U(c)=e^{-0.3c},
\qquad
K=0.25,
\qquad
b=2.
\]

The depth-specific requirements are:

| adaptive depth \(h\) | available value \(U(h)\) | required gap \(q_h\) | required fixed cost \(J_K(h)\) | binary ceiling \(2^h-1\) | result |
| ---: | ---: | ---: | ---: | ---: | --- |
| 1 | 0.741 | 2 | 3 | 1 | structurally impossible |
| 2 | 0.549 | 3 | 5 | 3 | structurally impossible |
| 3 | 0.407 | 4 | 7 | 7 | feasible |
| 4 | 0.301 | 6 | 10 | 15 | feasible but larger |
| 5 | 0.223 | — | \(\infty\) | 31 | biologically unviable |

Thus the first feasible binary architecture occurs exactly at

\[
\boxed{
h=3,
\qquad
C_F=7.
}
\]

The minimum world/query counts are

\[
\boxed{
n_{\min}=8,
\qquad
m_{\min}=7.
}
\]

This example shows two different failure mechanisms on opposite sides of the
viable region:

- shallow routing fails because binary structure cannot make fixed resolution
  expensive enough;
- deep routing fails because too little biological value remains by the time
  the adaptive route finishes.

The evolvable architecture therefore occupies an intermediate structural
window generated jointly by cue arity and natural-history time value.


## 9b. Theorem RF2 — cue arity creates an absolute robust-cost ceiling

The previous results fixed world count and query count.

Now allow both to grow without bound while keeping only one structural
restriction:

\[
\operatorname{arity}(q)\le b,
\qquad
b\ge2.
\]

For an adaptive tree of depth \(h\), the maximum possible number of internal
node occurrences in a full \(b\)-ary tree is

\[
\boxed{
J_b(h)
=
1+b+b^2+\cdots+b^{h-1}
=
\frac{b^h-1}{b-1}.
}
\]

Therefore every finite task with query arity at most \(b\) and

\[
C_A=h
\]

satisfies

\[
\boxed{
C_F\le J_b(h).
}
\]

The full \(b\)-ary private-pair construction attains

\[
\boxed{
(C_A,C_F)
=
(h,J_b(h))
}
\]

using \(b^h\) represented leaves and \(J_b(h)\) query resources.

Hence for any finite nonincreasing completion value \(U\) that is bounded
below, the maximum architecture benefit over **all finite tasks of arbitrary
size** with cue arity at most \(b\) is

\[
\boxed{
K_{\rm crit,robust}^{(b)}
=
\max_{h\ge2}
\left[
U(h)-U(J_b(h))
\right].
}
\]

Depth \(h=1\) is excluded because strict adaptive advantage is impossible when
one query already resolves the target: the same query is a fixed resolver.

Therefore

\[
\boxed{
K>K_{\rm crit,robust}^{(b)}
\Longrightarrow
\text{no finite task with arity }\le b\text{ can guarantee positive net adaptive value in every world.}
}
\]

This **robust no-go** is independent of world count and query count.

Adding more ecological states or more sensor resources cannot overcome a
control cost above the arity-limited ceiling if positive value is required in
every represented world. It does not exclude positive expected value under a
specific nonuniform encounter distribution.

## Corollary RF2.1 — binary cues impose a global robust-value ceiling

For \(b=2\),

\[
J_2(h)=2^h-1.
\]

Thus

\[
\boxed{
K_{\rm crit,robust}^{(2)}
=
\max_{h\ge2}
\left[
U(h)-U(2^h-1)
\right].
}
\]

For exponential opportunity value

\[
U(c)=v e^{-\mu c},
\]

\[
\boxed{
K_{\rm crit}^{(2)}
=
v
\max_{h\ge2}
\left[
e^{-\mu h}
-
e^{-\mu(2^h-1)}
\right].
}
\]

At

\[
\mu=0.3,
\qquad
v=1,
\]

the maximum occurs at

\[
h=4
\]

and equals approximately

\[
\boxed{
K_{\rm crit,robust}^{(2)}
=
0.290085.
}
\]

Therefore a binary-cue contingent-control architecture with additive
constitutive cost

\[
K\ge0.290085
\]

cannot have positive **statewise guaranteed** net value through this mechanism
in any finite deterministic binary task, no matter how many worlds or binary
queries are supplied.

This explains the example \(K=0.30\): the failure is not caused by insufficient
sample size of the finite task. It is an arity-limited global no-go.

## Corollary RF2.2 — increasing cue arity raises the maximum robustly payable control cost

For fixed \(h\),

\[
J_{b+1}(h)\ge J_b(h).
\]

Since \(U\) is nonincreasing,

\[
U(h)-U(J_{b+1}(h))
\ge
U(h)-U(J_b(h)).
\]

Therefore

\[
\boxed{
K_{\rm crit,robust}^{(b+1)}
\ge
K_{\rm crit,robust}^{(b)}.
}
\]

Higher-outcome cues can never reduce the maximum constitutive control cost that
some finite task can pay while keeping the net advantage positive in every
represented world.

This is a structural statement about declared query arity, not a claim that
real sensory systems should evolve arbitrarily high categorical resolution.

## Corollary RF2.3 — even unlimited cue arity has a robust natural-history ceiling

Every strict adaptive advantage requires

\[
C_A\ge2.
\]

Let

\[
U_\infty
=
\lim_{c\to\infty}U(c),
\]

which exists and is finite under the bounded-below scope of RF2.

Then for every finite task,

\[
U(C_A)-U(C_F)
\le
U(2)-U_\infty.
\]

As cue arity, represented worlds and fixed resources grow, depth-two
constructions can make \(C_F\) arbitrarily large. Hence

\[
\boxed{
\sup_{\text{all finite tasks}}
\left[
U(C_A)-U(C_F)
\right]
=
U(2)-U_\infty.
}
\]

For exponential opportunity value,

\[
U_\infty=0,
\]

so the absolute architecture-cost ceiling is

\[
\boxed{
K_{\rm crit,robust}^{(\infty)}
=
v e^{-2\mu}.
}
\]

At \(\mu=0.3,\ v=1\),

\[
K_{\rm crit,robust}^{(\infty)}
=
e^{-0.6}
\approx
0.548812.
\]

Thus even infinitely rich finite information architecture cannot **guarantee
statewise repayment** of a constitutive contingent-control cost above the
biological value remaining after the minimum two-step strict-routing
architecture.


## Corollary RF2.3a — exact minimum cue arity required for robust repayment

For a bounded-below nonincreasing completion value \(U\), define

\[
K_{\rm crit,robust}^{(b)}
=
\max_{h\ge2}
\left[
U(h)-U(J_b(h))
\right].
\]

Because this ceiling is nondecreasing in \(b\), define

\[
\boxed{
b_{\min}(K;U)
=
\min
\left\{
b\ge2:
K<K_{\rm crit,robust}^{(b)}
\right\},
}
\]

with \(b_{\min}=\infty\) if the set is empty.

Then

\[
\boxed{
b<b_{\min}
\Longrightarrow
\text{no finite task with cue arity }b
\text{ can guarantee positive net value in every world},
}
\]

whereas every

\[
b\ge b_{\min}
\]

admits a finite constructive witness with robust positive architecture value.

For exponential opportunity value,

\[
U(c)=v e^{-\mu c},
\]

the unrestricted-information robust supremum is

\[
K_{\rm crit,robust}^{(\infty)}
=
v e^{-2\mu}.
\]

Hence

\[
\boxed{
K\ge v e^{-2\mu}
\Longrightarrow
b_{\min}=\infty.
}
\]

No finite cue arity, number of worlds, or number of query resources can
guarantee statewise repayment of such an expensive contingent-control
architecture.

Conversely, if

\[
K<v e^{-2\mu},
\]

then \(b_{\min}<\infty\), because the depth-two robust value

\[
v
\left[
e^{-2\mu}
-
e^{-\mu(b+1)}
\right]
\]

approaches \(v e^{-2\mu}\) as \(b\to\infty\).

### Canonical example

At

\[
\mu=0.3,\qquad v=1,
\]

the robust arity ceilings include

\[
K_{\rm crit,robust}^{(2)}
\approx0.290085
\]

and

\[
K_{\rm crit,robust}^{(3)}
\approx0.386328.
\]

Therefore for

\[
K=0.30,
\]

\[
\boxed{
b_{\min}=3.
}
\]

No binary finite task can guarantee repayment of the control cost, regardless
of how many worlds or binary query resources are added, whereas a ternary task
can.

Cue arity here means the maximum number of distinguishable outcomes of one
declared query in the finite model. It is not a direct proxy for receptor
number or sensory-organ complexity.


## Corollary RF2.4 — sensory complexity and natural history jointly bound robust evolvability

The hierarchy is now

\[
K_{\rm crit}^{\rm robust}(n,m,b;U)
\le
K_{\rm crit,robust}^{(b)}(U)
\le
U(2)-U_\infty.
\]

The three ceilings correspond to:

1. a particular finite ecological information budget;
2. unlimited task size but bounded cue arity;
3. unlimited finite information structure.

So failure of **distribution-free robust** adaptive value can arise at three distinct levels:

- not enough worlds/resources in the focal system;
- cue arity too restrictive;
- or natural history itself leaves too little value after the minimum strict
  adaptive decision depth.



## 9c. Theorem RF3 — finite-scope and scalable-scope robust low-urgency limits differ

For one fixed finite structural scope \((n,m,b)\), exponential opportunity value

\[
U_\mu(c)=v e^{-\mu c}
\]

gives

\[
R_{\max}(n,m,b;\mu)\to0
\qquad
\text{as}
\qquad
\mu\to0^+.
\]

This is because all relevant completion costs remain finite, so both adaptive
and fixed resolution eventually occur before appreciable value is lost.

The conclusion changes if task size is allowed to scale while cue arity remains
fixed.

Let

\[
K_{\rm crit,robust}^{(b)}(\mu)
=
v
\max_{h\ge2}
\left[
e^{-\mu h}
-
e^{-\mu J_b(h)}
\right].
\]

Then for every fixed

\[
b\ge2,
\]

\[
\boxed{
K_{\rm crit,robust}^{(b)}(\mu)\to v
\qquad
\text{as}
\qquad
\mu\to0^+.
}
\]

### Proof

The upper bound

\[
K_{\rm crit,robust}^{(b)}(\mu)\le v
\]

is immediate.

For a lower bound, choose any integer depth sequence satisfying

\[
h(\mu)
=
\left\lceil
2\log_b\frac1\mu
\right\rceil
\]

for sufficiently small \(\mu\).

Then

\[
\mu h(\mu)\to0,
\]

so

\[
e^{-\mu h(\mu)}\to1.
\]

Also

\[
b^{h(\mu)}
\ge
\mu^{-2},
\]

hence

\[
\mu J_b(h(\mu))
\ge
\frac{\mu(\mu^{-2}-1)}{b-1}
\to\infty.
\]

Therefore

\[
e^{-\mu J_b(h(\mu))}\to0.
\]

The attainable value along this sequence tends to \(v\), proving the result.

## Corollary RF3.1 — the low-urgency and large-complexity limits do not commute

For every fixed finite \(n,m\),

\[
\lim_{\mu\to0^+}
R_{\max}(n,m,b;\mu)
=
0.
\]

Therefore

\[
\sup_{n,m}
\lim_{\mu\to0^+}
R_{\max}(n,m,b;\mu)
=
0.
\]

But RF3 gives

\[
\boxed{
\lim_{\mu\to0^+}
\sup_{n,m}
R_{\max}(n,m,b;\mu)
=
v.
}
\]

Thus

\[
\boxed{
\sup_{n,m}\lim_{\mu\to0}R_{\max}
\neq
\lim_{\mu\to0}\sup_{n,m}R_{\max}.
}
\]

### Biological interpretation

Weak time pressure does not intrinsically eliminate the value of adaptivity.

It eliminates that value in a **fixed finite task**.

If ecological decision complexity itself scales with the available time
horizon, an adaptive architecture can use deeper routing while forcing fixed
resolution to provision an exponentially larger set of branch-specific
resources.

Even binary cues can then recover nearly the full value \(v\).

This is an asymptotic capacity result, not a claim that real ecological systems
increase task complexity without bound as opportunities become longer.

## Corollary RF3.2 — high urgency always destroys the arity-limited ceiling

For fixed \(b\),

\[
K_{\rm crit,robust}^{(b)}(\mu)
\le
v e^{-2\mu},
\]

because every strict adaptive advantage requires \(h\ge2\).

Therefore

\[
\boxed{
K_{\rm crit,robust}^{(b)}(\mu)\to0
\qquad
\text{as}
\qquad
\mu\to\infty.
}
\]

So unlimited task complexity can rescue adaptive value under arbitrarily weak
urgency, but not under arbitrarily severe urgency.



## 9d. Expected-value escape from the robust frontier

The resource thresholds above answer a frequency-free question.

They do **not** give the minimum architecture required for positive expected
selection under a declared world distribution.

For an adaptive policy \(\pi\),

\[
R_{\rm expected}
=
\sum_x p_x U[T_\pi(x)]
-
U(C_F).
\]

Because

\[
T_\pi(x)\le C_A
\]

for a minimax-optimal tree,

\[
R_{\rm expected}
\ge
U(C_A)-U(C_F)
=
R_{\rm robust}.
\]

Therefore a robustly viable architecture is viable in expectation under every
world distribution.

But the converse need not hold.  If common worlds terminate early while rare
worlds determine \(C_A\), then

\[
R_{\rm expected}>K
\]

can occur even when

\[
R_{\rm robust}\le K.
\]

Hence the present inverse frontier is an exact **distribution-free sufficient
and necessary frontier for statewise positive value**, not an expected-fitness
no-go.

The expected-value inverse problem additionally requires:

- world frequencies \(p_x\);
- branch-specific completion costs;
- the fitness-optimal rather than merely minimax routing policy.

Those objects belong to the separate policy-fitness layer.




## Corollary RF3.3 — architecture switching can create re-entrant urgency windows

For one fixed adaptive depth \(h\), the exponential robust benefit at cue arity
\(b\) is

\[
G_h(\mu)
=
v
\left[
e^{-\mu h}
-
e^{-\mu J_b(h)}
\right].
\]

Because

\[
J_b(h)>h
\]

for every strict adaptive case, \(G_h\) is zero at both urgency extremes and
has one unique maximum at

\[
\boxed{
\mu_h^*
=
\frac{\log[J_b(h)/h]}
{J_b(h)-h}.
}
\]

Thus for a declared control cost \(0<K<\max_\mu G_h(\mu)\), one depth is viable
over one open urgency interval.

But the scalable arity-limited ceiling is the upper envelope

\[
K_{\rm crit,robust}^{(b)}(\mu)
=
\max_{h\ge2}G_h(\mu).
\]

A maximum of unimodal depth-specific curves need not itself be monotone or
unimodal. Consequently the set

\[
\boxed{
\left\{
\mu>0:
K<K_{\rm crit,robust}^{(b)}(\mu)
\right\}
}
\]

can be a union of multiple disjoint intervals.

### Explicit re-entrant witness

Take

\[
b=10,\qquad v=1,\qquad K=0.97630.
\]

Direct evaluation of the exact depth envelope gives:

\[
\mu=0.0045:
\quad
K_{\rm crit,robust}^{(10)}
\approx0.977751>K,
\]

\[
\mu=0.0048:
\quad
K_{\rm crit,robust}^{(10)}
\approx0.976286<K,
\]

\[
\mu=0.0051:
\quad
K_{\rm crit,robust}^{(10)}
\approx0.976345>K,
\]

and

\[
\mu=0.006:
\quad
K_{\rm crit,robust}^{(10)}
\approx0.975012<K.
\]

Therefore increasing urgency produces the sequence

\[
\boxed{
\text{robustly feasible}
\to
\text{infeasible}
\to
\text{robustly feasible}
\to
\text{infeasible}.
}
\]

The re-entry occurs because the maximizing architecture switches from a deeper
routing tree to a shallower one. It is a discrete architecture-switching
effect, not a violation of the single-depth unimodality theorem.

This result should remain supplementary. Its role is to prevent the stronger
but false claim that the scalable robust cost ceiling must decrease
monotonically with ecological urgency.



## Corollary RF3.3 — finite-resource band-pass can disappear when ecological complexity is scalable

The finite-scope and scalable-scope limits imply a qualitative difference in
selection geometry.

Fix

\[
U_\mu(c)=v e^{-\mu c}
\]

and a positive robust architecture cost

\[
0<K<v.
\]

### Fixed finite structural scope

For any fixed finite

\[
(n,m,b),
\]

the robust value ceiling satisfies

\[
K_{\rm crit,robust}(n,m,b;\mu)
\to0
\]

as both

\[
\mu\to0^+
\]

and

\[
\mu\to\infty.
\]

Therefore if the ceiling exceeds \(K\) at some intermediate \(\mu\), robust
positive adaptive value can occur only inside bounded intermediate-urgency
regions.

This is the finite-resource band-pass effect.

### Scalable task size at fixed cue arity

If \(n\) and \(m\) may grow while cue arity \(b\) remains fixed, RF3 gives

\[
K_{\rm crit,robust}^{(b)}(\mu)
\to v
\qquad
\text{as}
\qquad
\mu\to0^+.
\]

Hence every

\[
K<v
\]

is robustly repayable for sufficiently weak urgency by some sufficiently large
finite task.

High urgency still destroys the ceiling:

\[
K_{\rm crit,robust}^{(b)}(\mu)
\to0
\qquad
\text{as}
\qquad
\mu\to\infty.
\]

Thus the low-urgency loss of adaptive value is not universal. It is a
**finite-resource effect**.

## Canonical binary contrast

Take

\[
v=1,
\qquad
K=0.25,
\qquad
b=2.
\]

For the fixed finite scope

\[
n=10,
\qquad
m=9,
\]

the exact robust ceiling crosses \(K\) at approximately

\[
\boxed{
\mu_{\rm low}=0.0877299
}
\]

and

\[
\boxed{
\mu_{\rm high}=0.379725.
}
\]

So robust positive value is available only for

\[
\boxed{
0.0877299<\mu<0.379725.
}
\]

At very weak urgency the finite task cannot create enough fixed burden before
both architectures become effectively timely.

Now allow arbitrary finite world/query counts while retaining binary cues.

The binary global ceiling satisfies

\[
K_{\rm crit,robust}^{(2)}(\mu)>0.25
\]

for all sufficiently small positive \(\mu\), and crosses \(0.25\) only at

\[
\boxed{
\mu\approx0.379725.
}
\]

Hence in the scalable binary class,

\[
\boxed{
0<\mu<0.379725
}
\]

admits some finite task with positive robust value.

The upper threshold is the same in this example because at that urgency the
finite \((10,9)\) scope already contains the globally maximizing binary depth.
The low threshold disappears because larger tasks can exploit longer
opportunity windows.

### Biological interpretation

The prediction is not simply

> intermediate time pressure favors flexibility.

It is conditional:

> intermediate time pressure favors flexibility when the ecological decision
> problem itself is held finite.

If longer opportunity windows are accompanied by proportionally richer
branch-specific alternatives, contingent sensing can remain valuable even when
time pressure is weak.

This distinction is especially important when comparing ecological systems
that differ simultaneously in opportunity duration and interaction
complexity.


## 9e. Theorem RF4 — retaining a fixed fraction of adaptive value has a sharp complexity scale

RF3 proves that, at fixed cue arity \(b\), the maximum opportunity value can
approach the full timely-resolution value \(v\) as

\[
\mu\to0^+
\]

provided task complexity is allowed to grow.

The next question is how fast that complexity must grow.

Fix:

\[
b\ge2,
\qquad
0<\varepsilon<1,
\]

and require a task to attain at least a fraction

\[
1-\varepsilon
\]

of the maximum possible timely-resolution value:

\[
R_{\rm opp}
\ge
(1-\varepsilon)v.
\]

Assume

\[
U_\mu(c)=v e^{-\mu c}.
\]

### Necessary conditions

Let a task have

\[
C_A=h,
\qquad
C_F=j.
\]

The requirement

\[
e^{-\mu h}-e^{-\mu j}
\ge
1-\varepsilon
\]

implies separately

\[
e^{-\mu h}
\ge
1-\varepsilon,
\]

hence

\[
\boxed{
h
\le
\frac{-\log(1-\varepsilon)}{\mu}.
}
\]

It also implies

\[
e^{-\mu j}
\le
\varepsilon,
\]

because \(e^{-\mu h}\le1\). Therefore

\[
\boxed{
j
\ge
\frac{\log(1/\varepsilon)}{\mu}.
}
\]

Since

\[
C_F\le m
\]

and every finite solvable task satisfies

\[
C_F\le n-1,
\]

one necessarily has

\[
\boxed{
m
\ge
\frac{\log(1/\varepsilon)}{\mu},
}
\]

and

\[
\boxed{
n
\ge
1+
\frac{\log(1/\varepsilon)}{\mu}.
}
\]

Bounded cue arity also gives

\[
j
\le
J_b(h)
=
\frac{b^h-1}{b-1}.
\]

Therefore

\[
\boxed{
h
\ge
\log_b
\left[
1+
\frac{(b-1)\log(1/\varepsilon)}{\mu}
\right].
}
\]

So any near-maximal-value architecture must satisfy the asymptotic lower bounds

\[
\boxed{
C_A
=
\Omega(\log(1/\mu)),
}
\]

and

\[
\boxed{
C_F,\ n,\ m
=
\Omega(1/\mu).
}
\]

These are lower bounds only.  They do not say that every architecture meeting
the value target has adaptive depth of order \(\log(1/\mu)\); deeper
architectures can also satisfy the target when their completion value remains
high enough.

### Matching construction

Now set

\[
L_\varepsilon
=
\log\frac{2}{\varepsilon}
\]

and choose

\[
\boxed{
h_\mu
=
\left\lceil
\log_b
\left[
1+
\frac{(b-1)L_\varepsilon}{\mu}
\right]
\right\rceil.
}
\]

Use the full \(b\)-ary private-pair witness, so

\[
C_A=h_\mu,
\]

\[
C_F=J_b(h_\mu),
\]

\[
n=b^{h_\mu},
\]

and

\[
m=J_b(h_\mu).
\]

By construction,

\[
J_b(h_\mu)
\ge
\frac{L_\varepsilon}{\mu},
\]

so

\[
e^{-\mu C_F}
\le
\frac{\varepsilon}{2}.
\]

If

\[
\mu h_\mu
\le
-\log(1-\varepsilon/2),
\]

which holds for all sufficiently small \(\mu\), then

\[
e^{-\mu C_A}
\ge
1-\frac{\varepsilon}{2}.
\]

Therefore

\[
\boxed{
R_{\rm opp}
\ge
(1-\varepsilon)v.
}
\]

Moreover, because

\[
b^{h_\mu}
<
b
\left[
1+
\frac{(b-1)L_\varepsilon}{\mu}
\right],
\]

the construction has

\[
\boxed{
n
=
O(1/\mu),
}
\]

\[
\boxed{
m
=
O(1/\mu),
}
\]

and

\[
\boxed{
C_A
=
O(\log(1/\mu)).
}
\]

Combining the lower bounds with the explicit construction gives tight orders
for the **minimum resource scale needed to make the target value attainable**:

\[
\boxed{
C_{A,\min}^{\rm attainable}
=
\Theta(\log(1/\mu)),
}
\]

and

\[
\boxed{
C_{F,\min}^{\rm attainable},\ 
n_{\min}^{\rm attainable},\ 
m_{\min}^{\rm attainable}
=
\Theta(1/\mu).
}
\]

Equivalently, there exist near-maximal-value constructions at these orders, and
no construction can achieve the target with asymptotically smaller adaptive
depth, fixed burden, world count, or query count.  This is not a statement that
all architectures achieving the target have those orders.

## Corollary RF4.1 — why weak urgency can still favor adaptivity in scalable environments

The scaling law identifies the mechanism behind RF3.

As ecological opportunities become longer:

- the adaptive route may deepen only logarithmically;
- the fixed architecture must provision a number of branch-specific resources
  proportional to the opportunity timescale \(1/\mu\).

For the explicit order-optimal construction above, the structural ratio scales
as

\[
\boxed{
\frac{C_F}{C_A}
=
\Theta
\left(
\frac{1}
{\mu\log(1/\mu)}
\right).
}
\]

The same expression is the ratio of the minimum fixed-burden scale to the
minimum adaptive-depth scale.  It is not asserted as the ratio of every
near-maximal-value architecture.

The noncommuting low-urgency limit is therefore generated by a mismatch between

\[
\text{logarithmic routing depth}
\]

and

\[
\text{linear simultaneous provisioning burden}.
\]

This gives RF3 a process interpretation rather than leaving it as an
asymptotic curiosity.

## Corollary RF4.2 — near-maximal adaptive value requires ecological complexity to track opportunity duration

Because the **minimum required resource scale** obeys

\[
n_{\min},m_{\min}=\Theta(1/\mu),
\]

a fixed finite environment cannot retain near-maximal robust routeability value
as the opportunity timescale diverges.

The number of ecologically distinguishable alternatives and/or branch-specific
information resources must grow on the same order as the characteristic
opportunity timescale.

This is an asymptotic capacity statement. It is not a claim that real
communities literally tune species richness or receptor number to \(1/\mu\).



## 9f. Theorem RF5 — expected-value capacity exceeds the robust ceiling by one decision step

The scalable robust frontier asks for positive net value in **every** represented
world.

If encounter frequencies are allowed to be nonuniform, the absolute expected-
value capacity is larger.

Assume \(U(c)\) is finite, nonincreasing, and bounded below, with

\[
U_\infty
=
\lim_{c\to\infty}U(c).
\]

Fix any cue-arity bound

\[
b\ge2.
\]

Consider all finite nontrivial tasks with query arity at most \(b\), all
guaranteed-resolving adaptive policies, and all strictly positive world-
frequency distributions.

Define

\[
R_{\rm expected}
=
\sum_x p_xU[T_\pi(x)]
-
U(C_F).
\]

Then

\[
\boxed{
\sup R_{\rm expected}
=
U(1)-U_\infty.
}
\]

### Upper bound

A nontrivial task contains at least two target classes, so before any query is
taken the target is unresolved.

Therefore every realized adaptive path satisfies

\[
T_\pi(x)\ge1.
\]

Since \(U\) is nonincreasing,

\[
U[T_\pi(x)]
\le
U(1)
\]

for every world, and hence

\[
\sum_xp_xU[T_\pi(x)]
\le
U(1).
\]

Also

\[
U(C_F)\ge U_\infty.
\]

Thus

\[
\boxed{
R_{\rm expected}
\le
U(1)-U_\infty.
}
\]

### Matching construction

Take a binary root query with:

- one target-pure leaf that terminates after the root query;
- one remaining branch containing an increasingly large private-pair routing
  subtree.

The full tree is a valid binary task and hence is admissible under every
\(b\ge2\).

Let the shallow leaf have encounter probability

\[
1-\delta
\]

and distribute total probability \(\delta>0\) over the remaining worlds.

As the rare subtree grows,

\[
C_F\to\infty,
\]

so

\[
U(C_F)\to U_\infty.
\]

As

\[
\delta\to0^+,
\]

the adaptive expected value tends to

\[
U(1).
\]

Therefore the upper bound is approached arbitrarily closely:

\[
\boxed{
\sup R_{\rm expected}
=
U(1)-U_\infty.
}
\]

The result is a supremum because every represented world may be required to
retain positive probability.

## Corollary RF5.1 — robust and expected global ceilings differ

From RF2.3,

\[
\sup R_{\rm robust}
=
U(2)-U_\infty.
\]

From RF5,

\[
\sup R_{\rm expected}
=
U(1)-U_\infty.
\]

Therefore

\[
\boxed{
\sup R_{\rm expected}
-
\sup R_{\rm robust}
=
U(1)-U(2)
\ge0.
}
\]

The gap is the maximum possible contribution of concentrating encounters on a
branch that terminates one query earlier than any strict worst-case adaptive
architecture can guarantee.

For exponential opportunity value,

\[
U(c)=v e^{-\mu c},
\]

\[
\boxed{
K_{\rm crit,robust}^{(\infty)}
=
v e^{-2\mu},
}
\]

whereas

\[
\boxed{
K_{\rm crit,expected}^{(\infty)}
=
v e^{-\mu}.
}
\]

At

\[
\mu=0.3,\qquad v=1,
\]

these are

\[
K_{\rm crit,robust}^{(\infty)}
\approx0.548812
\]

and

\[
K_{\rm crit,expected}^{(\infty)}
\approx0.740818.
\]

## Corollary RF5.2 — frequency-assisted evolvability band

If architecture cost satisfies

\[
\boxed{
U(2)-U_\infty
\le
K
<
U(1)-U_\infty,
}
\]

then:

- no finite information architecture can guarantee positive net value in every
  represented world;
- but some finite **binary** architecture can have positive expected net value
  under a sufficiently skewed encounter distribution.

For exponential opportunity value,

\[
\boxed{
v e^{-2\mu}
\le
K
<
v e^{-\mu}
}
\]

is therefore a frequency-assisted evolvability band.

Example:

\[
\mu=0.3,\qquad v=1,\qquad K=0.60.
\]

Since

\[
0.548812
<
0.60
<
0.740818,
\]

robust repayment is impossible even with unlimited finite cue arity and task
size, yet positive expected selection remains constructively possible with
binary cues if one early-terminating state dominates encounter frequency.

This is not a contradiction. The robust theorem is distribution-free; the
expected theorem uses ecological frequency concentration as an additional
resource.



## 9f. Theorem RF5 — robust and expected selection have different absolute information ceilings

The robust frontier asks whether contingent sensing has positive net value in
every represented world.

Expected selection asks only whether the world-frequency-weighted mean benefit
is positive.

These two questions have different absolute ceilings even when all finite
information structure is allowed.

Let \(U(c)\) be bounded below and nonincreasing, with

\[
U_\infty
=
\lim_{c\to\infty}U(c).
\]

### Robust ceiling

From RF2.3,

\[
\boxed{
\sup_{\text{all finite tasks}}
R_{\rm robust}
=
U(2)-U_\infty.
}
\]

The minimum worst-path depth supporting strict adaptive advantage is two.

### Expected ceiling

Now allow an arbitrary world-frequency distribution with strictly positive
probabilities that may be arbitrarily skewed.

For any nontrivial adaptive decision task, every realized policy must acquire
at least one query before resolving the target, so

\[
T_\pi(x)\ge1
\]

for every represented world.

Therefore

\[
\sum_xp_xU[T_\pi(x)]
\le
U(1).
\]

Also

\[
U(C_F)\ge U_\infty.
\]

Hence every expected adaptive advantage satisfies

\[
\boxed{
R_{\rm expected}
\le
U(1)-U_\infty.
}
\]

This upper bound is a supremum and is sharp.

### Sharpness construction

Take a binary root query with:

- one target-pure branch containing a focal common world;
- one rare branch containing an arbitrarily large finite routing task whose
  fixed burden tends to infinity.

Let the common world have probability

\[
1-\delta
\]

and distribute total probability \(\delta>0\) across the rare branch.

The adaptive policy resolves the common world after one query.

As the rare subtask grows,

\[
C_F\to\infty,
\]

and as

\[
\delta\to0^+,
\]

the expected adaptive completion value tends to

\[
U(1),
\]

while fixed completion value tends to

\[
U_\infty.
\]

Therefore

\[
\boxed{
\sup_{\substack{\text{finite tasks}\\\text{positive world frequencies}}}
R_{\rm expected}
=
U(1)-U_\infty.
}
\]

The supremum need not be attained by one finite task with all world
probabilities strictly positive.

## Corollary RF5.1 — encounter-frequency skew creates a selection regime unavailable to robust architecture

Let architecture cost be \(K\).

If

\[
K<U(2)-U_\infty,
\]

some finite architecture can have positive net value robustly in every world.

If

\[
\boxed{
U(2)-U_\infty
\le
K
<
U(1)-U_\infty,
}
\]

then no finite information architecture can guarantee positive net value in
every represented world, but some finite task with sufficiently skewed encounter
frequencies can have positive expected net value.

If

\[
K\ge U(1)-U_\infty,
\]

then even arbitrarily skewed expected selection cannot repay the control cost
through completion-time advantage alone.

Thus encounter frequencies create an exact three-regime decomposition:

\[
\boxed{
\begin{array}{ll}
K<U(2)-U_\infty
&
\text{robust and expected repayment are both possible},
\\[4pt]
U(2)-U_\infty\le K<U(1)-U_\infty
&
\text{expected repayment only},
\\[4pt]
K\ge U(1)-U_\infty
&
\text{neither is possible}.
\end{array}
}
\]

## Corollary RF5.2 — exponential opportunity value

For

\[
U(c)=v e^{-\mu c},
\]

\[
U_\infty=0.
\]

Therefore the unrestricted robust ceiling is

\[
\boxed{
K_{\rm robust}^{\sup}
=
v e^{-2\mu},
}
\]

whereas the unrestricted expected ceiling is

\[
\boxed{
K_{\rm expected}^{\sup}
=
v e^{-\mu}.
}
\]

The expected ceiling exceeds the robust ceiling by

\[
\boxed{
v(e^{-\mu}-e^{-2\mu}),
}
\]

and their ratio is

\[
\boxed{
\frac{K_{\rm expected}^{\sup}}
{K_{\rm robust}^{\sup}}
=
e^\mu.
}
\]

At

\[
\mu=0.3,
\qquad
v=1,
\]

\[
K_{\rm robust}^{\sup}
\approx0.548812,
\]

while

\[
K_{\rm expected}^{\sup}
\approx0.740818.
\]

Thus a control cost such as

\[
K=0.60
\]

cannot be repaid robustly by **any** finite information architecture, but can be
favored in expectation when common worlds terminate after one query and hard
worlds are sufficiently rare.

## Corollary RF5.3 — cue-arity no-go is specifically a robust no-go

For fixed finite cue arity \(b\),

\[
K_{\rm crit,robust}^{(b)}
\le
U(2)-U_\infty.
\]

But the expected supremum

\[
U(1)-U_\infty
\]

can be approached even with binary cues by placing the common world in a
one-query pure branch and the growing fixed burden in the rare branch.

Therefore

\[
b_{\min}^{\rm robust}=\infty
\]

does **not** imply expected evolutionary impossibility.

This formalizes the claim boundary already used elsewhere in the repository:
world frequencies can rescue an architecture that fails every statewise robust
threshold.



## 9g. Theorem RF6 — exact encounter-frequency threshold above the robust ceiling

RF5 identifies a frequency-assisted evolvability band but does not quantify how
skewed the encounter distribution must be.

Let

\[
p_1
=
\Pr[T_\pi=1]
\]

be the total encounter probability of worlds resolved after exactly one query
by a guaranteed-resolving adaptive policy.

For every other represented world,

\[
T_\pi\ge2.
\]

Therefore, for bounded-below nonincreasing \(U\),

\[
\sum_xp_xU[T_\pi(x)]
\le
p_1U(1)
+
(1-p_1)U(2).
\]

Also

\[
U(C_F)\ge U_\infty.
\]

Hence every finite task obeys

\[
\boxed{
R_{\rm expected}
\le
p_1U(1)
+
(1-p_1)U(2)
-
U_\infty.
}
\]

### Sharpness

The bound is asymptotically attainable with binary queries.

Construct a tree with:

1. one target-pure leaf at depth 1 carrying probability \(p_1\);
2. one target-pure leaf at depth 2 carrying probability
   \(1-p_1-\delta\);
3. a deep private-pair subtree below the other depth-2 branch carrying total
   probability \(\delta>0\).

As the rare subtree grows,

\[
C_F\to\infty,
\]

and as

\[
\delta\to0^+,
\]

the expected adaptive value approaches

\[
p_1U(1)+(1-p_1)U(2).
\]

Thus

\[
\boxed{
\sup R_{\rm expected}\mid p_1
=
p_1U(1)
+
(1-p_1)U(2)
-
U_\infty.
}
\]

## Corollary RF6.1 — minimum frequency of one-step states needed for expected rescue

Suppose architecture cost lies strictly inside the frequency-assisted band:

\[
U(2)-U_\infty
<
K
<
U(1)-U_\infty.
\]

Positive expected net value is possible if and only if

\[
\boxed{
p_1
>
p_{\rm crit}
=
\frac{
K-[U(2)-U_\infty]
}{
U(1)-U(2)
}.
}
\]

So \(p_{\rm crit}\) is the exact scalable-scope minimum encounter mass that
must be placed on one-step states in order for frequency concentration to
rescue a control cost that no architecture can repay robustly.

At the lower edge of the band,

\[
p_{\rm crit}\to0,
\]

while at the upper expected-value ceiling,

\[
p_{\rm crit}\to1.
\]

## Corollary RF6.2 — exponential opportunity formula

For

\[
U(c)=ve^{-\mu c},
\qquad
U_\infty=0,
\]

the frequency-assisted band is

\[
ve^{-2\mu}<K<ve^{-\mu},
\]

and

\[
\boxed{
p_{\rm crit}
=
\frac{
K-ve^{-2\mu}
}{
v(e^{-\mu}-e^{-2\mu})
}.
}
\]

At

\[
\mu=0.3,\qquad
v=1,\qquad
K=0.60,
\]

\[
\boxed{
p_{\rm crit}
\approx
0.266597.
}
\]

Thus only about \(26.7\%\) of encounters need to belong to one-step states in
the asymptotic scalable construction to make expected repayment possible,
despite robust repayment being impossible for every finite information
architecture.

The theorem concerns the aggregate probability of one-step completion, not the
frequency of any particular ecological species or habitat state.



## Corollary RF6.3 — encounter-frequency structure can substitute for cue arity in expectation

The robust and expected inverse problems have qualitatively different arity
requirements.

For robust statewise repayment, RF2.3a defines

\[
b_{\min}^{\rm robust}(K;U)
=
\min
\left\{
b\ge2:
K<K_{\rm crit,robust}^{(b)}
\right\},
\]

which can equal \(3,4,\ldots\) or \(\infty\).

For expected repayment when encounter frequencies and finite task size may vary,
RF5 gives the absolute ceiling

\[
U(1)-U_\infty.
\]

Because the matching RF5 construction is already binary, the minimum expected-
value cue arity is simply

\[
\boxed{
b_{\min}^{\rm expected}
=
\begin{cases}
2,&K<U(1)-U_\infty,\\
\infty,&K\ge U(1)-U_\infty.
\end{cases}
}
\]

Thus ecological frequency concentration can substitute for sensory branching
capacity in the expected-value problem.

### Two canonical contrasts

For

\[
U(c)=e^{-0.3c},
\]

and

\[
K=0.30,
\]

the robust problem gives

\[
b_{\min}^{\rm robust}=3,
\]

while

\[
\boxed{
b_{\min}^{\rm expected}=2.
}
\]

For

\[
K=0.60,
\]

the cost lies above the absolute robust ceiling

\[
e^{-0.6}\approx0.548812,
\]

so

\[
b_{\min}^{\rm robust}=\infty.
\]

But it remains below the expected ceiling

\[
e^{-0.3}\approx0.740818,
\]

so

\[
\boxed{
b_{\min}^{\rm expected}=2.
}
\]

This does not mean binary sensory systems are universally sufficient.
The expected result exploits arbitrarily skewed encounter frequencies and a
scalable rare-state subtree. The robust result remains the relevant threshold
when positive value must hold across all represented states.


## 10. Relation to PAYOFF

The forward **robust** interface is

\[
R_{\rm robust,max}
=
\max_h[U(h)-U(I_h)].
\]

PAYOFF asks whether the relevant recoverable benefit, robust or expected for
the declared comparison, exceeds architecture cost:

\[
R-K>0.
\]

The inverse interface developed here asks what structural resources are needed
to make that inequality possible.

Thus:

\[
\boxed{
\text{natural history + architecture cost}
\to
J_K(h)
\to
\text{minimum finite information architecture}.
}
\]

This is the cleanest reverse bridge from fitness back to sensing structure.

## 11. Prior-art boundary

Inverse resource requirements are algebraically equivalent to the forward sharp
envelope, so they are not a separate independent novelty family.

Their biological role is interpretive and predictive:

- recover the old exact structural-gap theorem from a linear fitness model;
- show why nonlinear natural history makes required structural complexity
  depth dependent;
- give a direct minimum-world/query requirement for a declared architecture
  cost.

Do not claim novelty for integer inversion of a monotone utility function by
itself.
