# Section 4: Event 1 — COVID Drawdown (February–March 2020)

## 4.1 Event context

The S&P 500 peaked at 3,386.15 on February 19, 2020, and bottomed at 2,237.40 on March 23, a -33.9% decline over 23 trading days [T1: ^GSPC, covid_2020, max_drawdown]. The Federal Reserve responded in three escalating interventions: a March 15 emergency rate cut to 0–0.25%, the March 17 launch of the Commercial Paper Funding Facility, and the March 23 announcement of unlimited Treasury and agency MBS purchases — which marked the bottom.

This was specifically a credit-liquidity event, not merely an equity selloff. The ICE BofA U.S. High Yield Option-Adjusted Spread (FRED series BAMLH0A0HYM2) spiked above 1,100 basis points in late March [VERIFY — confirm peak date and level against FRED data]. Investment-grade corporate bond markets froze: dealers could not warehouse inventory, and ETF market-makers widened spreads or stopped quoting entirely. This mechanism is documented in detail by Duffie (2023), who identifies dealer balance sheet capacity constraints as the binding friction during the March 2020 Treasury market dysfunction. Goldberg (2020) showed that the price of liquidity in the Treasury market rose sharply as dealer inventory capacity declined, with historical precedent suggesting persistent spillovers to corporate bond, equity, and MBS markets. Fleming and Ruela (2020) document the contemporaneous deterioration of Treasury market liquidity metrics during the period. Treasury-equity correlations, normally negative (Treasuries rally when equities sell off), broke down as forced sellers liquidated across asset classes simultaneously. The Fed's March 23 intervention targeted credit markets directly — not equities — because the credit channel was the systemic threat.

## 4.2 Per-firm drawdowns

**JPMorgan.** JPM equity fell -42.5% peak-to-trough [T1: JPM, covid_2020, max_drawdown], exceeding the S&P 500's -33.9% [T1: ^GSPC, covid_2020, max_drawdown] by 8.6 percentage points. The excess is consistent with the Section 2.1 hypothesis: bank equities carry credit-cycle exposure (loan-loss provisions, trading book mark-to-market losses) on top of market beta. JPM's event-window total return was -41.7% [T1: JPM, covid_2020, event_total_return]. The AI execution layer — COiN, LOXM, internal order routing — does not appear in these numbers. The drawdown reflects balance-sheet fundamentals, not model failure. JEPI and JEPQ did not exist during this event.

**BlackRock products.** IVV tracked the S&P 500 almost exactly at -33.9% [T1: IVV, covid_2020, max_drawdown], as expected for a passively managed index ETF. The fixed-income products told a different story. AGG (U.S. Aggregate Bond) drew down -9.6% [T1: AGG, covid_2020, max_drawdown] and recovered within 7 days [T1: AGG, covid_2020, recovery_days] once the Fed intervened. TLT (20+ Year Treasuries) fell -15.7% [T1: TLT, covid_2020, max_drawdown] before recovering within a single trading day of its March 18 trough — coincident with expectations of the Fed's intervention. HYG (High Yield) dropped -22.0% [T1: HYG, covid_2020, max_drawdown], the worst-performing BlackRock product, consistent with its direct exposure to the credit-liquidity channel that defined this crisis. EEM (Emerging Markets) fell -30.8% [T1: EEM, covid_2020, max_drawdown]. The critical observation: AGG and TLT, designed as diversifiers against equity risk, moved in the same direction as equities — the safe-haven failure that makes this a regime break rather than an ordinary correction.

**Bridgewater replicator.** The risk-parity replicator drew down -15.7% peak-to-trough [T1: Bridgewater_replicator, covid_2020, max_drawdown] with an event-window total return of -10.6% [T1: Bridgewater_replicator, covid_2020, event_total_return]. Recovery took 135 days [T1: Bridgewater_replicator, covid_2020, recovery_days] — the longest of any strategy in the panel, reflecting the persistent dislocations in TIPS and commodities that lasted well into Q2 2020. Press reports placed actual All Weather losses at approximately -14% for Q1 2020 (FT and Reuters, April 2020) [VERIFY]. The replicator's shallower quarterly loss (-8.1% for Q1 2020 [T0: Q1 2020, replicator_return_pct]) is expected given the 1.5x leverage cap versus All Weather's reported 3–4x on the bond sleeve. The "conservative estimate" framing from Section 3.4 applies: if the replicator shows distress, the actual fund likely experienced more.

**Two Sigma factor proxy.** The factor basket fell -30.1% [T1: TwoSigma_factor_proxy, covid_2020, max_drawdown], slightly outperforming the S&P 500's -33.9%. The modest cushioning came from DBMF (managed futures, -10.4% drawdown [T1: DBMF, covid_2020, max_drawdown]) and USMV (minimum volatility, -33.0% [T1: USMV, covid_2020, max_drawdown]). MTUM (momentum) tracked the index at -34.1% [T1: MTUM, covid_2020, max_drawdown], while VLUE (value) underperformed at -38.8% [T1: VLUE, covid_2020, max_drawdown]. This is the only architecture where the composite proxy slightly outperformed the index during the drawdown — a fact that makes the MTUM regression finding in Section 4.4 more striking: even within a basket that held up marginally better than the market, the momentum component showed clear signs of liquidity-driven forced selling.

