# Phase 1 Report

## Step Status

| Step | Description | Status |
|------|-------------|--------|
| 1 | Verify scaffold files on disk | DONE |
| 2 | Verify scaffold integrity (sizes) | DONE |
| 3 | Read foundation, write PROJECT_BRIEF.md | DONE |
| 4 | Directory layout, .gitignore, LICENSE | DONE |
| 5 | Venv (Python 3.12.10), install deps, smoke test | DONE |
| 6 | Run data_pipeline.py | DONE — 23/23 yfinance, 7/7 FRED |
| 7 | Sanity check data | DONE — 4/5 checks pass, 1 marginal |
| 8 | Run analysis.py | DONE — all 5 analyses produced output |
| 9 | Draft FINDINGS_MEMO.md | DONE — 0 banned phrases, sentence std 7.7 |
| 10 | Git init + GitHub push | DONE |
| 11 | This report | DONE |

## Headline Drawdown Numbers

### COVID 2020 (Feb 19 - Mar 23)
- S&P 500: -33.9%
- JPMorgan equity: -42.5%
- BlackRock IVV: -33.9%
- Two Sigma factor proxy: -30.1%
- Nikkei 225: -27.1%
- AGG (bonds): -9.6% (recovered in 7 days)
- TLT (long Treasuries): -15.7% (recovered in 1 day)

### Yen Carry 2024 (Jul 31 - Aug 9)
- Nikkei 225: -19.5%
- TLT: -11.1% (not recovered in window)
- JPMorgan equity: -8.4%
- Two Sigma factor proxy: -6.2%
- S&P 500: -6.1%
- IVV: -6.0%
- AGG: -3.7%

## Correlation Regime Shifts

| Event | Pre-event avg corr | Event-window avg corr | Post-event avg corr |
|-------|-------------------:|---------------------:|--------------------:|
| COVID 2020 | 0.24 | 0.51 | 0.40 |
| Yen carry 2024 | 0.35 | 0.45 | 0.28 |

COVID 2020 showed a 110% increase in average correlation (0.24 to 0.51). Yen carry 2024 showed only a 27% increase (0.35 to 0.45), and post-event correlations fell below pre-event levels.

## [VERIFY] Items

1. **Bridgewater replicator returns all zeros.** Root cause: the aligned price panel includes non-US trading days (from ^N225), creating NaN gaps in US ETF prices. `rolling(60).std()` returns NaN when any value in the window is NaN, propagating through `inv_vol` and `weights` to produce zero portfolio returns. Fix needed: add `min_periods=40` (or similar) to the rolling calls in `build_risk_parity_replicator()`. This requires modifying `data_pipeline.py` in Phase 2.

2. **Nikkei 225 drawdown (-19.5%) vs expected range (-20% to -28%).** The -19.5% is correct from closing prices. The discrepancy with the expected -20% lower bound is within 0.5 percentage points. The 12.4% single-day drop on Aug 5 is measured from the previous close, not from the event-window peak. No action needed.

3. **yfinance version upgraded from 0.2.51 to 1.3.0.** The pinned version could not connect to Yahoo Finance (API endpoint change). The upgrade was necessary to pull any data at all. `requirements.txt` still says 0.2.51 — should be updated in Phase 2 to reflect the working version. scipy was also pinned to <1.15 for statsmodels compatibility.

## Output Files

- Findings memo: `FINDINGS_MEMO.md`
- Project brief: `PROJECT_BRIEF.md`
- Tables: `outputs/tables/` (11 files)
- Figures: `outputs/figures/` (7 PNGs)
- Manifest: `data/manifest.json`

## GitHub Repository

**URL:** https://github.com/ArnavG-ProGrammer/regime-breaks (private)
**Tag:** `phase-1-complete`
**Branch:** `main`

## Phase 1.5 Completion (2026-05-10)

All three issues resolved:
- **Issue A (Bridgewater NaN bug):** Fixed via `dropna()` on component returns + `min_periods=30` in rolling windows. Replicator now shows -15.7% drawdown in COVID, +0.9% in yen carry. Ann vol = 9.7%, cumulative return = +48.4%.
- **Issue B (Headline overclaim):** Added `analysis_4b_liquidity_regression_by_window()`. Result: 3/7 significant negative spread coefficients in 2020, 0/8 in 2024. Headline rewritten to present as hypothesis consistent with data + alternative explanations.
- **Issue C (Numeric traceability):** 22 inline citations added to FINDINGS_MEMO.md in `[T1/T2/T4b: ticker, event, column]` format.

**Tag:** `phase-1.5-complete`

## Next Phase

Phase 2 begins after Arnav reviews FINDINGS_MEMO.md. Remaining items:
1. Update `requirements.txt` to reflect working versions (yfinance 1.3.0, scipy<1.15)
2. Begin paper section drafts
