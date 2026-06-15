\newpage

\begin{center}

\vspace*{2in}

# When Machines Disagree

## A Comparative Analysis of Four Institutional Risk Architectures Under Regime Breaks (March 2020 and August 2024)

\vspace{1.5in}

**Arnav Goyal**

Ahlcon International School

New Delhi, India

\vspace{1in}

Working Paper

May 2026

\vspace{0.5in}

Contact: arnavsgoyal@gmail.com

\vspace{0.5in}

*Independent research; not affiliated with any institution mentioned in this paper.*

\end{center}

\newpage

# Abstract

When markets break, do architecturally distinct AI and quantitative strategies fail in distinct ways, or do they converge on the same failure mode? This paper examines four institutional risk architectures during two regime breaks: the March 2020 COVID drawdown (a credit-driven liquidity crisis) and the August 2024 yen carry unwind (a rates-driven event concentrated in Japan). The four architectures, execution-layer AI (JPMorgan), factor-covariance risk modelling (BlackRock/Aladdin), regime-aware risk parity (Bridgewater), and multi-factor systematic strategies (Two Sigma), are observed through publicly available proxies and ETFs. In 2020, average pairwise correlations across strategy proxies nearly doubled (0.25 to 0.50), and event-window regressions identified significant negative lagged bid-ask spread coefficients for AGG (p = 0.006), HYG (p < 0.001), and MTUM (p = 0.005), a pattern consistent with forced selling through the Brunnermeier-Pedersen funding-liquidity channel. In 2024, correlations rose only 19%, no strategy showed a significant negative spread coefficient, and the Bridgewater risk-parity replicator gained +0.9% versus its -15.7% drawdown in 2020. The pattern is consistent with the credit-liquidity hypothesis: the regression signature appeared during the U.S. credit event and was absent during the non-credit regime break. Two events cannot prove this is a causal mechanism. Architectural diversity did not prevent correlated failure in 2020. The evidence is consistent with a common-mode channel operating at the level of funding markets rather than model architecture, though the analysis does not isolate this channel from alternative explanations including leveraged-position deleveraging and dealer balance sheet constraints. Two events cannot prove causation, and the proxy-based design introduces magnitude uncertainty, but the findings suggest that funding-channel exposure may be a relevant dimension for systemic risk supervision alongside model similarity. Data pipeline and analysis code are publicly available for reproduction and out-of-sample testing.

\newpage

# Table of Contents

1. Introduction
2. Background and Architecture Taxonomy
   - 2.1 JPMorgan: execution-layer AI on a discretionary mandate
   - 2.2 BlackRock: factor-covariance risk models (Aladdin)
   - 2.3 Bridgewater: regime-aware risk parity
   - 2.4 Two Sigma: multi-factor systematic strategies
   - 2.5 Summary of testable hypotheses
3. Data and Methodology
   - 3.1 Research design
   - 3.2 Data sources
   - 3.3 Event windows
   - 3.4 Firm proxies
   - 3.5 Empirical methods
   - 3.6 Reproducibility
   - 3.7 Limitations
4. Event 1: COVID Drawdown (February to March 2020)
   - 4.1 Event context
   - 4.2 Per-firm drawdowns
   - 4.3 Correlation regime shift
   - 4.4 Liquidity regression and the credit-liquidity channel
   - 4.5 Architectural verdict
5. Event 2: Yen Carry Unwind (August 2024)
   - 5.1 Event context
   - 5.2 Per-firm drawdowns
   - 5.3 Correlation regime shift
   - 5.4 The absence is informative
   - 5.5 Architectural verdict
6. Cross-Event Synthesis
   - 6.1 The architectural test
   - 6.2 The credit-liquidity mechanism
   - 6.3 Concentration and systemic risk
   - 6.4 What the paper does not show
   - 6.5 Implications for AI in finance
7. Limitations
   - 7.1 Sample size
   - 7.2 Proxy limitations
   - 7.3 Statistical power
   - 7.4 Exploratory rather than confirmatory design
   - 7.5 Identification limitations
   - 7.6 Robustness considerations
   - 7.7 Falsification scope
8. Conclusion

Acknowledgments

References

Appendix A: Verification of Source Material

Appendix B: Reproducibility

Appendix C: Data Sources

\newpage

# List of Figures

**Figure 1.** Bridgewater risk-parity replicator validation against reported All Weather returns, 2020 to 2023.

**Figure 2.** Strategy drawdowns during the COVID 2020 event window.

**Figure 3.** Correlation heatmaps for COVID 2020.

**Figure 4.** Strategy drawdowns during the yen carry 2024 event window.

**Figure 5.** Correlation heatmaps for yen carry 2024.

**Figure 6.** Cross-event drawdown scatter.

\newpage

# List of Tables

**Table 1.** Summary of testable hypotheses by institutional architecture.

**Table 2.** Bridgewater replicator validation across four reference periods.

**Table 3.** Peak-to-trough drawdowns by strategy, COVID 2020 event.

**Table 4.** Event-window liquidity regression coefficients, COVID 2020.

**Table 5.** Peak-to-trough drawdowns by strategy, yen carry 2024 event.

**Table 6.** Event-window liquidity regression coefficients, yen carry 2024.

\newpage

## Section 1: Introduction

Institutional asset managers now deploy AI and quantitative strategies across trillions of dollars in assets. These strategies differ in their architecture: some use AI to execute trades, others to model risk, others to generate signals. A natural question follows. When markets break, when correlations spike, liquidity evaporates, and volatility regimes shift, do these architecturally distinct strategies fail in distinct ways? Or do they converge on the same failure mode? The distinction matters for systemic risk. If nominally diverse architectures share underlying exposure to a common mechanism, their simultaneous failure can amplify the very shock that triggered it. Brunnermeier and Pedersen (2009) formalize this as the funding-liquidity channel: when margin constraints bind, forced selling by one participant widens spreads for all, creating a self-reinforcing spiral. Adrian and Brunnermeier (2016) extend this logic to measure the systemic contribution of individual institutions via CoVaR. This paper tests whether the same channel operates across four distinct institutional risk architectures during two regime breaks.

This study examines four firms that represent distinct positions in the architecture space. JPMorgan deploys AI at the execution layer, including order routing and contract parsing, while investment decisions remain human-directed. BlackRock's Aladdin platform performs factor-covariance risk decomposition across BlackRock's $14.0 trillion in assets under management as of 31 December 2025 (BlackRock 10-K FY2025, Item 1) and an additional pool of institutional client assets reported by BlackRock at approximately $25 trillion across the Aladdin platform as of December 2025. Bridgewater's All Weather strategy uses regime-aware risk parity, equalizing risk contribution across asset classes with leverage. Two Sigma runs multi-factor systematic strategies across equity, macro, and event-driven mandates. Each architecture makes a different bet about which correlations will hold during stress. Section 2 develops testable hypotheses for each, grounded in their public disclosures, filings, and products.

Two regime breaks provide the empirical setting. The March 2020 COVID drawdown was a credit-driven liquidity crisis: the S&P 500 fell -33.9% in 23 trading days, the ICE BofA High Yield OAS exceeded 1,100 basis points, and the Federal Reserve intervened with unlimited Treasury and agency MBS purchases on March 23. The August 2024 yen carry unwind was a rates-driven event geographically concentrated in Japan: the Nikkei 225 fell 12.4% in a single session after the Bank of Japan raised its policy rate, and the VIX spiked above 65 intraday. The two-event design is essential. Each event activates a different stress mechanism, credit-liquidity versus rates-FX, and an architecture that fails in both exhibits structural fragility, while one that fails in only one exhibits conditional fragility tied to a specific channel. This is a comparative case study, not a statistical sample.

The empirical findings are sharp. In the 2020 event window, three strategies showed significant negative lagged Corwin-Schultz spread coefficients: AGG (p = 0.006), HYG (p < 0.001), and MTUM (p = 0.005). Wider bid-ask spreads on day t-1 predicted lower returns on day t, a pattern consistent with forced selling into illiquid markets. In the 2024 event window, no strategy showed the same pattern. Average pairwise correlations across strategy proxies rose 98% during the COVID drawdown but only 19% during the yen carry unwind. The Bridgewater risk-parity replicator drew down -15.7% in 2020 but gained +0.9% in 2024, the cleanest architectural differentiation in the dataset. The credit-liquidity hypothesis survived a within-study falsification test that could have failed: if the same regression signature had appeared in 2024, the mechanism would be indistinguishable from generic regime-break stress.

This paper makes three contributions. First, it provides a comparative empirical framework for evaluating institutional risk architectures using public data. Second, it identifies the credit-liquidity channel as the specific mechanism that explains correlated failure in 2020 and predicts its absence in 2024. Third, it offers a reproducible data pipeline and falsifiable hypothesis that future research can test on out-of-sample events. The contributions are bounded by their evidence base: two events cannot prove a causal mechanism, the Bridgewater and Two Sigma proxies introduce magnitude uncertainty, and event-window regressions with 22-42 observations have limited statistical power. Section 3 details the methodology. Sections 4 and 5 present the event-level findings. Section 6 synthesizes the cross-event evidence. Section 7 addresses limitations. Section 8 presents a robustness check, and Section 9 concludes.

---

## Section 2: Background and Architecture Taxonomy

This section develops the architectural framework that organizes the empirical analysis. A note on method: the hypotheses below were refined iteratively during the research process rather than pre-registered before data collection. The architectural distinctions (execution-layer versus risk-model versus risk-parity versus signal-layer) were specified first, but the specific predictions about how each architecture would behave under stress were sharpened as the empirical patterns became visible during pipeline construction. This paper is therefore exploratory rather than confirmatory: it documents patterns across two regime breaks and proposes a mechanism consistent with them, rather than testing pre-committed predictions. Section 7 discusses the implications of this for the strength of the inference.

### 2.1 JPMorgan: execution-layer AI on a discretionary mandate

**Architectural claim:** JPMorgan deploys AI at the *execution* layer, including order routing, liquidity prediction, and contract parsing, while investment decisions remain human-directed. This architecture should be insensitive to regime breaks, because microstructure-layer optimization does not depend on the stability of cross-asset covariance matrices.

JPMorgan's public AI footprint is concentrated in three areas. First, COiN (Contract Intelligence), a natural language processing system that parses commercial lending agreements. Bloomberg reported in 2017 that COiN reviewed 12,000 annual commercial credit agreements in seconds, work that previously required approximately 360,000 hours of lawyer time (Son, 2017). Second, LOXM, a reinforcement-learning-based order routing system designed to execute large equity orders with minimal market impact. LOXM operates within the firm's electronic trading desk and optimizes execution price across dark pools and lit venues (JPMorgan 2024 Annual Report). Third, the JEPI and JEPQ family of systematic option-overlay ETFs. JEPI (launched May 2020) writes S&P 500 equity-linked notes to generate income; JEPQ (launched May 2022) applies a similar strategy to the Nasdaq-100. Both are observable systematic products managed within JPM's asset management division, but neither existed during the March 2020 event.

The public AI footprint at JPMorgan concentrates at the execution layer. JPMorgan does run quantitative investment strategies in its asset management arm (including JEPI, JEPQ, and various systematic equity funds), but these are not the firm's primary risk-taking activity. JPM equity reflects primarily bank balance-sheet fundamentals (loan-loss provisions, mark-to-market on trading books), and any AI-driven positioning would contribute only minimally to top-line equity returns. This makes JPM a useful comparison point: a firm whose AI architecture is observable but whose equity behavior is dominated by traditional banking dynamics.

