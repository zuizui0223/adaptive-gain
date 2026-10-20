# Same-day wind × independent flowering richness × hoverfly larval class

Date: 2026-10-20. Registered **before fitting** this extension, based only on observed support counts. Isolated work on analysis/wind-plant-context-20261020. Not a causal claim and no edits to frozen manuscripts.

Question: within the same site/date, is the *difference* in wind-associated adult hoverfly captures between zoophagous-larva and other-larva groups modified by the **richness of recorded flowering-plant taxa in separate near-trap inventories**?

Sources: UK PoMS original pan trap samples+specimens+2-m flowering-herb records, DOI 10.5285/5841bfae-471b-498c-af89-c30e5140d6c5; independent EuPollTrait DOI 10.5281/zenodo.18032357. Use locked original published MD5/SHA256 and the source-matched exact-binomial species / larval-class analysis from prior branch. Never assume a plant not recorded in a trap flower list was absent in the surrounding habitat.

Cohort: prior pan quality (unambiguous undisturbed traps, 4–8h exposure, >=3 same-day stations, within-day >=0.5 Beaufort range), >=80% matched original larval taxa, >=1 capture of BOTH larval groups per day. Require **all** stations in an eligible date to have a positive recorded flower list and >=2 distinct recorded richness values per day. Minimum >=30 sites, 100 dates and 1000 station observations.

Primary: stacked two-group conditional Poisson counts with site-day×larval class intercepts conditioned out. Trap hours are log offsets. Center wind W and log1p recorded flowering-taxon richness R **within site-day**; scale R by the pooled within-day SD, chosen before looking at outcome. First coefficient is W×R×zoophagous contrast. Include all lower order terms W×R, W×diet, R×diet, W, R and nuisance terms physical station (2–5), vegetation, sun and temperature, plus diet×nuisance. Exploratory site-cluster sandwich 95% interval, no assumed sign. Always report sample sizes, richness support, estimator condition, optimization score and the full contrast.

Declared sensitivities: (i) remove extreme dates using the *earlier original* 99th percentile count threshold, (ii) restrict to >=95% source larval classification coverage, (iii) remove source-abundance top genus **Episyrphus** while rebuilding zero and matched counts. Do not test ad-hoc plant species to rescue a p-value. H2 individual Urtica/Trifolium comparisons remain as prior no-go/inconclusive results. Physically fixed trap station / shelter can confound both R and wind: do not interpret as intervention or proof of plant→prey→larva→adult mediation. Species diet and genus are heavily confounded; a positive effect cannot identify diet-specific evolutionary adaptation.

Full runnable local counterpart: PROTOCOL_PRE_OUTCOME_20261020.md in delivered reproduction package.