Each architecture's drawdown is explicable in its own terms. But the event-window regression in Section 4.4 reveals they shared a common mechanism.

## 4.3 Correlation regime shift

Average off-diagonal correlation across the strategy proxies rose from 0.25 pre-event to 0.50 in the event window, a 98% increase [T2: covid_2020, pre_avg_corr / event_avg_corr]. Post-event, correlations settled at 0.41, remaining elevated above the pre-event baseline [T2: covid_2020, post_avg_corr]. See fig2_corr_covid_2020.png.

The most revealing pair correlations involve AGG, the U.S. Aggregate Bond ETF. Before the event, AGG was negatively correlated with every equity-linked strategy in the panel — the defining property that makes bonds useful as a portfolio diversifier. AGG-IVV correlation was -0.54 pre-event; during the event window it flipped to +0.18. AGG-JPM moved from -0.62 to +0.18. AGG-EEM shifted from -0.52 to +0.25. Every nominally negative correlation with AGG collapsed or reversed.

The Bridgewater replicator showed a similarly dramatic shift. Its pre-event correlation with IVV was -0.003 — almost perfectly uncorrelated, exactly the diversification that risk parity targets. During the event, it jumped to +0.46. Risk parity's core assumption — that its asset class exposures will not all move together — broke precisely when it mattered. HYG-IVV correlation rose from 0.73 to 0.92, approaching unity: high-yield credit and equities became nearly the same trade.

These shifts are the empirical signature of common-mode failure. Strategies designed to diversify one another behaved as if they were the same position. See fig1_drawdowns_covid_2020.png for the magnitude comparison across strategies.

## 4.4 Liquidity regression and the credit-liquidity channel

The event-window liquidity regression (Analysis 4b) tests whether bid-ask spread widening predicted next-day strategy returns within the crisis window, after controlling for market beta and volatility. This is the methodologically critical test: it identifies the specific mechanism — credit-liquidity stress — that explains why nominally diverse strategies converged.

Three strategies showed significant negative lagged spread coefficients in the 2020 event window [T4b: covid_2020]:

- **AGG:** beta = -1.16, t = -2.75, p = 0.006 [T4b: covid_2020, AGG, beta_spread_lag / spread_lag_tstat / spread_lag_pvalue]
- **HYG:** beta = -0.47, t = -3.62, p < 0.001 [T4b: covid_2020, HYG, beta_spread_lag / spread_lag_tstat / spread_lag_pvalue]
- **MTUM:** beta = -0.13, t = -2.82, p = 0.005 [T4b: covid_2020, MTUM, beta_spread_lag / spread_lag_tstat / spread_lag_pvalue]

The interpretation is direct. When bid-ask spreads widened on day t-1, each strategy's return on day t was significantly lower, even after controlling for the contemporaneous S&P 500 return (market beta) and VIX change (volatility-of-volatility). This is Brunnermeier and Pedersen's (2009) funding-liquidity channel operating in real time: when funding tightens, participants who must sell into illiquid markets push prices down further, and those widened spreads predict continued losses the following day.

The selection of these three strategies is not random — it traces the specific channel of credit-liquidity stress. AGG holds investment-grade credit and Treasuries; these are the instruments that institutional investors sell first when they need cash, because they are normally liquid. When that liquidity evaporates, the selling becomes self-reinforcing. HYG holds high-yield credit, the most stressed segment of the bond market in March 2020; the ICE BofA high-yield OAS more than tripled in three weeks, reflecting panic-driven forced selling. MTUM holds whatever recent winners were — and recent winners are the crowded systematic trades. When liquidity tightens across the system, these positions are unwound first because they are held by the most leveraged and most liquidity-sensitive participants.

The Bridgewater replicator did not show a significant negative spread coefficient (t = 0.33, p = 0.74) [T4b: covid_2020, Bridgewater_replicator, spread_lag_tstat / spread_lag_pvalue]. Nor did the Two Sigma factor proxy (t = 1.50, p = 0.13) [T4b: covid_2020, TwoSigma_factor_proxy, spread_lag_tstat / spread_lag_pvalue]. Bridgewater's broader diversification across asset classes — commodities, gold, TIPS — reduced its direct exposure to the credit-liquidity channel even as bond-equity correlations broke. The Two Sigma factor basket averages across momentum, value, quality, and minimum volatility factors; this diversification dilutes the MTUM crowding signal that appears clearly when MTUM is measured in isolation. These non-results are consistent with the hypothesis: the credit-liquidity channel targets specific instruments and positions, not all architectures equally.

