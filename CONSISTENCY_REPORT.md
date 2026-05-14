# Consistency Report — PAPER.md Internal Review

**Date:** 2026-05-14
**Reviewer:** Automated consistency pass (Phase 5, Step 1)
**File:** drafts/PAPER.md (493 lines)

---

## Category A: Numeric Consistency Across Sections

### S&P 500 -33.9% (COVID 2020)
Appears in: Abstract (L15), Section 1 (L25), Section 2.1 (L43), Section 2.2 (L53), Section 2.4 (L73), Section 3.7 (L160), Section 4.1 (L172), Section 4.2 (L178, L180, L184), Section 4.5 (L220, L226), Section 6.1 (L290), Section 6.4 (L318).
**Result: CONSISTENT.** All citations read "-33.9%".

### JPMorgan -42.5% (COVID 2020)
Appears in: Section 2.1 (L43), Section 4.2 (L178), Section 4.5 (L220), Section 6.1 (L290).
**Result: CONSISTENT.** All citations read "-42.5%".

### Bridgewater replicator -15.7% (COVID 2020)
Appears in: Abstract (L15), Section 1 (L27), Section 2.3 (L63), Section 3.4 (L125), Section 4.2 (L180, L182), Section 4.5 (L224), Section 5.2 (L248), Section 5.5 (L278), Section 6.1 (L290), Section 7.2 (L346).
**Result: CONSISTENT.** All citations read "-15.7%".

### Bridgewater replicator +0.9% (yen carry 2024)
Appears in: Abstract (L15), Section 1 (L27), Section 2.3 (L63), Section 5.2 (L248), Section 5.5 (L278), Section 6.1 (L292).
**Result: CONSISTENT.** All citations read "+0.9%".

### Correlation values: COVID 0.25→0.50, yen carry 0.37→0.44
Appears in: Abstract (L15), Section 1 (L27 — as "98%" and "19%"), Section 4.3 (L190), Section 5.3 (L254), Section 6.1 (L290, L292, L294), Section 8 (L370).
**Result: CONSISTENT.** All COVID citations read 0.25/0.50; all yen carry citations read 0.37/0.44. Percentage increases (98%, 19%) are consistent throughout.

### Regression p-values: AGG 0.006, HYG <0.001, MTUM 0.005
Appears in: Abstract (L15), Section 1 (L27), Section 4.4 (L204-206), Section 4.5 (L226 — MTUM only), Section 6.2 (L298), Section 7.3 (L354).
**Result: CONSISTENT.** All citations match.

### Two Sigma factor proxy -30.1% (COVID 2020)
Appears in: Section 2.4 (L73), Section 4.2 (L184), Section 4.5 (L226), Section 6.1 (L290).
**Result: CONSISTENT.**

### S&P 500 -6.1% (yen carry 2024)
Appears in: Section 2.1 (L43), Section 2.4 (L73), Section 3.7 (L160), Section 5.2 (L244, L246), Section 5.3 (L258), Section 5.5 (L274), Section 6.1 (L292), Section 6.4 (L318).
**Result: CONSISTENT.**

**Category A summary: 0 inconsistencies found.**

---

## Category B: Reference Consistency

### Body citations with corresponding References entry

| Citation in body | References entry | Status |
|-----------------|-----------------|--------|
| Brunnermeier and Pedersen (2009) | Yes | OK |
| Adrian and Brunnermeier (2016) | Yes | OK |
| Son (2017) | Yes | OK |
| MacKinlay (1997) | Yes | OK |
| Newey-West (1987) / Newey and West (1987) | Yes | OK |
| Corwin-Schultz (2012) / Corwin and Schultz (2012) | Yes | OK |
| Dalio (2017) | Yes | OK |
| Wigglesworth (2021) | Yes | OK |
| Patterson (2010) | Yes | OK |
| Duffie (2023) | Yes | OK |
| Goldberg (2020) | Yes | OK |
| Fleming and Ruela (2020) | Yes | OK |
| Bank for International Settlements (2024) / BIS (2024) | Yes | OK |
| FCA (2021) / Financial Conduct Authority (2021) | Yes | OK |
| FSOC (2014) / Financial Stability Oversight Council (2014) | Yes | OK |
| FSB (2017) / Financial Stability Board (2017) | Yes | OK |
| Acharya et al. (2017) | Yes | OK |
| BlackRock 10-K FY2025 | Yes | OK |
| JPMorgan 2024 Annual Report | Yes | OK |

### Body citations WITHOUT formal References entry — FIXED

| Citation in body | Location | Resolution |
|-----------------|----------|------------|
| "FT and Reuters, April 2020" | Section 2.3 (L61), Section 4.2 (L182) | **FIXED** — added to References under Journalism |
| "Bloomberg reported a loss of -9.4% (January 2023)" | Section 2.3 (L61) | **FIXED** — added to References under Journalism |
| "Hedgeweek's January 2025 reporting" | Section 2.4 (L69) | **FIXED** — added to References under Journalism |

