# Figure legends

## Figure 1. Finite routing structure creates an exact gain-layer multiplicity profile

**A**, finite genotype-policy states have `k` branch coordinates, each in `{0,...,q}`, and total gain is set by the weakest branch, `g(x)=min_i x_i`. **B**, for the running example `q=2,k=3`, the exact numbers of genotypes at gains `0,1,2` are `(19,7,1)`. In general, `D_r=(q-r+1)^k-(q-r)^k`; writing `s=q-r`, the layer `s` steps below full gain has multiplicity `A_s=(s+1)^k-s^k`. The adjacent layer has `A_1=2^k-1` genotypes whereas the full-gain layer contains one genotype.

## Figure 2. Aggregate modality and stationary majority occur at distinct thresholds

For `q=2,k=3`, aggregate layer weights under symmetric stationary tilt are `D_r theta^r`. The full-gain layer first reaches the aggregate-mode boundary at `T_3=7`; there it ties the adjacent layer and carries stationary mass `49/117≈0.419`. A stronger tilt is required for a stationary majority: the exact half-mass threshold is `(7+5 sqrt(5))/2≈9.09`. More generally, `T_k=2^k-1` is the sharp aggregate-mode threshold, whereas for `q>=2` the majority threshold satisfies `T_k<theta_1/2(q,k)<2T_k`. In canonical routing with `k=q+1` and Moran fitness step `a=2`, unique aggregate modality first occurs at `N=q+2` and stationary majority at `N=q+3`.

## Figure 3. Representation and mutation measure delimit the occupancy thresholds

**A**, keeping the same gain values and phenotype-level fitness schedule but compressing the branch-product genotype-policy representation to one genotype per gain changes stationary occupancy. At `q=2,theta=2`, the compressed representation gives full-gain mass `4/7`, whereas the branch-product representation gives `4/37`. **B**, even with fixed gain values, fitness tilt, and mutation support, changing a reversible neutral mutation measure can produce distinct positive stationary occupancies. Thus the exact thresholds derived in the main text are conditional on both the declared genotype-policy representation and the symmetric neutral-measure assumption.