# When Machines Disagree
## A Comparative Analysis of Four Institutional Risk Architectures Under Regime Breaks (March 2020 and August 2024)

**Arnav Goyal**
*Ahlcon International School, New Delhi*
*Working paper, 2026. Comments welcome.*

---

> *Skeleton document. Sections marked [TODO] are to be drafted week by week
> per the schedule in `README.md`. Citations marked [CITE] are anchor
> references -- read these first, do not write the section without them.
> Word budgets are guidelines, not ceilings.*

---

## Abstract (150 words, write LAST)

[TODO Week 5] One-paragraph statement of question, method, finding, and
why it matters. Should be readable to a Wharton AO who has never thought
about risk parity. Lead with the empirical finding ("we find that..."), not
with the motivation.

---

## 1. Introduction (1.5 pages, ~600 words)

The premise: when markets break, do AI/quantitative architectures fail in
the same way, or do they fail differently? This question matters because
the answer determines whether widespread AI adoption in finance increases
*or decreases* systemic concentration risk.

We study two regime breaks:

- **March 2020 (COVID drawdown).** S&P 500 fell 33.9% in 23 trading days.
  Treasury-equity correlation briefly turned positive. Investment-grade
  credit liquidity froze until the Fed's 23 March announcement of unlimited
  QE and corporate credit facilities.
- **August 2024 (yen carry unwind).** Bank of Japan raised its policy
  rate to 0.25% on 31 July 2024. The Nikkei 225 fell 12.4% on 5 August
  2024 -- its largest single-day drop since the 1987 Black Monday crash.
  VIX spiked intraday to 65.73. The cascade lasted approximately five
  trading days before reversing.

We compare four institutional architectures: JPMorgan (execution-layer AI
on a discretionary mandate), BlackRock (factor-based covariance risk
modelling via Aladdin-overseen products), Bridgewater (macro regime
modelling with risk parity), and Two Sigma (multi-factor systematic
strategies, proxied by public factor ETFs).