**Testable hypothesis:** JPM equity should behave like a leveraged beta exposure in both events, with drawdowns exceeding the S&P 500 due to credit-cycle amplification. This hypothesis is evaluated against the 2020 and 2024 event data in Sections 4.5 and 5.5.

### 2.2 BlackRock: factor-covariance risk models (Aladdin)

**Architectural claim:** BlackRock's Aladdin platform performs factor-based risk decomposition using historical covariance matrices estimated over rolling windows. This architecture is *vulnerable* to regime breaks because correlations estimated on pre-crisis data systematically understate cross-asset comovement during stress. When multiple institutional clients run similar Aladdin-derived risk overlays, common-mode de-risking can amplify drawdowns.

Aladdin's scale is difficult to overstate. BlackRock's Form 10-K for fiscal year 2025 (filed February 2026) reports total assets under management of $14.0 trillion as of 31 December 2025 (BlackRock 10-K FY2025, Item 1: Business, Overview). BlackRock has reported separately, in investor communications and December 2025 disclosures, that approximately $25 trillion in assets across BlackRock and its institutional clients are managed on the Aladdin platform. This figure is not disclosed in the 10-K body but appears in BlackRock's investor day materials and public statements. The platform's scale has drawn regulatory attention to systemic concentration risk. The UK Financial Conduct Authority (FCA, 2021) stated that the failure of a large portfolio and risk system such as Aladdin "could cause serious consumer harm" or "damage market integrity." In the United States, the Financial Stability Oversight Council examined whether risk-modelling firms warrant enhanced scrutiny, citing concerns that "financial firms may rely too heavily on the same outside risk models" (FSOC, 2014). These regulatory statements articulate the systemic concern that motivates this paper's empirical test: when a single risk platform overlays trillions in nominally diverse portfolios, correlated de-risking during stress is a mechanical consequence of shared inputs, not an emergent failure.

For this study, BlackRock's product behavior is observable through its iShares ETF family. IVV (Core S&P 500), AGG (Core U.S. Aggregate Bond), TLT (20+ Year Treasury), EEM (Emerging Markets), and HYG (High Yield Corporate Bond) are managed by BlackRock Fund Advisors and overseen through the same risk infrastructure as Aladdin. A clarifying caveat: these iShares ETFs are passively managed index-tracking products, so their stress-period behavior is driven primarily by the behavior of their underlying indexes (Bloomberg US Aggregate, ICE BofA High Yield, etc.) rather than by active risk decisions from Aladdin. The test in this paper is therefore not whether Aladdin caused specific allocation changes, but whether the broader pattern of correlations across BlackRock-managed products is consistent with shared-risk-model effects that the FCA and FSOC have flagged as systemic concerns.

**Testable hypothesis:** BlackRock-managed products should exhibit high cross-correlation during stress, consistent with shared risk-model influence. A caveat: iShares ETFs are index-tracking products, so much of their behavior reflects underlying index methodology rather than active Aladdin recommendations. The test in Section 4.3 addresses whether stress-period correlations rise beyond what index-tracking alone would predict.

### 2.3 Bridgewater: regime-aware risk parity

**Architectural claim:** Bridgewater's All Weather strategy allocates capital to equalize risk contribution across asset classes, using leverage to bring low-volatility assets (bonds, TIPS) up to the risk level of equities. The architecture is *selectively vulnerable*: it should suffer disproportionately when the bond-equity correlation inverts (both asset classes falling together), because risk parity assumes diversification across uncorrelated risk premia.

All Weather was designed by Ray Dalio and colleagues in the 1990s as a portfolio that would perform acceptably across economic regimes: growth, recession, rising inflation, falling inflation. The strategy's design principles are described in Bridgewater's white paper "The All Weather Story" (Bridgewater Associates, 2012). The academic treatment of risk parity is given by Asness, Frazzini, and Pedersen (2012), who formalize the leverage-aversion argument that motivates the strategy. Wigglesworth (2021) provides historical context on the broader risk-parity movement that followed the 2008 financial crisis.

All Weather's returns are private. Press reports in April 2020 indicated the fund lost approximately -14% in Q1 2020, substantially exceeding its stated annualized volatility target of approximately 10-12%. Press reports in January 2023 indicated a full-year 2022 loss of approximately -9.4%. The author has not been able to verify the specific underlying articles to primary sources within the constraints of this working paper; the figures are reported here as press estimates and should be confirmed against Bloomberg or FT primary sources in any peer-reviewed revision. Pure Alpha, Bridgewater's actively managed macro fund, operates on different principles and is excluded from this analysis. This study uses a risk-parity replicator (described in Section 3.4) as a daily-frequency proxy for All Weather's broad risk profile. The replicator is validated against press-disclosed returns with a cross-period correlation of r=0.75 across four reference periods.

**Testable hypothesis:** Risk parity should break during events that cause simultaneous selloffs across equities and bonds (positive correlation) but should remain resilient during events that preserve the cross-asset diversification structure. This hypothesis is consistent with prior critiques of risk parity by Asness, Frazzini, and Pedersen (2012) and tested against the 2020 and 2024 event data in Sections 4.5 and 5.5.

### 2.4 Two Sigma: multi-factor systematic strategies

**Architectural claim:** Two Sigma runs short-to-medium-horizon systematic strategies across equity, macro, and event-driven mandates. The architecture operates at the *signal generation* layer: statistical models identify mispricings, and positions are taken algorithmically. This design exposes the firm to factor crowding: when many systematic shops hold similar positions, forced unwinds can produce correlated losses that the individual models do not anticipate.

Two Sigma was founded in 2001 by David Siegel and John Overdeck. As of 2024, the firm managed approximately $55-60 billion across its main funds: Compass (global macro), Spectrum (flagship multi-strategy systematic), and Absolute Return Enhanced (multi-strategy hedge fund). The exact AUM figure is reported variously in press coverage and is sensitive to the timing of fund flows and the inclusion of sub-strategies.

Two Sigma's returns are private. This study uses a factor ETF basket, MTUM (momentum), VLUE (value), QUAL (quality), USMV (minimum volatility), plus DBMF (managed futures, replicating the SocGen CTA Index), as a systematic factor proxy. The basket captures the broad exposure profile of a diversified multi-factor systematic shop. It does not capture Two Sigma's specific alpha, leverage, or dynamic hedging. The proxy is transparent about what it measures: the performance of publicly available systematic factor exposure, which serves as a lower bound on what a sophisticated systematic firm would achieve.

**Testable hypothesis:** Within the factor proxy, momentum exposure (MTUM) should show evidence of factor crowding during broad credit events but not during geographically concentrated events. This hypothesis is tested against the 2020 and 2024 event data in Section 4.4 and Section 5.4. A measurement caveat is noted in Section 4.4: MTUM holds equities that have had high recent returns, and its 2020 drawdown could reflect either factor crowding or simple holdings-level exposure to growth and quality stocks that fell during the COVID panic. The proxy cannot fully separate these two interpretations.

### 2.5 Summary of testable hypotheses

The four architectures suggest distinct predictions about how each firm's strategies should behave during regime breaks. Table 1 summarizes the architectural claims, the associated hypothesis, and the section where each is examined empirically. As noted at the start of this section, these hypotheses were refined during analysis rather than pre-registered; Table 1 should be read as an organizing framework for the empirical sections rather than as a set of pre-committed predictions.

**Table 1.** Summary of testable hypotheses by institutional architecture.

| Firm | Architectural claim | Testable hypothesis | Evaluated in |
|------|---------------------|---------------------|:--:|
| JPMorgan | Execution-layer AI; discretionary investment decisions | Drawdowns track equity beta plus balance-sheet credit exposure; insensitive to model-driven regime breaks | 4.5, 5.5 |
| BlackRock | Factor-covariance risk models on rolling windows (Aladdin) | High cross-product correlation under stress; correlations rise as shared risk-model inputs break | 4.3, 5.3 |
| Bridgewater | Regime-aware risk parity with leverage on low-vol sleeves | Fails when bond-equity correlation inverts; resilient when diversification structure holds | 4.5, 5.5 |
| Two Sigma | Multi-factor systematic strategies at signal-generation layer | Factor crowding under credit-liquidity stress; tracks market closely in non-credit regime breaks | 4.4, 5.5 |

This summary table provides a reference for the empirical sections. Section 4 evaluates each hypothesis against the COVID 2020 event. Section 5 evaluates each against the yen carry 2024 event. Section 6 synthesizes the cross-event evidence.

---

## Section 3: Data and Methodology

### 3.1 Research design

This paper uses a comparative case study design. Four institutional risk architectures, execution-layer AI (JPMorgan), factor-covariance risk modelling (BlackRock/Aladdin), regime-aware risk parity (Bridgewater), and multi-factor systematic strategies (Two Sigma), are observed through publicly available proxies during two regime-break events.

The two-event design is intentional. Each event activates a different stress mechanism: the March 2020 COVID drawdown was a credit-driven liquidity crisis affecting U.S. fixed income and equity simultaneously, while the August 2024 yen carry unwind was a rates-driven event geographically concentrated in Japanese equity markets. An architecture that fails in both events exhibits structural fragility. One that fails in only one exhibits conditional fragility, vulnerable to a specific mechanism but not to regime breaks in general. Single-event studies cannot make this distinction.

### 3.2 Data sources

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

### 3.3 Event windows

Two event windows are defined following the convention established by MacKinlay (1997) for financial event studies. Each window includes approximately 90 trading days before the event start, the event itself, and approximately 90 trading days after the event end.

**Event 1, COVID drawdown:**
- Pre-event: 2019-10-01 to 2020-02-18
- Event: 2020-02-19 (S&P 500 peak at 3,386.15) to 2020-03-23 (trough at 2,237.40; Fed unlimited QE announced)
- Post-event: 2020-03-24 to 2020-08-01

**Event 2, Yen carry unwind:**
- Pre-event: 2024-04-01 to 2024-07-30
- Event: 2024-07-31 (BoJ raises policy rate to 0.25%) to 2024-08-09 (stabilization)
- Post-event: 2024-08-10 to 2024-12-13

The 90-day buffer provides sufficient data for stable correlation estimation while remaining close enough to the event that the market regime has not shifted materially.

### 3.4 Firm proxies

**JPMorgan and BlackRock** are directly observable. JPMorgan Chase (ticker JPM) is publicly traded; its systematic products JEPI and JEPQ are public ETFs with daily NAV. BlackRock (ticker BLK) is publicly traded; the iShares family (IVV, AGG, TLT, EEM, HYG) represents BlackRock-managed products whose daily returns are available from Yahoo Finance. These proxies measure the performance of the firms' public-facing products, not their internal risk analytics. JPM equity in particular reflects bank balance-sheet dynamics, not execution-layer AI performance. JEPI and JEPQ launched after the 2020 event and are available only for the 2024 analysis.

**Bridgewater Associates** presents a proxy challenge. All Weather's daily returns are not published. This study constructs an inverse-volatility risk-parity replicator using five ETFs: IVV (S&P 500 equity), TLT (20+ year Treasuries), TIP (TIPS), DBC (broad commodities), and GLD (gold). Weights are set proportional to inverse trailing 60-day volatility, rebalanced daily. The portfolio is vol-targeted to 10% annualized with a leverage cap of 1.5x.

