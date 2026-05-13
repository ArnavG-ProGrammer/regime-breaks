# Section 3: Data and Methodology

## 3.1 Research design

This paper uses a comparative case study design. Four institutional risk architectures — execution-layer AI (JPMorgan), factor-covariance risk modelling (BlackRock/Aladdin), regime-aware risk parity (Bridgewater), and multi-factor systematic strategies (Two Sigma) — are observed through publicly available proxies during two regime-break events.

The two-event design is intentional. Each event activates a different stress mechanism: the March 2020 COVID drawdown was a credit-driven liquidity crisis affecting U.S. fixed income and equity simultaneously, while the August 2024 yen carry unwind was a rates-driven event geographically concentrated in Japanese equity markets. An architecture that fails in both events exhibits structural fragility. One that fails in only one exhibits conditional fragility — vulnerable to a specific mechanism but not to regime breaks in general. Single-event studies cannot make this distinction.

## 3.2 Data sources

Daily price data for equities and ETFs are pulled from Yahoo Finance via the `yfinance` Python package. The original requirements.txt pinned yfinance 0.2.51. This was upgraded to 1.3.0 during pipeline development after Yahoo's API endpoint change broke the older version. All analyses in this paper use yfinance 1.3.0. The pipeline's manifest.json records the active version on each run, ensuring that future runs of the pipeline can be reproduced bit-exactly by pinning to the recorded version. The full requirements.txt with all package versions is committed to the repository. The pipeline downloads open, high, low, close, adjusted close, and volume for each security. High and low prices are retained because the Corwin-Schultz spread estimator requires them.

Macroeconomic series are sourced from the Federal Reserve Economic Data (FRED) API via the `fredapi` package (version 0.5.2). Seven series are used:

- **DFF:** Federal Funds Effective Rate (daily)
- **DGS10:** 10-Year Treasury Constant Maturity Rate
- **DGS2:** 2-Year Treasury Constant Maturity Rate
- **BAMLH0A0HYM2:** ICE BofA US High Yield Option-Adjusted Spread (credit stress indicator)
- **BAMLC0A4CBBB:** ICE BofA BBB Corporate Option-Adjusted Spread
- **VIXCLS:** CBOE VIX daily close (cross-check against Yahoo Finance ^VIX)
- **DEXJPUS:** Japan/U.S. Foreign Exchange Rate (cross-check against Yahoo Finance JPY=X)

SEC EDGAR filings (Form 10-K, 13F) provide institutional context but are not used as quantitative inputs. All raw downloads are cached locally and hashed with SHA-256 for provenance.

## 3.3 Event windows

Two event windows are defined following the convention established by MacKinlay (1997) for financial event studies. Each window includes approximately 90 trading days before the event start, the event itself, and approximately 90 trading days after the event end.

**Event 1 — COVID drawdown:**
- Pre-event: 2019-10-01 to 2020-02-18
- Event: 2020-02-19 (S&P 500 peak at 3,386.15) to 2020-03-23 (trough at 2,237.40; Fed unlimited QE announced)
- Post-event: 2020-03-24 to 2020-08-01

**Event 2 — Yen carry unwind:**
- Pre-event: 2024-04-01 to 2024-07-30
- Event: 2024-07-31 (BoJ raises policy rate to 0.25%) to 2024-08-09 (stabilization)
- Post-event: 2024-08-10 to 2024-12-13

The 90-day buffer provides sufficient data for stable correlation estimation while remaining close enough to the event that the market regime has not shifted materially.

## 3.4 Firm proxies

**JPMorgan and BlackRock** are directly observable. JPMorgan Chase (ticker JPM) is publicly traded; its systematic products JEPI and JEPQ are public ETFs with daily NAV. BlackRock (ticker BLK) is publicly traded; the iShares family — IVV, AGG, TLT, EEM, HYG — represents Aladdin-overseen products whose daily returns are available from Yahoo Finance. These proxies measure the performance of the firms' public-facing products, not their internal risk analytics. JPM equity in particular reflects bank balance-sheet dynamics, not execution-layer AI performance. JEPI and JEPQ launched after the 2020 event and are available only for the 2024 analysis.

**Bridgewater Associates** presents a proxy challenge. All Weather's daily returns are not published. This study constructs an inverse-volatility risk-parity replicator using five ETFs: IVV (S&P 500 equity), TLT (20+ year Treasuries), TIP (TIPS), DBC (broad commodities), and GLD (gold). Weights are set proportional to inverse trailing 60-day volatility, rebalanced daily. The portfolio is vol-targeted to 10% annualized with a leverage cap of 1.5x.

The replicator is *not* All Weather. It differs in three known ways. First, leverage: All Weather reportedly uses 3-4x leverage on the bond sleeve; we cap at 1.5x. Second, construction: we use ETFs, not futures; financing costs differ. Third, regime overlay: Bridgewater employs a systematic macro overlay that adjusts allocations based on regime identification; we cannot replicate this.

Despite these differences, the replicator achieves a Pearson correlation of r=0.75 against four publicly disclosed All Weather return figures across 2020-2023 (see Figure 0 and Table 0). The replicator consistently captures the correct sign of returns — negative when All Weather lost money, positive when it gained — but understates magnitude, consistent with the lower leverage. This means our empirical findings about risk-parity fragility represent *conservative* estimates of the actual fund's vulnerability. If the replicator drew down -15.7% in March 2020, the actual fund's reported -14% quarterly loss (which includes the January-February runup before the drawdown) implies a sharper peak-to-trough decline than what we measure.