### References entries NOT cited in body (orphans)

| References entry | Status |
|-----------------|--------|
| Federal Reserve Economic Data (FRED) | Cited in Section 3.2 as "FRED API" — OK (data source) |
| Yahoo Finance / yfinance | Cited in Section 3.2 — OK (data source) |

**No orphan references.**

**Category B summary: 3 missing reference entries found and FIXED.**

---

## Category C: Figure and Table Cross-References

### Figures referenced in text

| Text reference | Corresponding file | Status |
|---------------|-------------------|--------|
| Figure 0 and Table 0 (L125) | fig0_bridgewater_validation.png, table0_bridgewater_validation.csv | OK |
| Figure 2 COVID 2020 (L190) | fig2_corr_covid_2020.png | OK |
| Figure 1 COVID 2020 (L196) | fig1_drawdowns_covid_2020.png | OK |
| Figure 2 yen carry 2024 (L254) | fig2_corr_yen_carry_2024.png | OK |

### Figures that exist but are NOT referenced in text

| File | Note |
|------|------|
| fig0b_bridgewater_monthly.png | Supplementary; not cross-referenced |
| fig1_drawdowns_yen_carry_2024.png | Not cross-referenced (Section 5 has no explicit figure callout) |
| fig3_vol_breach_covid_2020.png | Not cross-referenced |
| fig3_vol_breach_yen_carry_2024.png | Not cross-referenced |
| fig5_cross_event_scatter.png | Not cross-referenced |

**FLAGGED for Arnav:** Five figures exist in outputs/ but are not called out in the text. These are available as supplementary material but should be explicitly referenced if they are to be included in the SSRN submission. No fix applied — awaiting author decision.

### Tables referenced in text

Table 0 (L125) → table0_bridgewater_validation.csv — OK
Tables 1-5 are not explicitly referenced by number in the paper body, but correspond to analyses described in Sections 4-6. The data they contain is cited by value throughout.

**Category C summary: 0 errors. 5 unreferenced figures flagged for author.**

---

## Category D: Voice and Tense

### Banned phrase scan
Searched for: "fundamentally", "transformative", "rapidly evolving", "no longer just", "core economic engine", "paradigm shift", "next-generation", "reshape", "revolutionize", "in today's world", "in an era of", "cutting-edge", "state of the art".

**Result: 0 banned phrases found.**

### Tense consistency
- Events described in past tense throughout (correct).
- Findings and interpretations in present tense ("The findings suggest...", "The result is bounded...") — consistent.
- Hypotheses stated in present/conditional tense ("should behave", "should break") — consistent.
- No tense drift detected.

### Voice
- Active voice predominates. Passive used appropriately for methodological description ("Standard errors are computed using...").
- No AI-signature prose detected.

**Category D summary: 0 issues.**

---

## Category E: Section Transitions

| Transition | Opening connects to previous close? | Status |
|-----------|-------------------------------------|--------|
| Abstract → Section 1 | N/A (separate) | OK |
| Section 1 → Section 2 | Section 1 ends: "Section 2 develops testable hypotheses..." Section 2 opens with JPMorgan's architectural claim. | OK — smooth handoff |
| Section 2 → Section 3 | Section 2 ends with Two Sigma testable hypothesis. Section 3 opens: "This paper uses a comparative case study design." | OK — natural transition from hypotheses to methodology |
| Section 3 → Section 4 | Section 3 ends with limitations. Section 4 opens with event context. | OK — methodology → first event |
| Section 4 → Section 5 | Section 4 ends: "all roads led to the same forced-selling dynamic." Section 5 opens with yen carry context. | OK — credit event → non-credit event |
| Section 5 → Section 6 | Section 5 ends with architectural verdicts. Section 6 opens: "The two-event design tests whether four institutional risk architectures fail in the same way or in different ways under stress." | OK — event results → cross-event synthesis |
| Section 6 → Section 7 | Section 6 ends: "Supervising the funding channel may be more important." Section 7 opens: "This study examines two events." | OK — implications → limitations |
| Section 7 → Section 8 | Section 7 ends with falsification scope discussion. Section 8 opens with summary of findings. | OK — limitations → conclusion |

**Category E summary: 0 abrupt transitions.**

---

## Summary

| Category | Issues found | Fixed | Flagged |
|----------|-------------|-------|---------|
| A: Numeric consistency | 0 | 0 | 0 |
| B: Reference consistency | 3 | 3 | 0 |
| C: Figure/table cross-refs | 0 | 0 | 5 (unreferenced figures) |
| D: Voice and tense | 0 | 0 | 0 |
| E: Section transitions | 0 | 0 | 0 |
| **Total** | **3** | **3** | **5** |

All three reference issues were resolved by adding formal entries to the References section of PAPER.md.

The five unreferenced figures are flagged for the author's decision on whether to add explicit callouts or treat them as supplementary material.
