# SSRN Submission Package

**Paper:** "When Machines Disagree: A Comparative Analysis of Four Institutional Risk Architectures Under Regime Breaks (March 2020 and August 2024)"

**Author:** Arnav Goyal, Ahlcon International School, New Delhi

## Contents

- **paper.md** — Full paper in Markdown format (master source document). Convert to DOCX or PDF using pandoc for SSRN upload.
- **figures/** — Six PNG figures referenced in the paper:
  - `fig0_bridgewater_validation.png` — Bridgewater replicator validation against reported returns
  - `fig1_drawdowns_covid_2020.png` — Strategy drawdowns during COVID 2020
  - `fig1_drawdowns_yen_carry_2024.png` — Strategy drawdowns during yen carry 2024
  - `fig2_corr_covid_2020.png` — Correlation heatmaps for COVID 2020 (pre/event/post)
  - `fig2_corr_yen_carry_2024.png` — Correlation heatmaps for yen carry 2024 (pre/event/post)
  - `fig5_cross_event_scatter.png` — Cross-event drawdown scatter
- **tables/** — Six data files supporting the paper's empirical claims (CSV and JSON formats)
- **SSRN_ABSTRACT.txt** — Condensed abstract for the SSRN submission form (<1000 characters)
- **SSRN_KEYWORDS.txt** — Keywords for the SSRN form
- **SSRN_JEL_CODES.txt** — JEL classification codes
- **REPRODUCTION.md** — Step-by-step guide to reproducing all results from the public GitHub repository

## Conversion to DOCX/PDF

```
pandoc paper.md -o paper.docx -V geometry:margin=1in
pandoc paper.md -o paper.pdf --pdf-engine=xelatex -V geometry:margin=1in -V fontsize=11pt
```

Requires pandoc (https://pandoc.org/) and, for PDF, a LaTeX distribution.