We find that [INSERT FINDING -- likely something like: "during March 2020,
average pairwise correlations across nominally diverse strategies rose from
0.3X to 0.8X within five trading days, consistent with common-mode failure;
in August 2024 the same correlation regime shift did NOT occur, suggesting
that the risk-model overlap that produced March 2020's homogeneous failure
mode is conditional on liquidity stress in U.S. credit specifically."]

The contribution is modest but specific: a public, reproducible empirical
test of whether four nominally distinct AI/quantitative architectures
behave like one architecture under stress.

## 2. Background and architecture taxonomy (3 pages, ~1200 words)

### 2.1 JPMorgan: execution-layer AI

[CITE] Bloomberg, "JPMorgan Software Does in Seconds What Took Lawyers
360,000 Hours" (Son, 2017). [CITE] JPMorgan 2024 Annual Report. Key
public artifacts: COiN (contract intelligence), LOXM (RL-based order
routing), and the JEPI/JEPQ family of systematic option-overlay ETFs.

The architectural claim: JPM's AI lives at the *execution* layer -- order
slicing, liquidity prediction -- while the position-taking decision remains
discretionary. This architecture should be *insensitive* to regime breaks,
because microstructure-layer optimization does not depend on covariance
matrix stability.

### 2.2 BlackRock: factor-covariance risk models (Aladdin)

[CITE] BlackRock 2025 Form 10-K (SEC EDGAR). As of 31 December 2025,
total AUM was $14.0 trillion; Aladdin-overseen assets were approximately
$25 trillion across roughly 1,000 institutional clients (BlackRock 10-K
FY2025; Wikipedia *Aladdin (BlackRock)* citing the 10-K disclosure).
[CITE] FT, "BlackRock's black box: the technology hub of modern finance"
(Henderson and Walker, 2020).

Aladdin's risk decomposition relies on factor models with historical
covariance matrices estimated over rolling windows. The architectural
claim: this design is *vulnerable* to regime breaks because correlations
estimated on pre-crisis data understate cross-asset comovement during
stress. If many institutional clients run similar Aladdin-derived risk
overlays, common-mode de-risking can amplify drawdowns.

### 2.3 Bridgewater: regime-aware risk parity

[CITE] Dalio, R. (2017). *Principles*. Simon & Schuster. [CITE]
Bridgewater Associates, "Our thoughts about risk parity and All Weather"
(daily observations note, 2020). [CITE] Wigglesworth, R. (2021). *Trillions:
How a Band of Wall Street Renegades Invented the Index Fund and Changed
Finance Forever*.

Risk parity allocates capital to equalize *risk* contribution from each
asset class, leveraging low-volatility assets (bonds) to match the risk
of equities. Architectural claim: should suffer disproportionately when
the bond-equity correlation breaks (briefly true in March 2020). All
Weather's publicly disclosed March 2020 drawdown of approximately -14%
(per FT and Reuters reporting) substantially exceeded the strategy's
stated annualized vol target.

### 2.4 Two Sigma: multi-factor systematic

[CITE] Two Sigma research notes from twosigma.com/insights. [CITE]
Patterson, S. (2010). *The Quants*. Crown Business.

Founded 2001 by David Siegel and John Overdeck; ~$60bn AUM as of 2024.
Runs short-to-medium-horizon systematic strategies across equity,
macro, and event-driven mandates. Architectural claim: shorter signal
half-lives mean faster mean reversion after a regime break, but also
greater exposure to factor crowding.

## 3. Data and methodology (2 pages, ~800 words)

[TODO Week 3] Describe the pipeline. Reference the public GitHub repo.
List proxies explicitly. State frequency (daily for all primary
analyses). Note the Bridgewater replicator is not All Weather and is
cross-checked against monthly disclosures.

Key methodological choices to defend:
- Log returns throughout (additive aggregation).
- HAC-robust standard errors in Section 5 regressions (Newey-West, 5 lags).
- Corwin-Schultz spread estimator for liquidity (Corwin and Schultz, 2012,
  *Journal of Finance* 67(2): 719-760).
- Event windows: 90 trading days pre, the event itself, 90 trading days
  post. Choice of 90 days follows [CITE] MacKinlay (1997) event-study
  conventions.

## 4. Event 1 -- COVID drawdown, February-March 2020 (4 pages)

[TODO Week 3] Drawdown table. Correlation heatmap (pre / event / post).
Vol-breach analysis. Liquidity regression results. Discussion focused on
what each architecture predicted vs what happened.

## 5. Event 2 -- Yen carry unwind, August 2024 (3 pages)

[TODO Week 3] Same structure as Section 4. The interesting comparison:
which architectures that struggled in March 2020 also struggled here, and
which did not? The latter case is informative -- it identifies failures
that were *idiosyncratic* to one regime rather than architectural.

## 6. Cross-event synthesis and the concentration argument (3 pages)

[TODO Week 4] **This is the money section.** Headline finding restated.
Implications for systemic risk. Specific argument: if X% of global equity
is overseen via risk overlays that share factor structure, regime breaks
that activate that shared structure will exhibit common-mode failure
regardless of the firm-level branding of the strategies running on top.
Cite [CITE] Adrian and Brunnermeier (2016) on CoVaR and systemic risk;
[CITE] Acharya, Pedersen, Philippon and Richardson (2017) on systemic
risk measurement; [CITE] FSB reports on non-bank financial intermediation.

## 7. Limitations and falsifiability (1 page)

State explicitly:
- The Bridgewater and Two Sigma proxies are imperfect.
- Two events is not a sample; we cannot distinguish architecture from
  luck definitively. A third event (e.g. SVB / regional bank stress
  March 2023) would strengthen the inference.
- ETF returns include creation/redemption frictions.
- The concentration argument relies on assumptions about strategy
  overlap that are not fully observable from public filings.

State what would falsify the central claim:
> "If, in an event with similar microstructure but no shared U.S. credit
> liquidity stress, we still observed correlation convergence across the
> four architectures, the common-mode-via-credit-liquidity hypothesis
> would be inconsistent with the data."

## 8. Conclusion (0.5 page)

[TODO Week 4] One paragraph. State the finding. State its scope. State
what comes next.

---

## References

[TODO Week 5] Real, complete, every URL working. Anchor citations:

- Acharya, V. V., & Pedersen, L. H. (2005). Asset pricing with liquidity
  risk. *Journal of Financial Economics*, 77(2), 375-410.
- Adrian, T., & Brunnermeier, M. K. (2016). CoVaR. *American Economic
  Review*, 106(7), 1705-1741.
- Adrian, T., & Shin, H. S. (2010). Liquidity and leverage. *Journal of
  Financial Intermediation*, 19(3), 418-437.
- BlackRock, Inc. (2026). Form 10-K, fiscal year 2025. U.S. Securities
  and Exchange Commission. https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001364742
- Brunnermeier, M. K., & Pedersen, L. H. (2009). Market liquidity and
  funding liquidity. *Review of Financial Studies*, 22(6), 2201-2238.
- Corwin, S. A., & Schultz, P. (2012). A simple way to estimate bid-ask
  spreads from daily high and low prices. *Journal of Finance*, 67(2),
  719-760.
- Hendershott, T., Jones, C. M., & Menkveld, A. J. (2011). Does
  algorithmic trading improve liquidity? *Journal of Finance*, 66(1),
  1-33.
- MacKinlay, A. C. (1997). Event studies in economics and finance.
  *Journal of Economic Literature*, 35(1), 13-39.
- Patterson, S. (2010). *The Quants*. Crown Business.
- Son, H. (2017, February 28). JPMorgan software does in seconds what
  took lawyers 360,000 hours. *Bloomberg*.
  https://www.bloomberg.com/news/articles/2017-02-28/jpmorgan-marshals-an-army-of-developers-to-automate-high-finance
- Wigglesworth, R. (2021). *Trillions*. Penguin Business.
- Zuckerman, G. (2019). *The Man Who Solved the Market: How Jim Simons
  Launched the Quant Revolution*. Portfolio.

---

## Appendix A -- Full data manifest

[Auto-generated by `data_pipeline.py` on each run; see `data/manifest.json`]

## Appendix B -- Reproduction code

Public GitHub repository: https://github.com/[your-handle]/regime-breaks
(Push the cleaned-up pipeline there before submission. Add a clear LICENSE
file -- MIT or Apache 2.0 -- so the code is properly open.)
