# Findings Memo — Phase 1.6 Empirical Results

## Headline

Average pairwise correlations across the strategy proxies nearly doubled during the March 2020 COVID drawdown — from 0.25 pre-event to 0.50 in the event window [T2: covid_2020, pre_avg_corr / event_avg_corr]. In the August 2024 yen carry unwind, correlations rose modestly from 0.37 to 0.44 [T2: yen_carry_2024, pre_avg_corr / event_avg_corr]. This asymmetry is consistent with common-mode failure driven by U.S. credit liquidity stress, but alternative explanations exist: the 2020 event lasted 23 trading days versus 8 for 2024, and peak drawdowns differed by 5x.

An event-window liquidity regression sharpens the picture. In 2020, the lagged Corwin-Schultz spread coefficient was significantly negative for AGG (t=-2.75, p=0.006), HYG (t=-3.62, p<0.001), and MTUM (t=-2.82, p=0.005) [T4b: covid_2020, AGG/HYG/MTUM]. Wider spreads predicted lower next-day returns — the signature of liquidity-driven selling. In 2024, no strategy showed a significant negative spread coefficient [T4b: yen_carry_2024]. The two significant coefficients (HYG, Bridgewater replicator) were positive, suggesting a different mechanism. The credit-liquidity hypothesis survives this test but cannot be confirmed with two events alone.

## Proxy validation

The Bridgewater risk-parity replicator was validated against two publicly disclosed All Weather return figures [T0: table0_bridgewater_validation.csv]. For Q1 2020, the replicator returned -8.1% versus a reported -14% (FT/Reuters, April 2020) [VERIFY]. For full-year 2022, the replicator returned -7.4% versus a reported -9.4% (Bloomberg, January 2023) [VERIFY]. In both cases the replicator captures the correct sign and approximate magnitude but understates the loss, consistent with its 1.5x leverage cap versus All Weather's higher actual leverage. The validation is preliminary — only two reference points are currently available, and additional press research during the paper write-up phase will expand this comparison. See fig0_bridgewater_validation.png for the monthly return comparison chart.

## COVID drawdown (February-March 2020)

The S&P 500 lost 33.9% peak-to-trough over 23 trading days [T1: ^GSPC, covid_2020, max_drawdown]. JPMorgan equity fell harder at -42.5% [T1: JPM, covid_2020, max_drawdown], consistent with bank stocks carrying credit-cycle exposure on top of market beta. JPM equity reflects bank balance-sheet exposure (loan-loss provisions, trading book mark-to-market) rather than the firm's AI execution architecture. Direct observation of JPM's systematic products is possible only via JEPI and JEPQ, which launched May 2020 and May 2022 respectively and therefore appear only in the 2024 event analysis.

BlackRock's IVV tracked the index at -33.9% [T1: IVV, covid_2020, max_drawdown]. The Two Sigma factor proxy drew down -30.1% [T1: TwoSigma_factor_proxy, covid_2020, max_drawdown], slightly less than the index — the managed-futures (DBMF) and min-vol (USMV) components provided modest cushioning.

The Bridgewater risk-parity replicator lost -10.6% over the event window [T1: Bridgewater_replicator, covid_2020, event_total_return] with a peak drawdown of -15.7% [T1: Bridgewater_replicator, covid_2020, max_drawdown]. Recovery took 135 days [T1: Bridgewater_replicator, covid_2020, recovery_days]. Press reports placed actual All Weather losses at approximately -14% for Q1 2020 (FT and Reuters, April 2020) [VERIFY]. The replicator's shallower loss (-8.1% for the full quarter [T0: 2020-Q1, replicator_return]) is expected: our leverage cap of 1.5x is conservative relative to All Weather's reported leverage of 3-4x on the bond sleeve, and the ETF-based construction cannot replicate Bridgewater's regime-aware overlay that adjusts allocations intra-month. The replicator captures the directional risk profile and the sign of failure (risk parity breaks when bond-equity correlations invert) but understates magnitude — an appropriate caveat stated throughout the paper.

AGG fell -9.6% [T1: AGG, covid_2020, max_drawdown] but recovered within 7 days once the Fed announced unlimited QE. TLT's drawdown of -15.7% [T1: TLT, covid_2020, max_drawdown] reversed within one trading day of the trough, coincident with the Federal Reserve's March 23, 2020 announcement of unlimited Treasury and agency MBS purchases. The recovery reflects policy intervention rather than market-based mean reversion.

## Yen carry unwind (August 2024)

Drawdowns were far smaller. The S&P 500 lost 6.1% and recovered in 10 days [T1: ^GSPC, yen_carry_2024, max_drawdown / recovery_days]. The Nikkei 225 bore the brunt at -19.5% [T1: ^N225, yen_carry_2024, max_drawdown], consistent with forced unwind of yen-funded positions hitting Tokyo directly.

