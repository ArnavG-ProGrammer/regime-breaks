# Section 8: Conclusion

Four institutional risk architectures — execution-layer AI, factor-covariance risk modelling, regime-aware risk parity, and multi-factor systematic strategies — converged during the March 2020 COVID drawdown and diverged during the August 2024 yen carry unwind. Average pairwise correlations nearly doubled in 2020 (from 0.25 to 0.50) and rose only modestly in 2024 (from 0.37 to 0.44). The event-window regression identifies the specific channel: in 2020, wider bid-ask spreads predicted lower next-day returns for AGG, HYG, and MTUM — the empirical signature of forced selling into illiquid credit markets. In 2024, no strategy showed the same pattern. Architectural diversity did not prevent correlated failure; the credit-liquidity channel operated below the level of model architecture, at the level of funding markets.

The result is bounded by its evidence. Two events cannot prove a causal mechanism. The Bridgewater and Two Sigma proxies introduce magnitude uncertainty. The event-window regressions, with 22 to 42 observations per window, have limited statistical power. The significant coefficients would not survive Bonferroni correction across the full strategy panel. These are empirical regularities from two well-documented regime breaks, not a general law. Future research should test the credit-liquidity hypothesis on out-of-sample events — the March 2023 regional bank crisis and subsequent dislocations — using the reproducible pipeline and falsifiable specification provided with this paper.

The broader point is simple. The systemic risk of AI and quantitative strategies in finance does not depend primarily on whether firms use the same models. It depends on whether their portfolios share exposure to the same funding channels. Supervising model architecture is necessary. Supervising the funding channel that connects architecturally diverse portfolios may be more important for financial stability.

---

## STYLE_AUDIT

**Word counts:**
- Paragraph 1 (empirical finding): 115
- Paragraph 2 (bounds and future work): 101
- Paragraph 3 (closing thought): 62
- Total: ~278

**Banned phrases found:** 0

**[VERIFY] tags:** 0

**Sentence statistics:**
- Total sentences: ~16
- Mean sentence length: ~16.2 words
- Standard deviation: ~9.1 words
- Range: 5 to 40 words