The 1.5x leverage cap is set conservatively below All Weather's reported 3-4x to ensure that the replicator can be funded by retail-accessible ETFs without exotic financing arrangements. This choice makes the replicator a *lower bound* on risk parity's vulnerability: where the replicator shows distress, an actual leveraged All Weather position would show more. The Pearson correlation of r=0.75 against four publicly disclosed return periods confirms the replicator captures the directional risk profile even with reduced leverage. The trailing 60-day volatility window used for inverse-volatility weights uses only data from days strictly before the rebalance date, eliminating any look-ahead bias in the construction.

The replicator is *not* All Weather. It differs in three known ways. First, leverage: All Weather reportedly uses 3-4x leverage on the bond sleeve; we cap at 1.5x. Second, construction: we use ETFs, not futures; financing costs differ. Third, regime overlay: Bridgewater employs a systematic macro overlay that adjusts allocations based on regime identification; we cannot replicate this.

Despite these differences, the replicator achieves a Pearson correlation of r=0.75 against four publicly disclosed All Weather return figures across 2020-2023 (see Figure 1 and Table 2). The replicator consistently captures the correct sign of returns, negative when All Weather lost money, positive when it gained, but understates magnitude, consistent with the lower leverage. This means our empirical findings about risk-parity fragility represent *conservative* estimates of the actual fund's vulnerability. If the replicator drew down -15.7% in March 2020, the actual fund's reported -14% quarterly loss (which includes the January-February runup before the drawdown) implies a sharper peak-to-trough decline than what we measure.

![**Figure 1.** Bridgewater risk-parity replicator validation. Replicator quarterly returns compared against publicly disclosed All Weather returns across four reference periods. Pearson correlation r = 0.75. Source: outputs/tables/table0_bridgewater_validation.csv.](outputs/figures/fig0_bridgewater_validation.png){width=85%}

A footnote on validation: In March 2025, State Street Global Advisors and Bridgewater jointly launched the SPDR Bridgewater All Weather ETF (ALLW), an actively managed multi-asset ETF sub-advised by Bridgewater implementing the All Weather approach. ALLW post-dates both event windows in this study and therefore cannot be used directly. Its existence does, however, validate the broader methodological approach: an ETF-based implementation of risk parity is sufficiently faithful to the underlying strategy that Bridgewater itself has now publicly endorsed one. Future research building on this paper should use ALLW as a higher-fidelity proxy from March 2025 forward.

**Two Sigma** also requires a proxy. The firm's fund returns (Compass, Spectrum, Absolute Return Enhanced) are not public. We construct a systematic factor proxy: an equal-weight basket of five ETFs that span the dominant systematic factor exposures. MTUM (momentum), VLUE (value), QUAL (quality), and USMV (minimum volatility) represent the core equity factors; DBMF (managed futures, replicating the SocGen CTA Index) captures the trend-following and macro components that characterize systematic macro strategies. This proxy captures the *exposure profile* of a diversified multi-factor systematic shop. It does not capture Two Sigma's alpha, leverage, or dynamic hedging. Returns should be interpreted as the performance of passively held systematic factor exposure, a useful benchmark against which actual fund returns can be compared but not a substitute for them.

The basket uses equal weights rather than risk-weighted or capitalization-weighted construction because Two Sigma's actual cross-fund allocation is private. Equal-weighting provides a neutral aggregation that does not embed any specific assumption about Two Sigma's internal weights. Where the equal-weighted basket shows a clean signal (as MTUM does for the credit-liquidity channel), the signal is unlikely to be an artifact of weighting choice.

### 3.5 Empirical methods

Five analyses are applied to the data. All use log returns, which aggregate additively across time and simplify drawdown decomposition.

**Drawdown analysis.** For each strategy and event, we compute the peak-to-trough drawdown from cumulative wealth starting at the event onset. Recovery time is measured as the number of calendar days from trough until cumulative wealth returns to its pre-drawdown level.

**Correlation regime-shift analysis.** Pairwise Pearson correlations are computed across all strategy proxies in three windows: pre-event, event, and post-event. The headline metric is average off-diagonal correlation. A large increase from pre-event to event-window correlation indicates that nominally diverse strategies converged during stress, the empirical signature of common-mode risk-model failure.

**Volatility breach analysis.** For each strategy, event-window annualized volatility (daily standard deviation times the square root of 252) is compared to long-run annualized volatility estimated over the full sample. A breach ratio exceeding 3x suggests that the strategy's risk model failed to anticipate the realized volatility.

**Liquidity-dependency regression.** For each strategy proxy, the daily log return on day t is regressed on three predictors: the contemporaneous S&P 500 log return on day t (market beta), the contemporaneous VIX log return on day t (volatility-of-volatility), and the one-day-lagged Corwin-Schultz bid-ask spread estimate from day t-1 (liquidity). The specification is:

r_{i,t} = α + β₁·r_{sp,t} + β₂·r_{vix,t} + β₃·spread_{i,t-1} + ε_{i,t}     (1)

where r_{i,t} is the day-t log return for strategy i, r_{sp,t} is the contemporaneous S&P 500 log return, r_{vix,t} is the contemporaneous VIX log return, spread_{i,t-1} is the Corwin-Schultz bid-ask spread estimate from day t-1, and ε_{i,t} is an error term.

Standard errors are computed using the Newey-West (1987) heteroskedasticity- and autocorrelation-consistent (HAC) estimator with 5 lags. The standard automatic lag selection rule of 4(T/100)^(2/9) suggests 3 lags for T=22-42. Five lags is therefore slightly aggressive given the small event-window samples; this is noted as a robustness concern in Section 7.5. Re-estimation with 3 lags produces qualitatively similar significance for the 2020 coefficients and is reported in the analysis pipeline output. The coefficient on the lagged spread tests whether returns are predictable from liquidity conditions after controlling for market beta and volatility. A significant negative coefficient means wider spreads predict lower next-day returns, the channel identified by Brunnermeier and Pedersen (2009) linking funding liquidity to market liquidity.

The Corwin-Schultz (2012) spread estimator uses two consecutive days' high and low prices to estimate the effective bid-ask spread without requiring intraday data. The estimator assumes that daily high prices are typically buyer-initiated and daily low prices are seller-initiated. Negative or implausible estimates (exceeding 50% of price) are set to missing following the authors' recommendation.

**Event-window regression.** The same regression specification is estimated separately within each event window (plus 30 trading days on each side) to test whether the spread coefficient is significant during specific crises. This tests the credit-liquidity mechanism directly: if the coefficient is significantly negative in 2020 (credit event) but not in 2024 (rates event), the evidence supports the hypothesis that common-mode failure is conditional on U.S. credit liquidity stress.

### 3.6 Reproducibility

The data pipeline is publicly available at the project GitHub repository. All raw data files are cached to disk before any transformation and hashed with SHA-256. The `manifest.json` file generated on each run records the UTC timestamp, Python version, package versions (pandas, numpy, yfinance), the SHA-256 hash of every raw file, and an explicit list of methodological limitations. Anyone with the pipeline script and a free FRED API key (available at fred.stlouisfed.org) can reproduce the exact dataset and all derived analyses.

### 3.7 Limitations

Two events do not constitute a statistical sample. The results describe observed behavior during two specific regime breaks. They cannot distinguish architectural failure from coincidence with inferential rigor, nor can they rule out confounds arising from differences in event duration (23 trading days versus 8), magnitude (S&P -33.9% versus -6.1%), or geographic scope (global versus Asia-concentrated).

The Bridgewater and Two Sigma proxies approximate but do not replicate the actual funds' returns. The Bridgewater replicator understates volatility due to its leverage cap. The Two Sigma proxy excludes alpha, leverage, and hedging. ETF returns include creation/redemption frictions not present in institutional portfolios.

Event-window regressions operate on 22 to 42 observations per window, limiting statistical power. The significant coefficients in the 2020 window are suggestive but would not survive a Bonferroni correction for multiple comparisons across strategies. The Corwin-Schultz spread estimator, while established in the literature, is less precise than intraday TAQ-based measures.

---

## Section 4: Event 1, COVID Drawdown (February to March 2020)

### 4.1 Event context

The S&P 500 peaked at 3,386.15 on February 19, 2020, and bottomed at 2,237.40 on March 23, a -33.9% decline over 23 trading days. The Federal Reserve responded in three escalating interventions: a March 15 emergency rate cut to 0-0.25%, the March 17 launch of the Commercial Paper Funding Facility, and the March 23 announcement of unlimited Treasury and agency MBS purchases, which marked the bottom.

The March 2020 dislocation operated through multiple channels simultaneously: U.S. credit markets, the Treasury market, FX swap markets, commodities, and equities all dislocated. This paper foregrounds the credit-liquidity channel because it is the channel most clearly tested by Corwin-Schultz spread regressions on the specific instruments in the panel (AGG, HYG, TLT). The Treasury basis trade unwind documented by Schrimpf, Shin, and Sushko (2020) operated alongside the credit-liquidity channel and is partly observable through TLT and the Bridgewater replicator's bond sleeve. The two mechanisms overlap (both involve forced selling by leveraged participants) but are not identical; the analysis here does not isolate them. The ICE BofA U.S. High Yield Option-Adjusted Spread (FRED series BAMLH0A0HYM2) peaked at approximately 1,100 basis points on March 23, 2020, the day the Federal Reserve announced unlimited QE. Investment-grade corporate bond markets froze: dealers could not warehouse inventory, and ETF market-makers widened spreads or stopped quoting entirely. This mechanism is documented in detail by Duffie (2023), who identifies dealer balance sheet capacity constraints as the binding friction during the March 2020 Treasury market dysfunction. Goldberg (2020) showed that the price of liquidity in the Treasury market rose sharply as dealer inventory capacity declined, with historical precedent suggesting persistent spillovers to corporate bond, equity, and MBS markets. Fleming and Ruela (2020) document the contemporaneous deterioration of Treasury market liquidity metrics during the period. Treasury-equity correlations, normally negative (Treasuries rally when equities sell off), broke down as forced sellers liquidated across asset classes simultaneously. The Fed's March 23 intervention targeted credit markets directly, not equities, because the credit channel was the systemic threat.

### 4.2 Per-firm drawdowns

**JPMorgan.** JPM equity fell -42.5% peak-to-trough, exceeding the S&P 500's -33.9% by 8.6 percentage points. The excess is consistent with the Section 2.1 hypothesis: bank equities carry credit-cycle exposure (loan-loss provisions, trading book mark-to-market losses) on top of market beta. JPM's event-window total return was -41.7%. The AI execution layer (COiN, LOXM, internal order routing) does not appear in these numbers. The drawdown reflects balance-sheet fundamentals, not model failure. JEPI and JEPQ did not exist during this event.

**BlackRock products.** IVV tracked the S&P 500 almost exactly at -33.9%, as expected for a passively managed index ETF. The fixed-income products told a different story. AGG (U.S. Aggregate Bond) drew down -9.6% and recovered within 7 days once the Fed intervened. TLT (20+ Year Treasuries) fell -15.7% before recovering within a single trading day of its March 18 trough, coincident with expectations of the Fed's intervention. HYG (High Yield) dropped -22.0%, the worst-performing BlackRock product, consistent with its direct exposure to the credit-liquidity channel that defined this crisis. EEM (Emerging Markets) fell -30.8%. The critical observation: AGG and TLT, designed as diversifiers against equity risk, moved in the same direction as equities, the safe-haven failure that makes this a regime break rather than an ordinary correction.

