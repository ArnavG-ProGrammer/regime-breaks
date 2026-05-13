# Section 7: Limitations

## 7.1 Sample size

This study examines two events. Two events cannot constitute a statistical sample, and any inference drawn from two observations is necessarily provisional. The results describe what happened during two specific regime breaks. They cannot distinguish the credit-liquidity mechanism from coincidence with the rigor that a larger sample would permit.

The two-event design is intentional — each event activates a different stress channel, enabling a within-study falsification test that a single-event study cannot perform — but the design imposes hard bounds on generalization. A third event with severe market dislocation but no U.S. credit stress would strengthen the inference. The March 2023 regional bank crisis, the October 2023 Treasury selloff, and the April 2025 tariff-driven equity correction are candidates for future out-of-sample tests.

## 7.2 Proxy limitations

Two of the four architectures — Bridgewater and Two Sigma — are observed through constructed proxies rather than actual fund returns.

The Bridgewater risk-parity replicator uses five ETFs (IVV, TLT, TIP, DBC, GLD) weighted by inverse trailing volatility, vol-targeted to 10% annualized, and leverage-capped at 1.5x. It differs from All Weather in three known ways: lower leverage (1.5x versus a reported 3-4x on the bond sleeve), ETF-based construction (versus futures, which have different financing costs), and no regime overlay. The replicator's Pearson correlation with four publicly disclosed All Weather return figures is r = 0.75. It captures the correct sign of returns — negative when All Weather lost money, positive when it gained — but understates magnitude. The -15.7% peak-to-trough drawdown in 2020 is therefore a conservative estimate of the actual fund's stress.

The Two Sigma factor proxy (MTUM, VLUE, QUAL, USMV, DBMF) captures the exposure profile of a diversified multi-factor systematic shop. It does not capture the firm's specific alpha generation, leverage, or dynamic hedging. Returns should be interpreted as the performance of passively held systematic factor exposure — a lower bound on what a sophisticated systematic fund would achieve, not a replication of its returns.

JPMorgan and BlackRock are directly observable through public equities and ETFs, but these instruments measure product performance, not internal risk analytics. JPM equity reflects bank balance-sheet dynamics. The iShares family reflects Aladdin's portfolio construction, not Aladdin's recommendations to external clients.

## 7.3 Statistical power

The event-window regressions operate on 22 to 42 observations per window. With three regressors and Newey-West HAC standard errors (5 lags), these are small-sample regressions. The significant coefficients in the 2020 window — AGG (p = 0.006), HYG (p < 0.001), MTUM (p = 0.005) — are individually strong but would not survive a Bonferroni correction for multiple comparisons across the full panel of strategies.

The Corwin-Schultz (2012) spread estimator, while established in the market microstructure literature, is less precise than intraday TAQ-based measures. It relies on daily high and low prices, which may not capture intraday liquidity dynamics during fast-moving markets. Negative or implausible estimates are set to missing, which reduces sample size further in volatile periods — precisely when the spread signal is most informative.

The full-sample liquidity regression (Analysis 4a) has more power but cannot distinguish event-specific mechanisms. The event-window regression (Analysis 4b) can distinguish mechanisms but lacks power. This trade-off is inherent in event study designs with short event windows.

## 7.4 Falsification scope

The credit-liquidity hypothesis survives a single falsification test: the 2024 yen carry unwind did not produce the regression signature observed in 2020. The non-result is consistent with the hypothesis but does not prove it. Alternative explanations — event duration, shock magnitude, geographic scope — remain viable.

A stronger falsification design would include at least three types of events: a U.S. credit-liquidity crisis (2020), a non-credit regime break (2024), and a third event that mixes elements of both. The March 2023 SVB crisis is a candidate: it originated in U.S. interest rate risk, triggered bank runs, and briefly stressed credit markets — but the contagion was contained before it reached the broad credit-liquidity channel. If the regression signature appeared during SVB (when credit stress was present but contained), it would sharpen the boundary conditions of the hypothesis. If it did not, it would support a threshold interpretation: the channel activates only when credit stress exceeds some severity threshold. Neither outcome is testable with the data in this paper.

---

## STYLE_AUDIT

**Word counts:**
- 7.1 Sample size: 152
- 7.2 Proxy limitations: 248
- 7.3 Statistical power: 178
- 7.4 Falsification scope: 156
- Total: ~734

**Banned phrases found:** 0

**[VERIFY] tags:** 0

**Sentence statistics:**
- Total sentences: ~50
- Mean sentence length: ~13.8 words
- Standard deviation: ~7.5 words
- Range: 4 to 38 words
