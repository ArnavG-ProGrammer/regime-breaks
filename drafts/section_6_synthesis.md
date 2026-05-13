# Section 6: Cross-Event Synthesis

## 6.1 The architectural test

The two-event design tests whether four institutional risk architectures fail in the same way or in different ways under stress. The answer is: both, depending on the channel.

In March 2020, all four architectures suffered significant drawdowns. JPMorgan equity fell -42.5%, the BlackRock iShares family tracked or exceeded the S&P 500's -33.9% decline across every product, the Bridgewater risk-parity replicator drew down -15.7%, and the Two Sigma factor proxy lost -30.1%. Average pairwise correlations nearly doubled, from 0.25 pre-event to 0.50 in the event window. Nominally diverse strategies converged — the empirical definition of common-mode failure.

In August 2024, the same architectures produced different outcomes. The S&P 500 fell -6.1%. JPMorgan equity lost -8.4%. The BlackRock products drew down modestly, except TLT (-11.1%), which reflected a structural repricing of global duration rather than liquidity stress. The Two Sigma factor proxy tracked the market almost exactly at -6.2%. And the Bridgewater replicator gained +0.9% over the event window. Average pairwise correlations rose only 19%, from 0.37 to 0.44, and fell below pre-event levels afterward. Strategies maintained their independence.

The contrast between the two events is the paper's central finding. Two numbers summarize it: a 98% correlation increase in 2020 versus a 19% increase in 2024. This is not a generic "regime breaks cause correlated failure" result. The correlation convergence was specific to the credit-liquidity event.

## 6.2 The credit-liquidity mechanism

The event-window regression identifies the specific channel. In the 2020 window, three strategies showed significant negative coefficients on the lagged Corwin-Schultz bid-ask spread: AGG (p = 0.006), HYG (p < 0.001), and MTUM (p = 0.005). Wider spreads on day t-1 predicted lower returns on day t, after controlling for market beta and VIX. This is the Brunnermeier and Pedersen (2009) funding-liquidity spiral operating at daily frequency: margin calls force liquidation, liquidation widens spreads, wider spreads trigger further margin calls.

In the 2024 window, no strategy showed a significant negative spread coefficient. The test could have failed — if the same regression signature had appeared during the yen carry unwind, the credit-liquidity explanation would be indistinguishable from a generic stress explanation. It did not fail. The two significant coefficients in 2024 (HYG and the Bridgewater replicator) were positive, consistent with mean reversion after a transient volatility spike rather than forced selling into frozen markets.

The selection of AGG, HYG, and MTUM in 2020 is not arbitrary. It traces the credit-liquidity channel through three distinct instrument classes. AGG holds investment-grade bonds and Treasuries — the instruments that institutional investors sell first when they need cash, because they are normally the most liquid. When that liquidity evaporates, selling becomes self-reinforcing. HYG holds high-yield credit, the most stressed segment of the bond market in March 2020 when the ICE BofA High Yield OAS exceeded 1,100 basis points. MTUM holds recent equity winners — crowded systematic positions that are unwound first by the most leveraged participants when funding costs spike. Each instrument sits at a different point in the financial system, but all three were connected by the same funding channel.

## 6.3 Concentration and systemic risk

The findings bear on the regulatory debate about systemic concentration in AI-driven and quantitative finance. The Financial Stability Oversight Council (2014) raised concerns that "financial firms may rely too heavily on the same outside risk models." The UK Financial Conduct Authority (2021) warned that the failure of a large portfolio and risk system such as BlackRock's Aladdin "could cause serious consumer harm" or "damage market integrity." These concerns implicitly assume that architectural diversity provides systemic resilience — that if different firms use different models, the system is safer.

The 2020 data complicate this assumption. JPMorgan's execution-layer AI, BlackRock's factor-covariance risk models, Bridgewater's risk parity, and Two Sigma's multi-factor systematic strategies are architecturally distinct. They make different bets about which correlations will hold under stress. Yet in March 2020, they converged. The mechanism was not that they shared a model; it was that they shared exposure to U.S. credit liquidity. Architectural diversity did not prevent correlated failure because the common-mode channel operated below the level of model architecture — at the level of funding markets.