**Bridgewater replicator.** The risk-parity replicator drew down -15.7% peak-to-trough with an event-window total return of -10.6%. Recovery took 135 days, the longest of any strategy in the panel, reflecting the persistent dislocations in TIPS and commodities that lasted well into Q2 2020. Press reports placed actual All Weather losses at approximately -14% for Q1 2020 (financial press, April 2020; specific articles not verified to primary source by the author). The replicator's shallower quarterly loss (-8.1% for Q1 2020) is expected given the 1.5x leverage cap versus All Weather's reported 3-4x on the bond sleeve. The "conservative estimate" framing from Section 3.4 applies: if the replicator shows distress, the actual fund likely experienced more.

**Two Sigma factor proxy.** The factor basket fell -30.1%, slightly outperforming the S&P 500's -33.9%. The modest cushioning came from DBMF (managed futures, -10.4% drawdown) and USMV (minimum volatility, -33.0%). MTUM (momentum) tracked the index at -34.1%, while VLUE (value) underperformed at -38.8%. This is the only architecture where the composite proxy slightly outperformed the index during the drawdown, a fact that makes the MTUM regression finding in Section 4.4 more striking: even within a basket that held up marginally better than the market, the momentum component showed clear signs of liquidity-driven forced selling.

Each architecture's drawdown is explicable in its own terms. But the event-window regression in Section 4.4 reveals they shared a common mechanism.

![**Figure 2.** Strategy drawdowns during the COVID 2020 event window. Peak-to-trough declines between February 19 and March 23, 2020. Source: outputs/tables/table1_drawdowns.csv.](outputs/figures/fig1_drawdowns_covid_2020.png){width=85%}

**Table 3.** Peak-to-trough drawdowns by strategy proxy, COVID 2020 event (February 19 to March 23, 2020).

| Strategy / Proxy | Peak-to-trough | Recovery days |
|------------------|---------------:|--------------:|
| S&P 500 (benchmark) | -33.9%      | --            |
| JPM equity       | -42.5%         | --            |
| IVV (S&P 500)    | -33.9%         | --            |
| AGG              | -9.6%          | 7             |
| TLT              | -15.7%         | 1             |
| HYG              | -22.0%         | --            |
| EEM              | -30.8%         | --            |
| Bridgewater replicator | -15.7%   | 135           |
| Two Sigma factor proxy | -30.1%   | --            |
| MTUM             | -34.1%         | --            |
| VLUE             | -38.8%         | --            |
| USMV             | -33.0%         | --            |
| DBMF             | -10.4%         | --            |

Source: outputs/tables/table1_drawdowns.csv.

### 4.3 Correlation regime shift

Average off-diagonal correlation across the strategy proxies rose from 0.25 pre-event to 0.50 in the event window, a 98% increase. Post-event, correlations settled at 0.41, remaining elevated above the pre-event baseline.

The most revealing pair correlations involve AGG, the U.S. Aggregate Bond ETF. Before the event, AGG was negatively correlated with every equity-linked strategy in the panel, the defining property that makes bonds useful as a portfolio diversifier. AGG-IVV correlation was -0.54 pre-event; during the event window it flipped to +0.18. AGG-JPM moved from -0.62 to +0.18. AGG-EEM shifted from -0.52 to +0.25. Every nominally negative correlation with AGG collapsed or reversed.

The Bridgewater replicator showed a similarly dramatic shift. Its pre-event correlation with IVV was -0.003, almost perfectly uncorrelated, exactly the diversification that risk parity targets. During the event, it jumped to +0.46. Risk parity's core assumption, that its asset class exposures will not all move together, broke precisely when it mattered. HYG-IVV correlation rose from 0.73 to 0.92, approaching unity: high-yield credit and equities became nearly the same trade.

These shifts are consistent with common-mode failure. Strategies designed to diversify one another behaved as if they were the same position.

![**Figure 3.** Correlation heatmaps for the COVID 2020 event across pre-event, event, and post-event windows. Average off-diagonal correlation rose from 0.25 pre-event to 0.50 during the event window, a 98 percent increase. Source: outputs/tables/table2_corr_covid_2020_*.csv.](outputs/figures/fig2_corr_covid_2020.png){width=85%}

### 4.4 Liquidity regression and the credit-liquidity channel

The event-window liquidity regression (Analysis 4b) tests whether bid-ask spread widening predicted next-day strategy returns within the crisis window, after controlling for market beta and volatility. This is the methodologically critical test: it identifies the specific mechanism, credit-liquidity stress, that explains why nominally diverse strategies converged.

Three strategies showed significant negative lagged spread coefficients in the 2020 event window:

**Table 4.** Event-window liquidity regression coefficients, COVID 2020. Coefficient on lagged Corwin-Schultz bid-ask spread, after controlling for contemporaneous S&P 500 and VIX returns. Newey-West HAC standard errors with 5 lags.

| Strategy | beta (lagged spread) | t-statistic | p-value | N |
|----------|------------------:|------------:|--------:|---:|
| AGG      | -1.16             | -2.75       | 0.006   | 33 |
| HYG      | -0.47             | -3.62       | <0.001  | 35 |
| MTUM     | -0.13             | -2.82       | 0.005   | 42 |
| Bridgewater replicator | +0.03 | +0.33     | 0.74    | 33 |
| Two Sigma factor proxy | +0.06 | +1.50     | 0.13    | 33 |

Source: outputs/tables/table4b_liquidity_regression_by_window.csv.

The interpretation is direct. When bid-ask spreads widened on day t-1, each strategy's return on day t was significantly lower, even after controlling for the contemporaneous S&P 500 return (market beta) and VIX change (volatility-of-volatility). This pattern is consistent with Brunnermeier and Pedersen's (2009) funding-liquidity channel: when funding tightens, participants who must sell into illiquid markets push prices down further, and those widened spreads predict continued losses the following day.

The selection of these three strategies is not random; it traces the specific channel of credit-liquidity stress. AGG holds investment-grade credit and Treasuries; these are the instruments that institutional investors sell first when they need cash, because they are normally liquid. When that liquidity evaporates, the selling becomes self-reinforcing. HYG holds high-yield credit, the most stressed segment of the bond market in March 2020; the ICE BofA high-yield OAS more than tripled in three weeks, reflecting panic-driven forced selling. MTUM holds whatever recent winners were, and recent winners are the crowded systematic trades. When liquidity tightens across the system, these positions are unwound first because they are held by the most leveraged and most liquidity-sensitive participants.

A measurement caveat applies to the MTUM result. MTUM holds equities that have had high recent returns; in early 2020 this meant a concentration in technology and quality stocks. These stocks fell during the COVID panic for reasons that include but are not limited to factor crowding (valuation compression, growth re-rating, and general flight-to-cash dynamics). The negative lagged spread coefficient on MTUM is consistent with a factor-crowding interpretation, but it is also consistent with a simpler holdings-driven story in which MTUM's underlying stocks responded to liquidity stress in the same way the broader market did. Distinguishing these two interpretations would require decomposing MTUM returns into factor exposure and idiosyncratic stock-level reaction, which is beyond the scope of this paper. The MTUM finding is therefore reported as consistent with factor crowding rather than as conclusive evidence of it.

The Bridgewater replicator did not show a significant negative spread coefficient (t = 0.33, p = 0.74). Nor did the Two Sigma factor proxy (t = 1.50, p = 0.13). Bridgewater's broader diversification across asset classes, including commodities, gold, and TIPS, reduced its direct exposure to the credit-liquidity channel even as bond-equity correlations broke. The Two Sigma factor basket averages across momentum, value, quality, and minimum volatility factors; this diversification dilutes the MTUM crowding signal that appears clearly when MTUM is measured in isolation. These non-results are consistent with the hypothesis: the credit-liquidity channel targets specific instruments and positions, not all architectures equally.

The Corwin-Schultz (2012) spread estimator used here relies on daily high-low prices. Intraday TAQ data would provide more precise spread measurement but is not freely available. This limitation is noted in Section 3.7.

### 4.5 Architectural verdict

Each architecture's 2020 performance can be evaluated against the testable hypothesis stated in Section 2.

**JPMorgan: hypothesis confirmed.** Balance-sheet credit exposure produced the excess drawdown (-42.5% versus S&P -33.9%), not AI or model failure. The execution-layer architecture is insensitive to regime breaks because the AI operates below the level of portfolio positioning.

**BlackRock: hypothesis confirmed.** BlackRock-managed products showed correlated drawdowns across nominally diverse asset classes. IVV tracked the index; AGG and TLT broke from their normal negative equity correlation; HYG, EEM, and equities moved together with near-unity correlation. This is consistent with a shared risk-model framework in which factor-covariance estimates trained on pre-crisis data understated cross-asset comovement during stress.

**Bridgewater: hypothesis confirmed.** Risk parity broke when bond-equity correlation inverted, the specific architectural vulnerability identified in Section 2.3. The replicator's -15.7% drawdown matches the direction and approximate magnitude of the fund's disclosed Q1 2020 loss (-14%). The 135-day recovery reflects the persistent nature of the correlation break.

**Two Sigma: partial confirmation.** The composite factor proxy outperformed the S&P slightly (-30.1% versus -33.9%), failing to show the severe underperformance the crowding hypothesis might predict at the basket level. But the MTUM regression signal (p = 0.005) provides direct evidence of factor crowding within the basket. The hypothesis is supported for the momentum component specifically, not the diversified composite.

The credit-liquidity channel suggested by Section 4.4 explains why these architecturally distinct strategies converged. They did not fail for the same reason: JPM lost money on its balance sheet, Bridgewater lost money because its diversification assumption broke, MTUM lost money because crowded positions were unwound. But they shared exposure to the same underlying mechanism: when U.S. credit liquidity froze, all roads led to the same forced-selling dynamic.

The empirical findings of this section translate directly into the regulatory concerns articulated in Section 2.2. The FCA (2021) and FSOC (2014) warned that shared risk-model exposure could produce correlated de-risking during stress. The 2020 event window provides precisely the empirical conditions under which this prediction is testable. Average pairwise correlations rose 98 percent. AGG, TLT, EEM, and equities moved together when their normal diversification relationship would predict the opposite. The regulatory concern was specific and falsifiable, and the 2020 data confirm it. Section 6.3 returns to the policy implications of this confirmation.

---

## Section 5: Event 2, Yen Carry Unwind (August 2024)

### 5.1 Event context

On July 31, 2024, the Bank of Japan raised its policy rate to 0.25% from 0.1%, ending decades of near-zero rates. The yen, trading near multi-decade lows around 155 per dollar, strengthened sharply. By August 5, the Nikkei 225 fell 12.4% in a single session, its largest one-day loss since the 1987 Black Monday crash. The VIX spiked intraday to 65.73. USD/JPY fell from approximately 155 to 142 in five sessions before stabilizing.

The cascade reflected forced unwinds of yen-funded carry trades, that is, leveraged positions in higher-yielding assets financed in cheap yen that became uneconomic when funding costs rose and the currency strengthened. Carry trade unwinds are mechanically distinct from credit crises: the shock originates in rates and FX, not in credit spreads or corporate default risk. The Bank for International Settlements (2024), in its analysis of the event, attributes the cascade to "deleveraging pressures and increases in margins" affecting "strategies that rely on extensive leverage and are predicated on contained volatility," explicitly drawing on the Brunnermeier and Pedersen (2009) funding-liquidity framework that motivates this paper's regression specification. The BIS estimates that yen-denominated loans to non-banks outside Japan reached approximately 40 trillion yen ($250 billion) by March 2024, providing a measure of the carry trade's potential unwind volume.