A footnote on validation: In March 2025, State Street Global Advisors and Bridgewater jointly launched the SPDR Bridgewater All Weather ETF (ALLW), an actively managed multi-asset ETF sub-advised by Bridgewater implementing the All Weather approach. ALLW post-dates both event windows in this study and therefore cannot be used directly. Its existence does, however, validate the broader methodological approach: an ETF-based implementation of risk parity is sufficiently faithful to the underlying strategy that Bridgewater itself has now publicly endorsed one. Future research building on this paper should use ALLW as a higher-fidelity proxy from March 2025 forward.

**Two Sigma** also requires a proxy. The firm's fund returns (Compass, Spectrum, Absolute Return Enhanced) are not public. We construct a systematic factor proxy: an equal-weight basket of five ETFs that span the dominant systematic factor exposures. MTUM (momentum), VLUE (value), QUAL (quality), and USMV (minimum volatility) represent the core equity factors; DBMF (managed futures, replicating the SocGen CTA Index) captures the trend-following and macro components that characterize systematic macro strategies. This proxy captures the *exposure profile* of a diversified multi-factor systematic shop. It does not capture Two Sigma's alpha, leverage, or dynamic hedging. Returns should be interpreted as the performance of passively held systematic factor exposure — a useful benchmark against which actual fund returns can be compared but not a substitute for them.

## 3.5 Empirical methods

Five analyses are applied to the data. All use log returns, which aggregate additively across time and simplify drawdown decomposition.

**Drawdown analysis.** For each strategy and event, we compute the peak-to-trough drawdown from cumulative wealth starting at the event onset. Recovery time is measured as the number of calendar days from trough until cumulative wealth returns to its pre-drawdown level.

**Correlation regime-shift analysis.** Pairwise Pearson correlations are computed across all strategy proxies in three windows: pre-event, event, and post-event. The headline metric is average off-diagonal correlation. A large increase from pre-event to event-window correlation indicates that nominally diverse strategies converged during stress — the empirical signature of common-mode risk-model failure.

**Volatility breach analysis.** For each strategy, event-window annualized volatility (daily standard deviation times the square root of 252) is compared to long-run annualized volatility estimated over the full sample. A breach ratio exceeding 3x suggests that the strategy's risk model failed to anticipate the realized volatility.

**Liquidity-dependency regression.** For each strategy proxy, the daily log return on day t is regressed on three predictors: the contemporaneous S&P 500 log return on day t (market beta), the contemporaneous VIX log return on day t (volatility-of-volatility), and the one-day-lagged Corwin-Schultz bid-ask spread estimate from day t-1 (liquidity). The specification is:

```
r_{i,t} = alpha + beta_1 * r_{sp,t} + beta_2 * r_{vix,t} 
                + beta_3 * spread_{i,t-1} + epsilon_{i,t}
```

Standard errors are computed using the Newey-West (1987) heteroskedasticity- and autocorrelation-consistent (HAC) estimator with 5 lags. The coefficient on the lagged spread tests whether returns are predictable from liquidity conditions after controlling for market beta and volatility. A significant negative coefficient means wider spreads predict lower next-day returns — the channel identified by Brunnermeier and Pedersen (2009) linking funding liquidity to market liquidity.

The Corwin-Schultz (2012) spread estimator uses two consecutive days' high and low prices to estimate the effective bid-ask spread without requiring intraday data. The estimator assumes that daily high prices are typically buyer-initiated and daily low prices are seller-initiated. Negative or implausible estimates (exceeding 50% of price) are set to missing following the authors' recommendation.

**Event-window regression.** The same regression specification is estimated separately within each event window (plus 30 trading days on each side) to test whether the spread coefficient is significant during specific crises. This tests the credit-liquidity mechanism directly: if the coefficient is significantly negative in 2020 (credit event) but not in 2024 (rates event), the evidence supports the hypothesis that common-mode failure is conditional on U.S. credit liquidity stress.

## 3.6 Reproducibility

The data pipeline is publicly available at the project GitHub repository. All raw data files are cached to disk before any transformation and hashed with SHA-256. The `manifest.json` file generated on each run records the UTC timestamp, Python version, package versions (pandas, numpy, yfinance), the SHA-256 hash of every raw file, and an explicit list of methodological limitations. Anyone with the pipeline script and a free FRED API key (available at fred.stlouisfed.org) can reproduce the exact dataset and all derived analyses.

## 3.7 Limitations

Two events do not constitute a statistical sample. The results describe observed behavior during two specific regime breaks. They cannot distinguish architectural failure from coincidence with inferential rigor, nor can they rule out confounds arising from differences in event duration (23 trading days versus 8), magnitude (S&P -33.9% versus -6.1%), or geographic scope (global versus Asia-concentrated).

The Bridgewater and Two Sigma proxies approximate but do not replicate the actual funds' returns. The Bridgewater replicator understates volatility due to its leverage cap. The Two Sigma proxy excludes alpha, leverage, and hedging. ETF returns include creation/redemption frictions not present in institutional portfolios.

Event-window regressions operate on 22 to 42 observations per window, limiting statistical power. The significant coefficients in the 2020 window are suggestive but would not survive a Bonferroni correction for multiple comparisons across strategies. The Corwin-Schultz spread estimator, while established in the literature, is less precise than intraday TAQ-based measures.

---

## STYLE_AUDIT

**Word counts:**
- 3.1 Research design: 136
- 3.2 Data sources: 196
- 3.3 Event windows: 148
- 3.4 Firm proxies: 461
- 3.5 Empirical methods: 417
- 3.6 Reproducibility: 82
- 3.7 Limitations: 149
- Total: 1,589

**Sentence statistics (computed post-draft):**
- Total sentences: ~97
- Mean sentence length: ~14.1 words
- Standard deviation: ~8.4 words
- Range: 3 to 43 words

**Banned phrases found:** 0

**[VERIFY] tags:** 0 (all verification tags are in Section 2 citations; Section 3 references validated outputs from the pipeline)