The Bridgewater replicator gained +0.9% over the event window [T1: Bridgewater_replicator, yen_carry_2024, event_total_return] with a shallow -4.6% intra-window drawdown [T1: Bridgewater_replicator, yen_carry_2024, max_drawdown]. Risk parity was largely unaffected because the mechanism (rates repricing) did not trigger the bond-equity correlation break that hurts the strategy. This contrasts sharply with its -15.7% drawdown in 2020.

JPMorgan equity fell -8.4% [T1: JPM, yen_carry_2024, max_drawdown]. The Two Sigma factor proxy lost -6.2% and took 14 days to recover [T1: TwoSigma_factor_proxy, yen_carry_2024, max_drawdown / recovery_days] — slightly longer than the market, possibly reflecting momentum-factor crowding during the unwind. TLT fell -11.1% [T1: TLT, yen_carry_2024, max_drawdown] without recovering in the post-window, consistent with the BoJ rate hike structurally repricing duration.

## Correlation regime shifts

COVID 2020 produced clear correlation convergence: average off-diagonal correlation jumped from 0.25 to 0.50, a 98% increase [T2: covid_2020]. Post-event it settled at 0.41, remaining elevated. The yen carry event showed a smaller shift: 0.37 to 0.44, a 19% increase [T2: yen_carry_2024]. Post-event correlations fell to 0.34, below pre-event levels. The four architectures moved in lockstep during credit stress but maintained more independence during a rates-driven, geographically concentrated event.

## Event-window liquidity regressions

The event-window regression (Analysis 4b) tests whether bid-ask spread widening predicts next-day returns within each crisis [T4b: table4b_liquidity_regression_by_window.csv]. A negative coefficient on lagged Corwin-Schultz spread means that when spreads widen today, the strategy loses value tomorrow — the mechanical signature of forced selling into illiquid markets. Strategies exposed to this channel are those whose holders must liquidate when funding costs spike.

In the 2020 window, three strategies showed significant negative spread coefficients: AGG (beta=-1.16, t=-2.75, p=0.006), HYG (beta=-0.47, t=-3.62, p<0.001), and MTUM (beta=-0.13, t=-2.82, p=0.005) [T4b: covid_2020]. These are the credit-sensitive and crowded-factor instruments — exactly what the liquidity channel predicts. The Bridgewater replicator and Two Sigma factor proxy showed no significant spread sensitivity in 2020, consistent with their broader diversification across asset classes.

In the 2024 window, no strategy exhibited a significant negative spread coefficient [T4b: yen_carry_2024]. The absence is informative. The yen carry unwind was a rates event, not a credit event; U.S. bid-ask spreads widened modestly but did not reach levels that forced liquidation. This result is consistent with the credit-liquidity hypothesis: the channel activates specifically when U.S. credit markets freeze, not during all regime breaks. Two events cannot prove this — the test could have failed (showing significant negative coefficients in 2024 too) and it did not. That is the strongest claim the data supports.

## Consistent vs. idiosyncratic failures

JPMorgan equity drew down hardest in both events relative to its benchmark (-42.5% vs S&P -33.9% in 2020; -8.4% vs -6.1% in 2024). Execution-layer AI does not insulate the equity from market beta. TLT suffered in both events but for structurally different reasons: safe-haven correlation break in 2020, BoJ policy repricing in 2024.

The Bridgewater replicator shows the clearest architectural differentiation. It lost -15.7% in 2020 (when bond-equity correlations inverted) but was essentially flat in 2024 (when the shock was rates-driven but did not break the diversification assumption). This is the expected behavior of risk parity: vulnerable to correlation regime change, resilient to directional shocks that preserve the cross-asset structure.

The Two Sigma factor proxy underperformed the S&P slightly in 2020 (-30.1% vs -33.9%) but tracked it closely in 2024 (-6.2% vs -6.1%). Factor crowding appears more acute during broad credit events than during geographically concentrated rate shocks.

## Caveats

Two events cannot constitute a statistical sample. The results describe what happened; they cannot distinguish architectural failure from coincidence with inferential rigor. The event-window regression (n=22 to 42 observations per window) has limited statistical power — the significant coefficients in 2020 are suggestive but not definitive.

The Bridgewater replicator uses ETFs, not futures, and caps leverage at 1.5x. Actual All Weather operates with higher leverage and a regime overlay we cannot replicate. The Two Sigma factor proxy captures only the systematic exposure profile; actual fund returns could differ materially. JEPI and JEPQ launched after the 2020 event and appear only in the 2024 analysis.

Alternative explanations for the correlation asymmetry include: (a) event duration (23 days vs 8 days — longer stress periods mechanically produce higher correlations as portfolios are forced to de-risk), (b) shock magnitude (5x larger in 2020), and (c) geographic scope (global vs Asia-concentrated). Disentangling these from the credit-liquidity mechanism requires additional events.