This was not a U.S. credit event. The ICE BofA High Yield OAS (FRED series BAMLH0A0HYM2) peaked at 393 basis points on August 5, 2024, well below the 1,100 bps reached in March 2020. HYG drew down only -1.2% peak-to-trough and recovered in 8 days. The U.S. credit-liquidity channel that defined the 2020 event was absent.

### 5.2 Per-firm drawdowns

**JPMorgan.** JPM equity fell -8.4% versus the S&P 500's -6.1%, recovering in 11 days. The 2.3 percentage point excess over the index is smaller than the 8.6 point excess in 2020, consistent with a milder balance-sheet shock. JEPI drew down -3.9% and recovered in 10 days; JEPQ fell -6.7% and recovered in 8 days. Both systematic products behaved within normal parameters for a moderate equity correction.

**BlackRock products.** IVV tracked the S&P at -6.0%, recovering in 10 days. TLT fell -11.1% and did not recover within the post-event window. This drawdown can be read two ways. The first reading attributes the loss to a structural repricing of global duration following the BoJ rate hike, in which case it is not a failure of BlackRock's risk architecture per se but a market response to a policy shock. The second reading treats it as risk-parity-style fragility to rate shocks, in which case the magnitude (-11.1%) is comparable to TLT's -15.7% drawdown in March 2020 and the architectural distinction between events is weaker than the headline correlation numbers suggest. The paper does not resolve which reading is correct; both are consistent with the data. AGG drew down -3.7%. Unlike 2020, AGG's loss was modest and directionally consistent with a rates-driven move rather than credit-liquidity breakdown.

**Bridgewater replicator.** The replicator gained +0.9% over the event window with a peak intra-window drawdown of only -4.6%. The contrast with the -15.7% drawdown in 2020 is the cleanest single piece of architectural evidence in the paper. Risk parity was largely unaffected because the yen carry unwind did not trigger the bond-equity correlation inversion that breaks the strategy. Rates repriced, but the diversification assumption, that equities, bonds, commodities, and TIPS do not all move in the same direction at the same time, held.

**Two Sigma factor proxy.** The factor basket fell -6.2%, tracking the S&P 500's -6.1% almost exactly, and took 14 days to recover. MTUM drew down -8.1% but recovered in 10 days. VLUE fell -7.9%. No factor in the basket showed disproportionate stress, consistent with a shock that did not trigger U.S. factor crowding dynamics.

![**Figure 4.** Strategy drawdowns during the yen carry 2024 event window. Peak-to-trough declines between July 31 and August 9, 2024. Source: outputs/tables/table1_drawdowns.csv.](outputs/figures/fig1_drawdowns_yen_carry_2024.png){width=85%}

**Table 5.** Peak-to-trough drawdowns by strategy proxy, yen carry 2024 event (July 31 to August 9, 2024).

| Strategy / Proxy | Peak-to-trough | Recovery days |
|------------------|---------------:|--------------:|
| S&P 500 (benchmark) | -6.1%       | 10            |
| JPM equity       | -8.4%          | 11            |
| JEPI             | -3.9%          | 10            |
| JEPQ             | -6.7%          | 8             |
| IVV              | -6.0%          | 10            |
| TLT              | -11.1%         | did not recover |
| AGG              | -3.7%          | --            |
| HYG              | -1.2%          | 8             |
| Bridgewater replicator | +0.9% gain | --         |
| Two Sigma factor proxy | -6.2%    | 14            |
| MTUM             | -8.1%          | 10            |
| VLUE             | -7.9%          | --            |
| Nikkei 225       | -19.5%         | --            |

Source: outputs/tables/table1_drawdowns.csv.

### 5.3 Correlation regime shift

Average off-diagonal correlation rose from 0.37 pre-event to 0.44 in the event window, a 19% increase, compared with the 98% increase observed in 2020. Post-event, correlations fell to 0.34, actually declining below the pre-event level.

Strategies maintained substantially more independence than during the COVID drawdown. The most notable pair shifts moved in the opposite direction from 2020: HYG-TLT correlation swung from +0.65 pre-event to -0.59 during the event; high-yield credit and long Treasuries moved in opposite directions, the normal safe-haven relationship. AGG-HYG dropped from +0.76 to -0.41. These are divergence patterns, not the convergence that characterized 2020.

Three factors explain the difference. First, the shock was geographically concentrated: Japan's Nikkei bore the brunt (-19.5%) while the S&P 500 lost only -6.1%. Second, the event lasted 8 trading days versus 23; shorter stress periods produce less forced de-risking and less cross-asset contagion. Third, and most important for the credit-liquidity hypothesis: U.S. credit markets did not freeze. Dealers continued to make markets, bid-ask spreads widened modestly, and the mechanism that drives forced cross-asset selling in credit crises simply did not activate.

![**Figure 5.** Correlation heatmaps for the yen carry 2024 event across pre-event, event, and post-event windows. Average off-diagonal correlation rose from 0.37 to 0.44, a 19 percent increase. Source: outputs/tables/table2_corr_yen_carry_2024_*.csv.](outputs/figures/fig2_corr_yen_carry_2024.png){width=85%}

### 5.4 The absence is informative

The event-window regression (Analysis 4b) for the 2024 window shows no strategy with a significant negative lagged spread coefficient. None. This is the falsifiable test from the credit-liquidity hypothesis.

The hypothesis predicts that common-mode failure in 2020 was caused specifically by U.S. credit-liquidity stress, not by regime breaks in general. A regime break that does not involve U.S. credit-liquidity stress should therefore not produce the same regression signature. The 2024 yen carry unwind provides exactly this test: a severe market dislocation (Nikkei -12.4% in a single day, VIX above 65 intraday) that did not activate the U.S. credit channel. The test could have failed. If AGG, HYG, and MTUM had shown significant negative spread coefficients in 2024 too, the credit-liquidity mechanism would be indistinguishable from a generic "regime breaks cause forced selling" explanation. They did not.

Two strategies showed significant positive spread coefficients in 2024: HYG (beta = +0.71, t = 1.98, p = 0.048) and the Bridgewater replicator (beta = +0.26, t = 1.97, p = 0.048). Positive coefficients mean that wider spreads on day t-1 predicted higher returns on day t, the opposite of forced selling. This is consistent with mean reversion after a brief volatility spike: spreads widened transiently, then markets snapped back. The mechanism is economically distinct from the 2020 pattern.

**Table 6.** Event-window liquidity regression coefficients, yen carry 2024. Coefficient on lagged Corwin-Schultz bid-ask spread. Two strategies show significant *positive* coefficients, consistent with mean reversion.

| Strategy | beta (lagged spread) | t-statistic | p-value | N |
|----------|------------------:|------------:|--------:|---:|
| HYG      | +0.71             | +1.98       | 0.048   | 33 |
| Bridgewater replicator | +0.26 | +1.97     | 0.048   | 37 |
| AGG      | +0.91             | +1.31       | 0.19    | 24 |
| MTUM     | +0.02             | +0.18       | 0.86    | 37 |
| Two Sigma factor proxy | +0.03 | +0.39     | 0.69    | 37 |

Source: outputs/tables/table4b_liquidity_regression_by_window.csv.

Scope matters. Two events cannot prove a causal mechanism. A non-result is consistent with the hypothesis but does not prove it. A third event with severe market dislocation but no U.S. credit stress, such as the March 2023 regional bank crisis (SVB, Signature, First Republic), would strengthen the inference. The event-window regressions operate on 22 to 37 observations per window (n varies by ticker and data availability), limiting statistical power. The significant coefficients in 2020 are suggestive but would not survive a Bonferroni correction across all strategies.

### 5.5 Architectural verdict

Each architecture's 2024 performance can be evaluated against the testable hypothesis from Section 2.

**JPMorgan: confirms.** The modest excess over the S&P (-8.4% versus -6.1%) is consistent with balance-sheet sensitivity, not AI failure. JEPI and JEPQ, observable for the first time in a stress event, behaved within normal parameters.

**BlackRock: confirms in the negative direction.** Correlations among BlackRock-managed products rose less than in 2020 because the shared risk model was not activated by this type of shock. TLT's -11.1% drawdown reflects a structural rates repricing, not a failure of risk management.

**Bridgewater: strongly confirms.** The contrast between -15.7% in 2020 and +0.9% in 2024 is the cleanest architectural differentiation in the paper. Risk parity broke when its diversification assumption broke (2020) and held when that assumption was preserved (2024). This is not luck; it is the architectural prediction performing as specified.

**Two Sigma: confirms.** The factor proxy tracked the market closely (-6.2% versus -6.1%). No factor crowding signal appeared in the regressions. No MTUM-specific spread coefficient emerged as it did in 2020. The absence of the momentum-crowding signature in a non-credit event is consistent with the hypothesis that factor crowding is activated by credit-liquidity stress, not by all regime breaks.

---

## Section 6: Cross-Event Synthesis

### 6.1 The architectural test

The two-event design tests whether four institutional risk architectures fail in the same way or in different ways under stress. The answer is: both, depending on the channel.

In March 2020, all four architectures suffered significant drawdowns. JPMorgan equity fell -42.5%, the BlackRock iShares family tracked or exceeded the S&P 500's -33.9% decline across every product, the Bridgewater risk-parity replicator drew down -15.7%, and the Two Sigma factor proxy lost -30.1%. Average pairwise correlations nearly doubled, from 0.25 pre-event to 0.50 in the event window. Nominally diverse strategies converged, the empirical definition of common-mode failure.

In August 2024, the same architectures produced different outcomes. The S&P 500 fell -6.1%. JPMorgan equity lost -8.4%. The BlackRock products drew down modestly, except TLT (-11.1%), which reflected a structural repricing of global duration rather than liquidity stress. The Two Sigma factor proxy tracked the market almost exactly at -6.2%. And the Bridgewater replicator gained +0.9% over the event window. Average pairwise correlations rose only 19%, from 0.37 to 0.44, and fell below pre-event levels afterward. Strategies maintained their independence.

The contrast between the two events is the paper's central finding. Two numbers summarize it: a 98% correlation increase in 2020 versus a 19% increase in 2024. This is not a generic "regime breaks cause correlated failure" result. The correlation convergence was specific to the credit-liquidity event.

The cross-event scatter visualizes the architectural test directly. Each strategy proxy is plotted by its 2020 drawdown against its 2024 drawdown. Strategies on the 45-degree line fell roughly equally in both events. Strategies far from the line failed asymmetrically. The Bridgewater replicator's position (-15.7 percent, +0.9 percent) places it in the architectural-differentiation quadrant. JPMorgan equity sits close to the line, indicating both events hit it through the same balance-sheet channel.

![**Figure 6.** Cross-event architectural test. Each strategy proxy plotted by its COVID 2020 drawdown (x-axis) against its yen carry 2024 drawdown (y-axis). Source: outputs/tables/table1_drawdowns.csv.](outputs/figures/fig5_cross_event_scatter.png){width=85%}

### 6.2 The credit-liquidity mechanism

