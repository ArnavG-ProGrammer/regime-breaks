# Project Brief — When Machines Disagree

**Re-read this at the start of every phase.**

## Research question

Do four nominally distinct AI/quantitative risk architectures fail in the same way during regime breaks, or differently? The answer bears on whether widespread AI adoption in finance increases systemic concentration risk.

## The four firms and what they represent

1. **JPMorgan** — execution-layer AI (order routing, liquidity prediction) on a discretionary mandate. Observed via JPM equity, JEPI, JEPQ.
2. **BlackRock** — factor-covariance risk modelling via Aladdin. Observed via iShares ETFs: IVV, AGG, TLT, EEM, HYG.
3. **Bridgewater** — macro regime modelling with risk parity (All Weather). Returns are private; observed via an inverse-vol risk-parity *replicator* (IVV, TLT, TIP, DBC, GLD), vol-targeted at 10%, leverage capped at 1.5x. **This is not All Weather.** Cross-checked against press-disclosed monthly returns.
4. **Two Sigma** — multi-factor systematic strategies. Returns are private; observed via an equal-weight basket of factor ETFs (MTUM, VLUE, QUAL, USMV, DBMF). **This captures the exposure profile, not Two Sigma's alpha.**

## The two events

- **COVID drawdown:** 2020-02-19 (S&P peak) to 2020-03-23 (trough, -33.9%). Pre-window from 2019-10-01; post-window to 2020-08-01.
- **Yen carry unwind:** 2024-07-31 (BoJ rate hike) to 2024-08-09 (stabilization). Pre-window from 2024-04-01; post-window to 2024-12-13.

## The five analyses

1. **Drawdown comparison** — peak-to-trough drawdown, vol, recovery time per firm per event.
2. **Correlation regime-shift** — pre/event/post correlation matrices; tests whether diverse strategies converge under stress.
3. **Volatility breach** — event-window realized vol vs long-run vol; breach ratio >3x signals risk-model failure.
4. **Liquidity-dependency regression** — return ~ S&P beta + VIX + lagged Corwin-Schultz spread (HAC-robust). Tests whether returns are explained by liquidity stress beyond market beta.
5. **Cross-event synthesis** — combines drawdowns and vol-breach across both events; separates architectural failures (both events) from idiosyncratic ones (one event only).

## Non-negotiables

- **Methodology is fixed:** log returns, HAC standard errors (Newey-West, 5 lags), Corwin-Schultz spread estimator, 90-trading-day pre/post windows.
- **Event windows are fixed.** Do not alter dates.
- **Proxy choices are fixed.** Do not substitute tickers or change basket composition.
- **Scaffold files are read-only** in Phase 1.
