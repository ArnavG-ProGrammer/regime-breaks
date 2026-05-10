# Findings Memo — Phase 1.5 Empirical Results

## Headline

Average pairwise correlations across the strategy proxies nearly doubled during the March 2020 COVID drawdown — from 0.25 pre-event to 0.50 in the event window [T2: covid_2020, pre_avg_corr / event_avg_corr]. In the August 2024 yen carry unwind, correlations rose modestly from 0.37 to 0.44 [T2: yen_carry_2024, pre_avg_corr / event_avg_corr]. This asymmetry is consistent with common-mode failure driven by U.S. credit liquidity stress, but alternative explanations exist: the 2020 event lasted 23 trading days versus 8 for 2024, and peak drawdowns differed by 5x.

An event-window liquidity regression sharpens the picture. In 2020, the lagged Corwin-Schultz spread coefficient was significantly negative for AGG (t=-2.75, p=0.006), HYG (t=-3.62, p<0.001), and MTUM (t=-2.82, p=0.005) [T4b: covid_2020, AGG/HYG/MTUM]. Wider spreads predicted lower next-day returns — the signature of liquidity-driven selling. In 2024, no strategy showed a significant negative spread coefficient [T4b: yen_carry_2024]. The two significant coefficients (HYG, Bridgewater replicator) were positive, suggesting a different mechanism. The credit-liquidity hypothesis survives this test but cannot be confirmed with two events alone.

## COVID drawdown (February-March 2020)

The S&P 500 lost 33.9% peak-to-trough over 23 trading days [T1: ^GSPC, covid_2020, max_drawdown]. JPMorgan equity fell harder at -42.5% [T1: JPM, covid_2020, max_drawdown], consistent with bank stocks carrying credit-cycle exposure on top of market beta. BlackRock's IVV tracked the index at -33.9% [T1: IVV, covid_2020, max_drawdown]. The Two Sigma factor proxy drew down -30.1% [T1: TwoSigma_factor_proxy, covid_2020, max_drawdown], slightly less than the index — the managed-futures (DBMF) and min-vol (USMV) components provided modest cushioning.

The Bridgewater risk-parity replicator lost -10.6% [T1: Bridgewater_replicator, covid_2020, event_total_return] with a peak drawdown of -15.7% [T1: Bridgewater_replicator, covid_2020, max_drawdown]. Recovery took 135 days [T1: Bridgewater_replicator, covid_2020, recovery_days]. This is directionally consistent with press-reported All Weather losses of approximately -14% in Q1 2020. The replicator's underperformance relative to published figures likely reflects its ETF-based construction missing the actual fund's leverage and regime overlay.

AGG fell -9.6% [T1: AGG, covid_2020, max_drawdown] but recovered within 7 days once the Fed announced unlimited QE. TLT dropped -15.7% [T1: TLT, covid_2020, max_drawdown] and recovered in a single day — Treasuries briefly lost safe-haven status before policy restored it.

## Yen carry unwind (August 2024)

Drawdowns were far smaller. The S&P 500 lost 6.1% and recovered in 10 days [T1: ^GSPC, yen_carry_2024, max_drawdown / recovery_days]. The Nikkei 225 bore the brunt at -19.5% [T1: ^N225, yen_carry_2024, max_drawdown], consistent with forced unwind of yen-funded positions hitting Tokyo directly.

The Bridgewater replicator gained +0.9% over the event window [T1: Bridgewater_replicator, yen_carry_2024, event_total_return] with a shallow -4.6% intra-window drawdown [T1: Bridgewater_replicator, yen_carry_2024, max_drawdown]. Risk parity was largely unaffected because the mechanism (rates repricing) did not trigger the bond-equity correlation break that hurts the strategy. This contrasts sharply with its -15.7% drawdown in 2020.

JPMorgan equity fell -8.4% [T1: JPM, yen_carry_2024, max_drawdown]. The Two Sigma factor proxy lost -6.2% and took 14 days to recover [T1: TwoSigma_factor_proxy, yen_carry_2024, max_drawdown / recovery_days] — slightly longer than the market, possibly reflecting momentum-factor crowding during the unwind. TLT fell -11.1% [T1: TLT, yen_carry_2024, max_drawdown] without recovering in the post-window, consistent with the BoJ rate hike structurally repricing duration.

## Correlation regime shifts

COVID 2020 produced clear correlation convergence: average off-diagonal correlation jumped from 0.25 to 0.50, a 98% increase [T2: covid_2020]. Post-event it settled at 0.41, remaining elevated. The yen carry event showed a smaller shift: 0.37 to 0.44, a 19% increase [T2: yen_carry_2024]. Post-event correlations fell to 0.34, below pre-event levels. The four architectures moved in lockstep during credit stress but maintained more independence during a rates-driven, geographically concentrated event.

## Consistent vs. idiosyncratic failures

JPMorgan equity drew down hardest in both events relative to its benchmark (-42.5% vs S&P -33.9% in 2020; -8.4% vs -6.1% in 2024). Execution-layer AI does not insulate the equity from market beta. TLT suffered in both events but for structurally different reasons: safe-haven correlation break in 2020, BoJ policy repricing in 2024.

The Bridgewater replicator shows the clearest architectural differentiation. It lost -15.7% in 2020 (when bond-equity correlations inverted) but was essentially flat in 2024 (when the shock was rates-driven but did not break the diversification assumption). This is the expected behavior of risk parity: vulnerable to correlation regime change, resilient to directional shocks that preserve the cross-asset structure.

The Two Sigma factor proxy underperformed the S&P slightly in 2020 (-30.1% vs -33.9%) but tracked it closely in 2024 (-6.2% vs -6.1%). Factor crowding appears more acute during broad credit events than during geographically concentrated rate shocks.

## Caveats

Two events cannot constitute a statistical sample. The results describe what happened; they cannot distinguish architectural failure from coincidence with inferential rigor. The event-window regression (n=22 to 42 observations per window) has limited statistical power — the significant coefficients in 2020 are suggestive but not definitive.

The Bridgewater replicator uses ETFs, not futures, and caps leverage at 1.5x. Actual All Weather operates with higher leverage and a regime overlay we cannot replicate. The Two Sigma factor proxy captures only the systematic exposure profile; actual fund returns could differ materially. JEPI and JEPQ launched after the 2020 event and appear only in the 2024 analysis.

Alternative explanations for the correlation asymmetry include: (a) event duration (23 days vs 8 days — longer stress periods mechanically produce higher correlations as portfolios are forced to de-risk), (b) shock magnitude (5x larger in 2020), and (c) geographic scope (global vs Asia-concentrated). Disentangling these from the credit-liquidity mechanism requires additional events.