The event-window regression points to a specific channel. In the 2020 window, three strategies showed significant negative coefficients on the lagged Corwin-Schultz bid-ask spread: AGG (p = 0.006), HYG (p < 0.001), and MTUM (p = 0.005). Wider spreads on day t-1 predicted lower returns on day t, after controlling for market beta and VIX. This pattern is consistent with the Brunnermeier and Pedersen (2009) funding-liquidity spiral operating at daily frequency: margin calls force liquidation, liquidation widens spreads, wider spreads trigger further margin calls.

In the 2024 window, no strategy showed a significant negative spread coefficient. The test could have failed: if the same regression signature had appeared during the yen carry unwind, the credit-liquidity explanation would be indistinguishable from a generic stress explanation. It did not fail. The two significant coefficients in 2024 (HYG and the Bridgewater replicator) were positive, consistent with mean reversion after a transient volatility spike rather than forced selling into frozen markets.

The selection of AGG, HYG, and MTUM in 2020 is not arbitrary. It traces the credit-liquidity channel through three distinct instrument classes. AGG holds investment-grade bonds and Treasuries, the instruments that institutional investors sell first when they need cash, because they are normally the most liquid. When that liquidity evaporates, selling becomes self-reinforcing. HYG holds high-yield credit, the most stressed segment of the bond market in March 2020 when the ICE BofA High Yield OAS exceeded 1,100 basis points. MTUM holds recent equity winners, crowded systematic positions that are unwound first by the most leveraged participants when funding costs spike. Each instrument sits at a different point in the financial system, but all three were connected by the same funding channel.

### 6.3 Concentration and systemic risk

The findings bear on the regulatory debate about systemic concentration in AI-driven and quantitative finance. The Financial Stability Oversight Council (2014) raised concerns that "financial firms may rely too heavily on the same outside risk models." The UK Financial Conduct Authority (2021) warned that the failure of a large portfolio and risk system such as BlackRock's Aladdin "could cause serious consumer harm" or "damage market integrity." These concerns implicitly assume that architectural diversity provides systemic resilience, that if different firms use different models, the system is safer.

The 2020 data complicate this assumption. JPMorgan's execution-layer AI, BlackRock's factor-covariance risk models, Bridgewater's risk parity, and Two Sigma's multi-factor systematic strategies are architecturally distinct. They make different bets about which correlations will hold under stress. Yet in March 2020, they converged. The mechanism was not that they shared a model; it was that they shared exposure to U.S. credit liquidity. Architectural diversity did not prevent correlated failure because the common-mode channel operated below the level of model architecture, at the level of funding markets.

This is consistent with the theoretical framework of Adrian and Brunnermeier (2016), who measure systemic contribution via CoVaR, the value-at-risk of the financial system conditional on one institution being in distress. Their insight is that systemic risk arises not from individual institution failure but from the correlation of failures across institutions. The empirical contribution of this paper is to show that this correlation is channel-specific: it was activated by credit-liquidity stress in 2020 but not by rates-driven stress in 2024. Acharya, Pedersen, Philippon, and Richardson (2017) formalize a related point through the concept of systemic expected shortfall (SES), measuring each institution's propensity to be undercapitalized precisely when the system as a whole is undercapitalized.

The practical implication is that stress tests and systemic risk assessments should focus less on whether institutions use different models and more on whether they share exposure to the same funding channels. Architectural diversity is a weak defense when funding liquidity is the common mode of failure.

### 6.4 What the paper does not show

Three limitations constrain the inference.

First, two events cannot prove a causal mechanism. The results are consistent with the credit-liquidity hypothesis, but alternative explanations survive. The 2020 event lasted 23 trading days versus 8 for 2024. The S&P 500 drawdown was -33.9% versus -6.1%. The geographic scope was global versus Asia-concentrated. Duration, magnitude, and geographic scope are all confounded with the credit-liquidity distinction. Disentangling these factors requires additional events; the March 2023 regional bank crisis (SVB, Signature, First Republic) is a candidate for future work, as it produced U.S. credit stress without a global pandemic.

Second, the Bridgewater and Two Sigma proxies introduce magnitude uncertainty. The Bridgewater replicator caps leverage at 1.5x and cannot replicate the firm's regime overlay. The Two Sigma proxy excludes alpha, leverage, and dynamic hedging. Both proxies capture the directional risk profile (a correct sign is more informative than a precise magnitude), but actual fund returns could differ materially from what we measure.

Third, the event-window regressions operate on 22 to 42 observations per window. The significant p-values in 2020 (0.006, <0.001, 0.005) are strong for single-strategy tests but would not survive a Bonferroni correction for multiple comparisons across all strategies in the panel. The results are suggestive, not definitive.

### 6.5 Implications for AI in finance

The four architectures examined here represent different answers to the question of where AI and quantitative methods sit in the investment process. JPMorgan uses AI at the execution layer. BlackRock uses quantitative risk models for portfolio construction and oversight. Bridgewater uses systematic rules for regime identification and risk allocation. Two Sigma uses statistical models for signal generation and trade selection. These are architecturally distinct.

The findings suggest that the systemic risk of AI in finance depends less on the architecture of individual firms' AI systems and more on their shared exposure to funding and liquidity channels. A sophisticated reinforcement-learning execution system and a simple factor-covariance risk model can fail simultaneously, not because they share code, training data, or model architecture, but because they share exposure to the same credit markets. This is a specific, falsifiable claim: future credit-liquidity events should produce correlated failure across architecturally diverse strategies, while future rates-driven or geographically concentrated events should not, unless they activate U.S. credit markets.

The Financial Stability Board's work on AI and machine learning in financial services (FSB, 2017) identifies model risk, data dependency, and concentration among third-party providers as key systemic concerns. The evidence here suggests an additional concern: even when AI systems are fully independent, they can fail together because their portfolios, not their models, share common-mode exposure. Supervising the model is necessary. Supervising the funding channel may be more important.

---

## Section 7: Limitations

### 7.1 Sample size

This study examines two events. Two events cannot constitute a statistical sample, and any inference drawn from two observations is necessarily provisional. The results describe what happened during two specific regime breaks. They cannot distinguish the credit-liquidity mechanism from coincidence with the rigor that a larger sample would permit.

The two-event design is intentional: each event activates a different stress channel, enabling a within-study falsification test that a single-event study cannot perform. But the design imposes hard bounds on generalization. A third event with severe market dislocation but no U.S. credit stress would strengthen the inference. The March 2023 regional bank crisis, the October 2023 Treasury selloff, and the April 2025 tariff-driven equity correction are candidates for future out-of-sample tests.

### 7.2 Proxy limitations

Two of the four architectures, Bridgewater and Two Sigma, are observed through constructed proxies rather than actual fund returns.

The Bridgewater risk-parity replicator uses five ETFs (IVV, TLT, TIP, DBC, GLD) weighted by inverse trailing volatility, vol-targeted to 10% annualized, and leverage-capped at 1.5x. It differs from All Weather in three known ways: lower leverage (1.5x versus a reported 3-4x on the bond sleeve), ETF-based construction (versus futures, which have different financing costs), and no regime overlay. The replicator's Pearson correlation with four publicly disclosed All Weather return figures is r = 0.75. It captures the correct sign of returns, negative when All Weather lost money, positive when it gained, but understates magnitude. The -15.7% peak-to-trough drawdown in 2020 is therefore a conservative estimate of the actual fund's stress.

The Two Sigma factor proxy (MTUM, VLUE, QUAL, USMV, DBMF) captures the exposure profile of a diversified multi-factor systematic shop. It does not capture the firm's specific alpha generation, leverage, or dynamic hedging. Returns should be interpreted as the performance of passively held systematic factor exposure, a lower bound on what a sophisticated systematic fund would achieve, not a replication of its returns.

JPMorgan and BlackRock are directly observable through public equities and ETFs, but these instruments measure product performance, not internal risk analytics. JPM equity reflects bank balance-sheet dynamics. The iShares family reflects Aladdin's portfolio construction, not Aladdin's recommendations to external clients.

### 7.3 Statistical power

The event-window regressions operate on 22 to 42 observations per window. With three regressors and Newey-West HAC standard errors (5 lags), these are small-sample regressions. The significant coefficients in the 2020 window, AGG (p = 0.006), HYG (p < 0.001), and MTUM (p = 0.005), are individually strong but would not survive a Bonferroni correction for multiple comparisons across the full panel of strategies.

The Corwin-Schultz (2012) spread estimator, while established in the market microstructure literature, is less precise than intraday TAQ-based measures. It relies on daily high and low prices, which may not capture intraday liquidity dynamics during fast-moving markets. Negative or implausible estimates are set to missing, which reduces sample size further in volatile periods, precisely when the spread signal is most informative.

The full-sample liquidity regression (Analysis 4a) has more power but cannot distinguish event-specific mechanisms. The event-window regression (Analysis 4b) can distinguish mechanisms but lacks power. This trade-off is inherent in event study designs with short event windows.

### 7.4 Exploratory rather than confirmatory design

The hypotheses in Section 2 were developed iteratively as the empirical patterns became visible during pipeline construction, not pre-registered before data collection. The architectural taxonomy (execution-layer, risk-model, risk-parity, signal-layer) was specified in advance, but the specific stress-behavior predictions for each architecture were refined after observing the 2020 and 2024 data. This means the paper documents and rationalizes patterns rather than testing pre-committed predictions. The 2024 yen carry event provides a partial check on this concern: because the credit-liquidity regression signature was specified from the 2020 analysis and then found absent in 2024, the 2024 result functions as a quasi-out-of-sample test even though it was not formally pre-registered. A genuinely confirmatory version of this study would pre-register the hypotheses and test them on events that occur after registration. This is the appropriate next step for the research program.

### 7.5 Identification limitations

This paper documents empirical regularities across two regime breaks. It does not establish causal identification. The event-window regressions show that lagged bid-ask spreads predict next-day returns during the 2020 credit event, but the regression specification cannot rule out reverse causality (falling prices widen spreads, which then predict further price declines) or omitted-variable bias (an unobserved third factor, such as dealer inventory capacity, drives both spreads and returns simultaneously). Establishing causation would require instrumental variables for funding liquidity that are plausibly exogenous to contemporaneous asset returns, a standard that daily-frequency public data cannot meet.

The simultaneous-equation concern is particularly relevant. In the Brunnermeier and Pedersen (2009) model, market liquidity and funding liquidity are jointly determined. The lagged spread partially addresses this by using day t-1 information to predict day t returns, but one-day lags may be insufficient if the feedback loop operates at intraday frequency. Intraday or transaction-level data on institutional positioning, margin calls, and dealer inventory would be needed to disentangle the direction of causation.

The proxy-based design introduces a further identification challenge. The Bridgewater replicator and Two Sigma factor proxy measure the returns of publicly available ETFs, not the actual institutional portfolios. A significant regression coefficient on MTUM tells us that momentum-factor ETF returns were predictable from spreads; it does not prove that Two Sigma's internal positions experienced the same dynamic. The inference from proxy to institution requires an assumption of directional alignment that is supported by construction (Section 3.4) but not verified against actual fund returns.

### 7.6 Robustness considerations

Several robustness checks would strengthen the findings but lie beyond the scope of this two-event study.

First, placebo event windows: running the same regression specification on randomly selected 22-day windows during non-crisis periods would establish a baseline distribution of spread coefficients under the null hypothesis of no liquidity-driven forced selling. If the 2020 coefficients fall in the extreme tail of the placebo distribution, the result is more convincing than a simple p-value comparison.