This is consistent with the theoretical framework of Adrian and Brunnermeier (2016), who measure systemic contribution via CoVaR — the value-at-risk of the financial system conditional on one institution being in distress. Their insight is that systemic risk arises not from individual institution failure but from the correlation of failures across institutions. The empirical contribution of this paper is to show that this correlation is channel-specific: it was activated by credit-liquidity stress in 2020 but not by rates-driven stress in 2024. Acharya, Pedersen, Philippon, and Richardson (2017) formalize a related point through the concept of systemic expected shortfall (SES), measuring each institution's propensity to be undercapitalized precisely when the system as a whole is undercapitalized [VERIFY — confirm Acharya et al. 2017 is the correct citation for SES].

The practical implication is that stress tests and systemic risk assessments should focus less on whether institutions use different models and more on whether they share exposure to the same funding channels. Architectural diversity is a weak defense when funding liquidity is the common mode of failure.

## 6.4 What the paper does not show

Three limitations constrain the inference.

First, two events cannot prove a causal mechanism. The results are consistent with the credit-liquidity hypothesis, but alternative explanations survive. The 2020 event lasted 23 trading days versus 8 for 2024. The S&P 500 drawdown was -33.9% versus -6.1%. The geographic scope was global versus Asia-concentrated. Duration, magnitude, and geographic scope are all confounded with the credit-liquidity distinction. Disentangling these factors requires additional events — the March 2023 regional bank crisis (SVB, Signature, First Republic) is a candidate for future work, as it produced U.S. credit stress without a global pandemic.

Second, the Bridgewater and Two Sigma proxies introduce magnitude uncertainty. The Bridgewater replicator caps leverage at 1.5x and cannot replicate the firm's regime overlay. The Two Sigma proxy excludes alpha, leverage, and dynamic hedging. Both proxies capture the directional risk profile — a correct sign is more informative than a precise magnitude — but actual fund returns could differ materially from what we measure.

Third, the event-window regressions operate on 22 to 42 observations per window. The significant p-values in 2020 (0.006, <0.001, 0.005) are strong for single-strategy tests but would not survive a Bonferroni correction for multiple comparisons across all strategies in the panel. The results are suggestive, not definitive.

## 6.5 Implications for AI in finance

The four architectures examined here represent different answers to the question of where AI and quantitative methods sit in the investment process. JPMorgan uses AI at the execution layer. BlackRock uses quantitative risk models for portfolio construction and oversight. Bridgewater uses systematic rules for regime identification and risk allocation. Two Sigma uses statistical models for signal generation and trade selection. These are architecturally distinct.

The findings suggest that the systemic risk of AI in finance depends less on the architecture of individual firms' AI systems and more on their shared exposure to funding and liquidity channels. A sophisticated reinforcement-learning execution system and a simple factor-covariance risk model can fail simultaneously — not because they share code, training data, or model architecture, but because they share exposure to the same credit markets. This is a specific, falsifiable claim: future credit-liquidity events should produce correlated failure across architecturally diverse strategies, while future rates-driven or geographically concentrated events should not, unless they activate U.S. credit markets.

The Financial Stability Board's work on AI and machine learning in financial services (FSB, 2017) identifies model risk, data dependency, and concentration among third-party providers as key systemic concerns [VERIFY — confirm FSB 2017 report title and date]. The evidence here suggests an additional concern: even when AI systems are fully independent, they can fail together because their portfolios — not their models — share common-mode exposure. Supervising the model is necessary. Supervising the funding channel may be more important.

---

## STYLE_AUDIT

**Word counts:**
- 6.1 Architectural test: 246
- 6.2 Credit-liquidity mechanism: 275
- 6.3 Concentration and systemic risk: 264
- 6.4 What the paper does not show: 230
- 6.5 Implications for AI in finance: 218
- Total: ~1,233

**Banned phrases found:** 0

**[VERIFY] tags:** 2
- Acharya et al. (2017) SES citation (1)
- FSB (2017) report title and date (1)

**Sentence statistics:**
- Total sentences: ~78
- Mean sentence length: ~14.5 words
- Standard deviation: ~8.2 words
- Range: 4 to 42 words
