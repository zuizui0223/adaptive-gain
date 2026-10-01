# Balanced-query companion prior-art receipt v1

Date: 2026-10-01
Status: targeted literature receipt for the exact-balanced mathematical companion. Non-discovery is not proof of priority.

## Question audited

The audit asks whether existing literature already contains the same extremal theory for finite deterministic target resolution when every available binary query is globally exactly half-half balanced.

The repository-specific claims under audit are:

1. the fixed-side cap
   \[
   \max C_F=n-3
   \]
   for even \(n\ge6\);

2. the equality classification forcing a star--edge--star private-pair forest;

3. the depth-constrained envelopes
   \[
   D_h(n)=\max\{C_F:C_A\le h\}
   \]
   and their finite compatibility defects;

4. unbounded \(C_F/C_A\) despite every query being exactly 50/50 balanced.

## Confirmed prior art

### Adaptive and non-adaptive search on one set system

Wiener (2009), *Rounds in Combinatorial Search*, defines \(k\)-round complexity on a separating system; one round is non-adaptive and the fully sequential endpoint is adaptive.

Damaschke (2019), *Combinatorial search in two and more rounds*, studies the same general test-hypergraph setting and explicitly connects the one-round case to Test Cover.

Consequence for claims:
- adaptive versus non-adaptive search is prior art;
- a common declared test vocabulary is prior art;
- generic adaptivity gaps are prior art.

### General irredundant separating-family cap

Bondy's 1972 induced-subsets theorem implies the classical sharp bound that an inclusionwise minimal separating family on an (n)-element ground set has size at most (n-1). Later separating-family literature states this consequence explicitly.

Consequence:
- the unrestricted (C_F\le n-1) cap is prior art;
- the private-pair forest proof should be presented as a convenient model-native proof, not as the novelty claim;
- the candidate new content begins with the improvement to (n-3) under exact half-balance and the associated equality structure.

### Cardinality-constrained and uniform separating systems

Katona (1966) and Wegener (1979) study separating systems under cardinality restrictions on the tests. Ahlswede (2008) develops ratewise-optimal non-sequential search under such test-size constraints and includes the k-uniform separating formulation. Ling, Li & van Rees (2004) define uniform separating systems using blocks of size exactly half the even ground set.

Consequence:
- exact half-size binary tests are an established combinatorial restriction;
- minimum-size non-adaptive search with cardinality-constrained or uniform tests is prior art;
- the paper must not claim novelty for imposing 50/50 balance itself;
- the candidate contribution is instead about maximum irredundant fixed burden and its interaction with bounded adaptive depth inside a declared balanced vocabulary.

### Complete read-once tree geometry

Chiarelli, Hatami & Saks (2020) note the classical construction in which a read-once decision tree of depth \(d\) depends on \(2^d-1\) relevant variables.

Consequence:
- \(2^d-1\) complete-tree resource counts are prior art;
- the unrestricted binary extremal formula should be baseline material, not the paper's novelty anchor.

## Dedicated collision searches performed

Queries included combinations of:

- irredundant uniform separating system;
- maximum irredundant balanced separating family;
- constant-weight separating matrix private pairs;
- balanced cuts private pairs;
- exact half-size adaptive search;
- balanced Twenty Questions adaptive non-adaptive;
- \(n-3\) uniform separating family;
- equality cases for uniform separating systems;
- adaptive uniform separating system.

The searches recovered:
- minimum-size uniform separating systems;
- bisecting/splitting systems;
- general adaptive combinatorial search;
- constant-weight group-testing / disjunct-matrix literature;
- standard balanced-question heuristics.

They did not locate an exact predecessor for:
- the \(n-3\) maximum fixed burden for a *declared* exact-balanced vocabulary;
- the star--edge--star equality structure;
- the \(D_h(n)\) exact envelopes or the \(D_3(10)\) compatibility defect;
- the exact statement that every available query can be globally 50/50 balanced while the fixed/adaptive worst-case ratio remains unbounded.

## Current priority status by result

### Fixed cap \(n-3\)

Status: **plausibly independent, priority not proved**.

Risk:
an equivalent theorem may exist under terminology such as maximal irredundant uniform separating family, constant-row-weight separating matrix, or minimal separating family with private pairs.

### Star--edge--star equality classification

Status: **strongest finite structural novelty candidate**.

No equivalent equality-case theorem was located in the targeted search.

### \(D_h(n)\) envelopes

Status: **strong candidate mathematical program**.

The object combines uniform query balance, a fixed minimum, and bounded adaptive depth. General round-complexity literature is close conceptually but the targeted search did not locate these exact extremal envelopes.

### Exactly-balanced unbounded ratio

Status: **strong asymptotic novelty candidate**.

Generic unbounded adaptivity gaps are prior art; the potentially distinctive part is that *every available binary query* is globally exactly balanced.

## Safe manuscript wording

Use:

> We study the extremal interaction between uniform half-size tests, fixed irredundance and bounded adaptive depth.

> Within this target-resolution model, exact balance yields a sharp \(n-3\) fixed-side cap and rigid equality structure.

> We have not located an earlier result giving the same depth-constrained exact-balanced envelopes.

Avoid:

- first;
- first-ever;
- no previous work;
- new adaptivity gap;
- new uniform separating system;
- new balanced-question model.

## References

- J. A. Bondy. 1972. Induced subsets. Journal of Combinatorial Theory, Series B 12:201-202. DOI: 10.1016/0095-8956(72)90025-1.
- R. Ahlswede. 2008. Ratewise-optimal non-sequential search strategies under constraints on the tests. Discrete Applied Mathematics 156(9):1431-1443. DOI: 10.1016/j.dam.2006.06.013.
- G. Wiener. 2009. Rounds in Combinatorial Search. Dagstuhl Seminar Proceedings 09281. DOI: 10.4230/DagSemProc.09281.6.
- P. Damaschke. 2019. Combinatorial search in two and more rounds. Theoretical Computer Science 780:1-11. DOI: 10.1016/j.tcs.2019.02.004.
- A. C. H. Ling, P. C. Li & G. H. J. van Rees. 2004. Splitting systems and separating systems. Discrete Mathematics 279:355-368. DOI: 10.1016/S0012-365X(03)00280-2.
- J. Chiarelli, P. Hatami & M. Saks. 2020. An asymptotically tight bound on the number of relevant variables in a bounded degree Boolean function. Combinatorica 40:237-244. DOI: 10.1007/s00493-019-4136-7.

## Next audit

The remaining high-value search is bibliographic rather than theorem-generating:

1. Aigner/Katona monographs and citations on irredundant separating systems;
2. constant-row-weight separating matrices with maximal minimal families;
3. equality classifications for uniform separating systems;
4. restricted-question Twenty Questions under globally balanced available tests.

Stop rule: do not create another theorem family while this boundary remains open.