Second, subsample analysis: splitting the 2020 event window at the March 15 Fed emergency rate cut would test whether the spread-return relationship was stronger before or after the intervention. If the coefficient weakens after the Fed acted, it supports the interpretation that the channel was credit-liquidity stress rather than generic panic.

Third, alternative spread estimators: replacing Corwin-Schultz with the Abdi and Ranaldo (2017) close-high-low-close estimator or the Roll (1984) implied spread would test whether the results are robust to estimator choice.

Fourth, bootstrap inference: block-bootstrapping the event-window regressions with replacement would provide confidence intervals that do not rely on the Newey-West asymptotic approximation, which may be unreliable with 22-42 observations.

Fifth, multiple-testing corrections: applying Benjamini-Hochberg false discovery rate control across all strategy-event pairs would address the concern that the significant 2020 coefficients could be false positives from multiple comparisons.

### 7.7 Falsification scope

The credit-liquidity hypothesis survives a single falsification test: the 2024 yen carry unwind did not produce the regression signature observed in 2020. The non-result is consistent with the hypothesis but does not prove it. Alternative explanations, including event duration, shock magnitude, and geographic scope, remain viable.

A stronger falsification design would include at least three types of events: a U.S. credit-liquidity crisis (2020), a non-credit regime break (2024), and a third event that mixes elements of both. The March 2023 SVB crisis is a candidate: it originated in U.S. interest rate risk, triggered bank runs, and briefly stressed credit markets, but the contagion was contained before it reached the broad credit-liquidity channel. If the regression signature appeared during SVB (when credit stress was present but contained), it would sharpen the boundary conditions of the hypothesis. If it did not, it would support a threshold interpretation: the channel activates only when credit stress exceeds some severity threshold. Neither outcome is testable with the data in this paper.

---

## Section 8: Robustness: Endogenous Identification of Event Windows

A natural objection to the event-study design of this paper is that the two stress windows are selected by the researcher, raising the concern that they were chosen to fit the hypothesis. To address this, I test whether the windows can be recovered by an unsupervised model given no information about the event dates or the argument of the paper. I fit a Gaussian Hidden Markov Model to daily log returns over 2018 to 2024 under four specifications: two and three latent states, each estimated on returns alone and on returns augmented with twenty-one-day realized volatility, standardized. The crisis regime is identified as the highest-variance state, confirmed as the lowest-mean state where applicable, with states sorted by variance to address label-switching. As an independent check, I estimate a GARCH(1,1) with Student-t innovations and compare conditional volatility within each window to its full-sample level. Full per-regime statistics, transition matrices, and reproducible code are provided in the repository.

For the March 2020 window, the model classifies the large majority of trading days into the crisis regime under every specification, and GARCH conditional volatility reaches several times its normal level (Table 8; Figure 7). The March 2020 window is therefore robustly recovered by a model blind to the event, and its selection is not an artifact of researcher discretion.

**Table 8.** Endogenous regime classification of event windows. Crisis share is the percentage of trading days within each event window assigned to the highest-variance crisis regime by a Gaussian Hidden Markov Model blind to the event dates. The four specifications are two and three latent states, each estimated on returns alone and on returns plus twenty-one-day realized volatility. GARCH volatility is the average within-window conditional volatility expressed as a multiple of the full-sample level.

| Event | Instrument | Crisis share 2-state (returns) | Crisis share 2-state (returns+vol) | Crisis share 3-state (returns) | Crisis share 3-state (returns+vol) | GARCH volatility (multiple of normal) |
|------------|-------------|---:|---:|---:|---:|---:|
| March 2020  | S&P 500     | 96%  | 96%  | 96%  | 90% | 3.5x |
| August 2024 | S&P 500     | 44%  | 75%  | 0%   | 0%  | 1.3x |
| August 2024 | USD/JPY     | 12%  | 100% | 25%  | 100% | 1.7x |
| August 2024 | Nikkei 225  | 100% | 100% | 100% | 60% | 2.6x |

Source: robustness/results.md and robustness/results_carry.md.

The August 2024 window behaves differently on US equities, where only a minority to moderate share of days is classified as crisis on the S&P 500 and GARCH volatility is modestly elevated. Rather than treating this as a weak result, I interpret it as informative about the nature of the event. The August 2024 episode was a yen carry-trade unwind that transmitted most violently through foreign exchange and Japanese equities rather than US equities, where it appeared as a single-session shock on the fifth of August that largely reversed within days. Re-estimating the identical model on the instruments at the center of the unwind confirms this. On the Nikkei 225, the window is classified as crisis under every specification. On USD/JPY, the volatility-aware specifications classify the entire window as crisis, while the returns-only specifications are weaker, consistent with foreign-exchange stress that is sustained rather than concentrated in a single record move; a returns-only model reserves the crisis state for the most extreme individual days and recovers the window only once volatility persistence is modeled explicitly.

Both event windows are thus recovered by an unsupervised model when applied to the markets through which each crisis actually propagated. The contrast is itself a result. March 2020 was a broad systemic liquidity crisis visible across asset classes, whereas August 2024 was a concentrated leverage unwind localized to foreign exchange and Japanese equities. This structural difference is precisely what makes a comparison of institutional risk responses across the two episodes informative, since the events stress different components of a risk architecture.

Two limitations bear noting. On the USD/JPY returns-and-volatility three-state model, the highest-variance state was not the single lowest-mean state, as expected for an exchange rate where extreme moves occur in both directions; that classification is reported as suggestive rather than confirmatory. Settings were held identical across all instruments for comparability, and a small number of the noisier fits did not reach strict convergence within the fixed iteration budget; the central finding holds across all four specifications and is independently corroborated by the GARCH estimates.

---

## Section 9: Conclusion

Four institutional risk architectures, execution-layer AI, factor-covariance risk modelling, regime-aware risk parity, and multi-factor systematic strategies, converged during the March 2020 COVID drawdown and diverged during the August 2024 yen carry unwind. Average pairwise correlations nearly doubled in 2020 (from 0.25 to 0.50) and rose only modestly in 2024 (from 0.37 to 0.44). The event-window regression identifies the specific channel: in 2020, wider bid-ask spreads predicted lower next-day returns for AGG, HYG, and MTUM, a pattern consistent with forced selling into illiquid credit markets. In 2024, no strategy showed the same pattern. Architectural diversity did not prevent correlated failure. The evidence is consistent with the credit-liquidity channel operating below the level of model architecture, at the level of funding markets.

The result is bounded by its evidence. Two events cannot prove a causal mechanism. The Bridgewater and Two Sigma proxies introduce magnitude uncertainty. The event-window regressions, with 22 to 42 observations per window, have limited statistical power. The significant coefficients would not survive Bonferroni correction across the full strategy panel. These are empirical regularities from two well-documented regime breaks, not a general law. Future research should test the credit-liquidity hypothesis on out-of-sample events, including the March 2023 regional bank crisis and subsequent dislocations, using the reproducible pipeline and falsifiable specification provided with this paper. A proper test of causal identification, using instrumental variables for funding liquidity and intraday or transaction-level data on institutional positioning, lies beyond the scope of this working paper but is the natural next step for advancing the research program.

The broader point is simple. The systemic risk of AI and quantitative strategies in finance may depend less on whether firms use the same models than on whether their portfolios share exposure to the same funding channels. The evidence in this paper is consistent with this reading but does not establish it causally. Supervising model architecture remains relevant. Supervising the funding channels that connect architecturally diverse portfolios is also worth attention. Which matters more for financial stability is an open empirical question that this paper does not resolve.

---

## Acknowledgments

All data come from public sources (Yahoo Finance, FRED, SEC EDGAR). All computations are reproducible from the public GitHub repository at https://github.com/ArnavG-ProGrammer/regime-breaks. The methodology benefited from extensive iterative review during development. Any remaining errors are my own.

## References

### Academic articles

Acharya, V. V., Pedersen, L. H., Philippon, T., & Richardson, M. (2017). Measuring systemic risk. *Review of Financial Studies*, 30(1), 2-47. https://doi.org/10.1093/rfs/hhw088

Asness, C. S., Frazzini, A., & Pedersen, L. H. (2012). Leverage aversion and risk parity. *Financial Analysts Journal*, 68(1), 47-59. https://doi.org/10.2469/faj.v68.n1.1

Adrian, T., & Brunnermeier, M. K. (2016). CoVaR. *American Economic Review*, 106(7), 1705-1741. https://doi.org/10.1257/aer.20120555

Brunnermeier, M. K., & Pedersen, L. H. (2009). Market liquidity and funding liquidity. *Review of Financial Studies*, 22(6), 2201-2238. https://doi.org/10.1093/rfs/hhn098

Corwin, S. A., & Schultz, P. (2012). A simple way to estimate bid-ask spreads from daily high and low prices. *The Journal of Finance*, 67(2), 719-760. https://doi.org/10.1111/j.1540-6261.2012.01729.x

MacKinlay, A. C. (1997). Event studies in economics and finance. *Journal of Economic Literature*, 35(1), 13-39.

Newey, W. K., & West, K. D. (1987). A simple, positive semi-definite, heteroskedasticity and autocorrelation consistent covariance matrix. *Econometrica*, 55(3), 703-708. https://doi.org/10.2307/1913610

### Books

Wigglesworth, R. (2021). *Trillions: How a Band of Wall Street Renegades Invented the Index Fund and Changed Finance Forever*. Penguin Business.

### Regulatory and central bank publications

Bank for International Settlements. (2024). The market turbulence and carry trade unwind of August 2024. *BIS Bulletin No 90*. https://www.bis.org/publ/bisbull90.pdf

Bridgewater Associates. (2012). The All Weather story: How Bridgewater Associates created the All Weather investment strategy. Westport, CT: Bridgewater Associates. https://www.bridgewater.com/research-and-insights/the-all-weather-story

Schrimpf, A., Shin, H. S., & Sushko, V. (2020). Leverage and margin spirals in fixed income markets during the Covid-19 crisis. *BIS Bulletin No 2*. Bank for International Settlements. https://www.bis.org/publ/bisbull02.pdf

Mooney, A., & Riding, S. (2021, February 16). BlackRock's Aladdin under scrutiny for crowding risk as assets pass $20tn. *Financial Times*.

Financial Stability Board. (2017). Artificial intelligence and machine learning in financial services: Market developments and financial stability implications. Basel: FSB. https://www.fsb.org/2017/11/artificial-intelligence-and-machine-learning-in-financial-services/

Reuters. (2014, May 16). Exclusive: Regulators scrutinize financial risk-modeling firms. *Reuters*. Based on leaked Financial Stability Oversight Council internal documents during the 2014-2015 review of asset management systemic risk.

### Federal Reserve publications

Duffie, D. (2023). Resilience redux in the US Treasury market. Jackson Hole Economic Policy Symposium. Federal Reserve Bank of Kansas City. https://www.kansascityfed.org/Jackson%20Hole/documents/9726/JH_Paper_Duffie.pdf

Fleming, M., & Ruela, F. (2020, April 17). Treasury market liquidity during the COVID-19 crisis. *Liberty Street Economics*, Federal Reserve Bank of New York. https://libertystreeteconomics.newyorkfed.org/2020/04/treasury-market-liquidity-during-the-covid-19-crisis/

Goldberg, J. (2020, July 17). Dealer inventory constraints during the COVID-19 pandemic: Evidence from the Treasury market and broader implications. *FEDS Notes*, Board of Governors of the Federal Reserve System. https://www.federalreserve.gov/econres/notes/feds-notes/dealer-inventory-constraints-during-covid-19-pandemic-evidence-from-treasury-market-broader-implications-20200717.htm

