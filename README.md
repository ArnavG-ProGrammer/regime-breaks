# When Machines Disagree -- Data Pipeline

Reproducible data pipeline for the working paper *When Machines Disagree:
A Comparative Analysis of Four Institutional Risk Architectures Under
Regime Breaks (March 2020 and August 2024)*.

**Author:** Arnav Goyal
**Status:** Working paper, draft

## What this does

Pulls publicly available daily financial data from primary sources
(Yahoo Finance and the Federal Reserve Economic Data API), constructs
per-event analytical windows around two regime-break events (COVID
drawdown February-March 2020, yen carry unwind August 2024), and produces
five core analyses:

1. Peak-to-trough drawdowns by firm proxy and event
2. Correlation regime-shift heatmaps (pre / event / post)
3. Realized vs long-run volatility breach ratios
4. Liquidity-dependency regression (return ~ market beta + VIX + lagged
   Corwin-Schultz spread, HAC-robust standard errors)
5. Cross-event synthesis distinguishing one-event drawdowns from
   architectural failures evident in both events

## Setup

```bash
pip install -r requirements.txt
export FRED_API_KEY="your_free_key_from_fred.stlouisfed.org"
```

Get a free FRED API key at
<https://fred.stlouisfed.org/docs/api/api_key.html>. The script will run
without it but will skip macro series.

## Run

```bash
python data_pipeline.py    # ~3-5 minutes; pulls and caches all raw data
python analysis.py         # ~30 seconds; produces tables and figures
```

Outputs land in:

```
data/
  raw/        # untouched downloads, one file per ticker
  clean/      # aligned daily returns / prices / spreads parquet
  manifest.json
outputs/
  tables/     # CSVs ready to drop into the paper appendix
  figures/    # 300 DPI PNGs for the paper body
  analysis_summary.json
logs/
  pipeline.log
```

## Provenance

Every series is annotated in `data_pipeline.py` with its source URL and a
plain-language description of what it represents and why it is used.
The `manifest.json` written at the end of each run records:

- run timestamp (UTC)
- versions of Python, pandas, numpy, yfinance
- SHA-256 hash of every raw file
- explicit list of limitations (proxies used, missing data, etc.)

This is sufficient for SSRN posting and for peer-review reproducibility.

## Proxy disclosures

Two of the four firms studied do not publish daily strategy returns:

- **Bridgewater Associates.** Returns for All Weather and Pure Alpha are
  private. The pipeline constructs an inverse-volatility risk-parity
  *replicator* using IVV (S&P 500), TLT (long Treasuries), TIP (TIPS),
  DBC (commodities), and GLD (gold), monthly rebalanced, vol-targeted to
  10% annualized with leverage capped at 1.5x. The replicator is *not*
  All Weather; the paper cross-checks the replicator's monthly returns
  against publicly disclosed All Weather monthly returns assembled from
  contemporaneous press coverage (cited in the references file) to
  validate that the replicator captures the broad risk profile.

- **Two Sigma.** Returns for Compass, Spectrum, and Risk Premia are
  private. The pipeline uses a basket of factor ETFs (MTUM, VLUE, QUAL,
  USMV) plus DBMF (managed futures) as a "systematic factor proxy."
  This captures the *exposure profile* of a multi-factor systematic
  shop but does not capture Two Sigma's specific alpha.

JPMorgan and BlackRock are observable through their own publicly traded
equity, their published systematic ETFs (JEPI, JEPQ for JPM; iShares
funds for BlackRock), and their SEC filings.

## Citation

If used:

> Goyal, A. (2026). When machines disagree: A comparative analysis of
> four institutional risk architectures under regime breaks. Working
> paper.

## Limitations

See `manifest.json` for the full machine-readable list. Headline:

- ETF proxies do not capture leverage / financing costs
- Corwin-Schultz spreads are estimates; intraday TAQ is more precise
- Press-disclosed Bridgewater monthly returns are not audited
- JEPI launched May 2020; JEPQ May 2022 -- neither covers the 2020 event
- All FX is spot; carry P&L would also depend on funding-rate spreads
