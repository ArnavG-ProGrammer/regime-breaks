# Findings Memo — Phase 1 Empirical Results

## Headline

During the March 2020 COVID drawdown, average pairwise correlations across the strategy proxies doubled — from 0.24 pre-event to 0.51 during the event window. In the August 2024 yen carry unwind, the same shift was muted: correlations rose only from 0.35 to 0.45. This asymmetry suggests the common-mode failure observed in 2020 was conditional on U.S. credit liquidity stress rather than a universal property of regime breaks.

## COVID drawdown (February-March 2020)

The S&P 500 lost 33.9% peak-to-trough over 23 trading days. JPMorgan equity fell harder (-42.5%), consistent with bank stocks carrying both market beta and credit-cycle exposure. BlackRock's IVV tracked the index almost exactly (-33.9%), as expected for a passive vehicle. The Two Sigma factor proxy drew down -30.1%, slightly less than the index, suggesting modest defensive positioning from the minimum-volatility and managed-futures components. AGG (-9.6%) recovered within 7 days once the Fed announced unlimited QE on March 23. TLT (-15.7%) recovered in a single day — the sharp reversal indicates Treasuries briefly lost safe-haven status before policy restored it.

## Yen carry unwind (August 2024)

Drawdowns were far smaller in absolute terms. The S&P 500 lost 6.1% and recovered in 10 days. The Nikkei 225 bore the brunt at -19.5%, consistent with the mechanism: forced unwind of yen-funded positions hit Tokyo most directly. JPMorgan equity (-8.4%) and IVV (-6.0%) tracked the S&P. The Two Sigma factor proxy lost -6.2% and took 14 days to recover — slightly longer than the market, possibly reflecting momentum-factor crowding during the unwind. TLT fell -11.1% and had not recovered by the end of the post-window, consistent with the BoJ rate hike structurally repricing duration.

## Correlation regime shifts

COVID 2020 produced a clear correlation convergence: average off-diagonal correlation jumped from 0.24 to 0.51 (a 110% increase). Post-event it settled at 0.40, remaining elevated. The yen carry event showed a much smaller shift: 0.35 to 0.45 (27% increase), and post-event correlations actually fell below their pre-event level (0.28). The four architectures moved in lockstep during credit stress but maintained more independence during a rates-driven event.

## Consistent vs. idiosyncratic failures

JPMorgan equity drew down hardest in both events relative to its benchmark exposure. This is consistent with the architecture — execution-layer AI does not insulate the equity from market beta; JPM stock carries additional credit and earnings risk. The Two Sigma factor proxy underperformed the S&P slightly in 2020 but tracked it closely in 2024, suggesting factor crowding was more acute in the credit event. TLT suffered in both events but for different structural reasons (safe-haven correlation break in 2020; BoJ policy repricing in 2024).

## Caveats

Two events cannot constitute a statistical sample. The results describe what happened; they cannot distinguish architectural failure from coincidence with any inferential rigor. The Bridgewater replicator produced zero returns due to a NaN-propagation bug in the rolling-window volatility calculation — it must be fixed before any claims about Bridgewater's architecture can be made. The Two Sigma factor proxy captures only the systematic exposure profile; actual Two Sigma returns could differ materially due to alpha, leverage, and hedging we cannot observe. JEPI and JEPQ launched after the 2020 event and therefore only appear in the 2024 analysis.