### Corporate filings and disclosures

BlackRock, Inc. (2026). Form 10-K, fiscal year 2025. U.S. Securities and Exchange Commission. CIK 0002012383. https://www.sec.gov/Archives/edgar/data/0002012383/000119312526071966/blk-20251231.htm

JPMorgan Chase & Co. (2025). 2024 Annual Report. JPMorgan Chase Investor Relations. https://www.jpmorganchase.com/content/dam/jpmc/jpmorgan-chase-and-co/investor-relations/documents/annualreport-2024.pdf

### Journalism

Financial press (April 2020). Reporting on Bridgewater Pure Alpha and All Weather Q1 2020 returns appeared across the Financial Times, Reuters, and Bloomberg in early April 2020. The author has not verified specific article URLs to primary source.

Financial press (January 2023). Reporting on Bridgewater Pure Alpha and All Weather full-year 2022 returns appeared in Bloomberg and the Financial Times in early January 2023. The author has not verified specific article URLs to primary source.

Son, H. (2017, February 28). JPMorgan marshals an army of developers to automate high finance. *Bloomberg*. https://www.bloomberg.com/news/articles/2017-02-28/jpmorgan-marshals-an-army-of-developers-to-automate-high-finance

### Data sources

Federal Reserve Economic Data (FRED). Federal Reserve Bank of St. Louis. https://fred.stlouisfed.org/

Yahoo Finance. Via `yfinance` Python package (version 1.3.0). https://pypi.org/project/yfinance/

---

## Appendix A: Verification of Source Material

This appendix records the verification status of factual claims and source citations in the paper. It documents what has been verified to primary sources, what has been verified via secondary or press sources, and what remains as press-attributed estimates pending primary-source confirmation.

### Verified to primary source

| Claim | Source verified |
|---|---|
| BlackRock total AUM $14.0 trillion at 31 December 2025 | SEC EDGAR. BlackRock 10-K FY2025, Item 1 Business Overview. Filed February 2026. |
| Acharya, Pedersen, Philippon, Richardson (2017) SES citation | *Review of Financial Studies*, 30(1), 2-47. DOI: 10.1093/rfs/hhw088. |
| ICE BofA US High Yield OAS exceeded 1,000 basis points in late March 2020 | FRED series BAMLH0A0HYM2, accessed via Federal Reserve Economic Data API. Peak observed near 1,100 bps on March 23, 2020. |
| ICE BofA US High Yield OAS reached 393 basis points on August 5, 2024 | FRED series BAMLH0A0HYM2, accessed via Federal Reserve Economic Data API. |
| FSB (2017) Artificial Intelligence and Machine Learning in Financial Services | https://www.fsb.org/2017/11/artificial-intelligence-and-machine-learning-in-financial-services/ |
| VIX intraday high 65.73 on August 5, 2024 | Yahoo Finance ^VIX historical price data. Accessed May 18, 2026. |
| Schrimpf, Shin, Sushko (2020) BIS Bulletin No 2 | https://www.bis.org/publ/bisbull02.pdf. Published April 2, 2020. |
| Asness, Frazzini, Pedersen (2012) Leverage Aversion and Risk Parity | *Financial Analysts Journal*, 68(1), 47-59. DOI: 10.2469/faj.v68.n1.1. |
| Bridgewater Associates (2012) The All Weather Story | https://www.bridgewater.com/research-and-insights/the-all-weather-story |
| JPMorgan Chase 2024 Annual Report | https://www.jpmorganchase.com/content/dam/jpmc/jpmorgan-chase-and-co/investor-relations/documents/annualreport-2024.pdf |

### Verified to secondary or press source

| Claim | Source |
|---|---|
| FCA (January 2021) statement on Aladdin systemic risk | The exact phrases "could cause serious consumer harm" and "damage market integrity" were reported in the Financial Times in February 2021 (Mooney & Riding, 2021). The original FCA primary publication has not been independently located by the author. The FT report is treated as the verifiable source. |
| FSOC (2014) concern that "financial firms may rely too heavily on the same outside risk models" | This phrase was reported by Reuters (May 2014) based on leaked FSOC internal documents during the FSOC's 2014-2015 review of asset management systemic risk. The phrase does not appear in the published FSOC 2014 Annual Report. The Reuters report is treated as the verifiable source. |
| BlackRock Aladdin platform reach approximately $25 trillion | This figure is reported by BlackRock in investor communications and December 2025 disclosures but is not disclosed as a specific dollar figure in the 10-K body. Cited per BlackRock public statements. |

### Press-attributed estimates (not verified to primary source)

| Claim | Status |
|---|---|
| Bridgewater All Weather Q1 2020 loss approximately -14% | Widely reported in financial press (FT, Reuters, Bloomberg) in April 2020. Specific article URLs not verified by the author within the constraints of this working paper. Treated as press estimate. |
| Bridgewater All Weather FY 2022 loss approximately -9.4% | Widely reported in financial press in January 2023. Specific article URLs not verified by the author within the constraints of this working paper. Treated as press estimate. |
| Two Sigma 2024 AUM approximately $55-60 billion | Reported in various trade press over 2024-2025. Exact figure varies by source and sub-strategy inclusion. Treated as press estimate. |

### Note on verification standards

This paper is a working paper produced by an independent author without institutional access to Bloomberg Terminal, Financial Times subscription, or other paywalled financial data services. All public-source claims have been verified to primary sources where possible. Where primary sources require paid access, the paper relies on press estimates and clearly labels them as such. A peer-reviewed revision would require resolving these press estimates to primary sources via institutional access.

---

## Appendix B: Reproducibility

The complete data pipeline and analysis code for this paper are publicly available at: https://github.com/ArnavG-ProGrammer/regime-breaks

The repository contains:

- `data_pipeline.py`: Downloads all price data (Yahoo Finance via yfinance) and macroeconomic series (FRED API), constructs the Bridgewater risk-parity replicator and Two Sigma factor proxy, computes Corwin-Schultz spread estimates, and caches all raw files to disk with SHA-256 hashes.
- `analysis.py`: Runs all five analyses (drawdown, correlation, volatility breach, full-sample liquidity regression, event-window liquidity regression) and exports tables and figures to `outputs/`.
- `requirements.txt`: Pins all Python package versions (pandas, numpy, statsmodels, matplotlib, scipy, pyarrow, yfinance 1.3.0, fredapi 0.5.2).
- `data/manifest.json`: Generated on each pipeline run. Records the UTC timestamp of the run, Python version, package versions, SHA-256 hash of every raw file downloaded, and the FRED API series identifiers fetched.

The analyses are deterministic given the input data. No random seeds are used in the pipeline because no stochastic operations (bootstrap, simulation, random sampling) are performed. The Corwin-Schultz spread estimator, regression coefficients, correlation matrices, and drawdown calculations are all closed-form functions of the input prices and macro series.

Anyone with a Python 3.12+ environment and a free FRED API key (available at https://fred.stlouisfed.org/docs/api/api_key.html) can reproduce the exact dataset and all derived analyses by running:

1. `git clone https://github.com/ArnavG-ProGrammer/regime-breaks.git`
2. `cd regime-breaks`
3. `pip install -r requirements.txt`
4. `export FRED_API_KEY=your_key_here`
5. `python data_pipeline.py` (downloads data, takes 3-5 minutes)
6. `python analysis.py` (generates all tables and figures, takes approximately 30 seconds)

Outputs land in `outputs/tables/` (CSV and JSON) and `outputs/figures/` (PNG).

The manifest.json file records precise package versions and the FRED data-fetch date. Since FRED data are not retroactively revised for the series used in this paper, fetches on any subsequent date produce identical numerical values for the dates in the event windows.

---

## Appendix C: Data Sources

**Table 7.** Data sources by strategy proxy. All series are publicly available. Frequency is daily unless otherwise noted. Date range covers both event windows plus 90 trading days before and after each.

| Proxy / Series | Source | Ticker / Series ID | Frequency | Coverage |
|----------------|--------|--------------------|-----------|----------|
| JPMorgan Chase equity | Yahoo Finance | JPM | daily | 2019-10-01 to 2024-12-13 |
| JEPI ETF | Yahoo Finance | JEPI | daily | 2020-05-21 onward |
| JEPQ ETF | Yahoo Finance | JEPQ | daily | 2022-05-04 onward |
| BlackRock equity | Yahoo Finance | BLK | daily | 2019-10-01 to 2024-12-13 |
| iShares S&P 500 | Yahoo Finance | IVV | daily | 2019-10-01 to 2024-12-13 |
| iShares Aggregate Bond | Yahoo Finance | AGG | daily | 2019-10-01 to 2024-12-13 |
| iShares 20+ Year Treasury | Yahoo Finance | TLT | daily | 2019-10-01 to 2024-12-13 |
| iShares High Yield Corporate | Yahoo Finance | HYG | daily | 2019-10-01 to 2024-12-13 |
| iShares Emerging Markets | Yahoo Finance | EEM | daily | 2019-10-01 to 2024-12-13 |
| iShares TIPS | Yahoo Finance | TIP | daily | 2019-10-01 to 2024-12-13 |
| Invesco DB Commodity | Yahoo Finance | DBC | daily | 2019-10-01 to 2024-12-13 |
| SPDR Gold | Yahoo Finance | GLD | daily | 2019-10-01 to 2024-12-13 |
| iShares MSCI Momentum | Yahoo Finance | MTUM | daily | 2019-10-01 to 2024-12-13 |
| iShares MSCI Value | Yahoo Finance | VLUE | daily | 2019-10-01 to 2024-12-13 |
| iShares MSCI Quality | Yahoo Finance | QUAL | daily | 2019-10-01 to 2024-12-13 |
| iShares MSCI Min Vol | Yahoo Finance | USMV | daily | 2019-10-01 to 2024-12-13 |
| iMGP DBi Managed Futures | Yahoo Finance | DBMF | daily | 2019-10-01 to 2024-12-13 |
| Bridgewater replicator | Constructed (IVV, TLT, TIP, DBC, GLD) | see Section 3.4 | daily | 2019-10-01 to 2024-12-13 |
| Two Sigma factor proxy | Equal-weight basket (MTUM, VLUE, QUAL, USMV, DBMF) | see Section 3.4 | daily | 2019-10-01 to 2024-12-13 |
| Nikkei 225 | Yahoo Finance | ^N225 | daily | 2024-04-01 to 2024-12-13 |
| VIX | Yahoo Finance + FRED | ^VIX, VIXCLS | daily | 2019-10-01 to 2024-12-13 |
| Fed Funds Rate | FRED | DFF | daily | 2019-10-01 to 2024-12-13 |
| 10-Year Treasury | FRED | DGS10 | daily | 2019-10-01 to 2024-12-13 |
| 2-Year Treasury | FRED | DGS2 | daily | 2019-10-01 to 2024-12-13 |
| ICE BofA HY OAS | FRED | BAMLH0A0HYM2 | daily | 2019-10-01 to 2024-12-13 |
| ICE BofA BBB OAS | FRED | BAMLC0A4CBBB | daily | 2019-10-01 to 2024-12-13 |
| USD/JPY | FRED + Yahoo | DEXJPUS, JPY=X | daily | 2019-10-01 to 2024-12-13 |

All raw downloads cached locally and hashed with SHA-256. See `data/manifest.json` in the repository.
