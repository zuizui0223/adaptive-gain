# Stage11 execution ledger

2026-10-30. Existing isolated branch: analysis/wind-reward-stage11-20261030, based on frozen Stage10; main and Stage9b unchanged. User requests continued execution, not another design approval cycle.

Source integrity: six provider-original files verified at run41008734136, v456836. DOI slash encoding was the root cause of initial404 and was regression tested. Source counts123 surveys/1227 rows differ from paper122/1217; eligibility is fixed by keys and measurement status, not forcing published counts.

TDD: source tests4 fail on stubs then4pass; URL regression fails then5total source tests pass; cohort tests4fail then4pass; association tests5fail/error on empty implementation then5pass. Combined14focused tests pass locally. Cluster CR1 covariance and t-p-values match independent statsmodels implementation on synthetic clustered fixtures. Synthetic cases never count as empirical outcomes.

Review: original nectar.site denotes local location whereas forage.site denotes city. Original mean-imputed ivy is excluded through raw nectar columns, not filled derived fields. One survey is one observation after aggregation, city-date clusters for inference. Single frozen interaction, no outcome-derived profit response. No fresh external reviewer available; mathematical comparison and whole-file self-review only, not independent human peer review.

Implementation choices left unspecified by protocol: pandas string/date parsing preserves original IDs; exact source digests pinned for modeled CSVs; all original exclusions logged. QR solves full-rank OLS; rank failure stops rather than deleting controls. Two city descriptive fits use full-sample within-plant centering per frozen protocol. These were fixed before the biological fit.