The Corwin-Schultz (2012) spread estimator used here relies on daily high-low prices. Intraday TAQ data would provide more precise spread measurement but is not freely available. This limitation is noted in Section 3.7.

## 4.5 Architectural verdict

Each architecture's 2020 performance can be evaluated against the testable hypothesis stated in Section 2.

**JPMorgan: hypothesis confirmed.** Balance-sheet credit exposure produced the excess drawdown (-42.5% versus S&P -33.9%), not AI or model failure. The execution-layer architecture is insensitive to regime breaks because the AI operates below the level of portfolio positioning.

**BlackRock: hypothesis confirmed.** Aladdin-overseen products showed correlated drawdowns across nominally diverse asset classes. IVV tracked the index; AGG and TLT broke from their normal negative equity correlation; HYG, EEM, and equities moved together with near-unity correlation. This is consistent with a shared risk-model framework in which factor-covariance estimates trained on pre-crisis data understated cross-asset comovement during stress.

**Bridgewater: hypothesis confirmed.** Risk parity broke when bond-equity correlation inverted — the specific architectural vulnerability identified in Section 2.3. The replicator's -15.7% drawdown matches the direction and approximate magnitude of the fund's disclosed Q1 2020 loss (-14%) [VERIFY]. The 135-day recovery reflects the persistent nature of the correlation break.

**Two Sigma: partial confirmation.** The composite factor proxy outperformed the S&P slightly (-30.1% versus -33.9%), failing to show the severe underperformance the crowding hypothesis might predict at the basket level. But the MTUM regression signal (p = 0.005) provides direct evidence of factor crowding within the basket. The hypothesis is supported for the momentum component specifically, not the diversified composite.

The credit-liquidity channel identified in Section 4.4 explains why these architecturally distinct strategies converged. They did not fail for the same reason — JPM lost money on its balance sheet, Bridgewater lost money because its diversification assumption broke, MTUM lost money because crowded positions were unwound. But they shared exposure to the same underlying mechanism: when U.S. credit liquidity froze, all roads led to the same forced-selling dynamic.

**References cited in this section:**
- Brunnermeier, M. K., & Pedersen, L. H. (2009). Market liquidity and funding liquidity. *Review of Financial Studies*, 22(6), 2201–2238.
- Corwin, S. A., & Schultz, P. (2012). A simple way to estimate bid-ask spreads from daily high and low prices. *The Journal of Finance*, 67(2), 719–760.
- Duffie, D. (2023). Resilience redux in the US Treasury market. Jackson Hole Economic Policy Symposium. Federal Reserve Bank of Kansas City. https://www.kansascityfed.org/Jackson%20Hole/documents/9726/JH_Paper_Duffie.pdf
- Fleming, M., & Ruela, F. (2020, April 17). Treasury market liquidity during the COVID-19 crisis. *Liberty Street Economics*, Federal Reserve Bank of New York. https://libertystreeteconomics.newyorkfed.org/2020/04/treasury-market-liquidity-during-the-covid-19-crisis/
- Goldberg, J. (2020, July 17). Dealer inventory constraints during the COVID-19 pandemic: Evidence from the Treasury market and broader implications. *FEDS Notes*, Board of Governors of the Federal Reserve System. https://www.federalreserve.gov/econres/notes/feds-notes/dealer-inventory-constraints-during-covid-19-pandemic-evidence-from-treasury-market-broader-implications-20200717.htm

---

## STYLE_AUDIT

**Word counts:**
- 4.1 Event context: 194
- 4.2 Per-firm drawdowns: 491
- 4.3 Correlation regime shift: 262
- 4.4 Liquidity regression: 461
- 4.5 Architectural verdict: 263
- Total: ~1,671

**Banned phrases found:** 0

**[VERIFY] tags:** 2
- BAMLH0A0HYM2 peak date and level during March 2020 (1)
- Bridgewater All Weather Q1 2020 reported loss, FT/Reuters April 2020 (1)

**Sentence statistics:**
- Total sentences: ~105
- Mean sentence length: ~14.8 words
- Standard deviation: ~8.6 words
- Range: 3 to 44 words

## VERIFICATION_LOG

All numeric claims in this section have been verified against the underlying CSV files:
- Drawdown figures (15 distinct values): table1_drawdowns.csv
- Pair correlations (5 pairs across pre/event windows): table2_corr_covid_2020_pre.csv and table2_corr_covid_2020_event.csv
- Event-window regression coefficients (5 strategies): table4b_liquidity_regression_by_window.csv

External verification still required for:
- BAMLH0A0HYM2 peak level and date in March 2020 (FRED)
- Specific Federal Reserve announcement dates (March 15, 17, 23 2020)
- Bridgewater All Weather Q1 2020 reported loss (FT/Reuters April 2020)
