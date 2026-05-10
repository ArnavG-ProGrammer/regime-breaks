"""
Analysis Layer
==============

Runs after data_pipeline.py. Produces the five core analyses for the paper:

  Analysis 1: Drawdown comparison table (per firm, per event)
  Analysis 2: Correlation regime-shift (pre / event / post heatmaps)
  Analysis 3: Realized vs target volatility breach analysis
  Analysis 4: Liquidity-dependency regression (Corwin-Schultz spread vs return)
  Analysis 5: Counterfactual / cross-event comparison synthesis

Each analysis writes a CSV (or two) to ./outputs/tables/ and a chart to
./outputs/figures/. All charts use a consistent academic style -- single-color
or two-color, no chartjunk, captions on every figure ready to drop into LaTeX.

Run AFTER data_pipeline.py:
    python analysis.py
"""

from __future__ import annotations

import json
import logging
import sys
from pathlib import Path

import numpy as np
import pandas as pd

try:
    import matplotlib.pyplot as plt
    import matplotlib as mpl
except ImportError as e:
    raise SystemExit("matplotlib required: pip install matplotlib") from e

try:
    import statsmodels.api as sm
except ImportError as e:
    raise SystemExit("statsmodels required: pip install statsmodels") from e


ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data"
CLEAN_DIR = DATA_DIR / "clean"
OUTPUT_DIR = ROOT / "outputs"
TABLES_DIR = OUTPUT_DIR / "tables"
FIGURES_DIR = OUTPUT_DIR / "figures"

for d in (TABLES_DIR, FIGURES_DIR):
    d.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)
log = logging.getLogger("analysis")

# Academic chart styling -- a serif font, restrained colors, white background.
mpl.rcParams.update({
    "font.family": "serif",
    "font.serif": ["Times New Roman", "DejaVu Serif"],
    "font.size": 10,
    "axes.labelsize": 10,
    "axes.titlesize": 11,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.grid": True,
    "grid.alpha": 0.3,
    "grid.linewidth": 0.5,
    "figure.dpi": 150,
    "savefig.dpi": 300,
    "savefig.bbox": "tight",
    "legend.frameon": False,
    "lines.linewidth": 1.4,
})

# Two-color palette: navy + rust. Distinguishable in print and for color-blind.
NAVY = "#1f3a5f"
RUST = "#c0392b"
GRAY = "#7f8c8d"
GOLD = "#b7950b"

EVENTS = {
    "covid_2020": {
        "label": "COVID drawdown (Feb-Mar 2020)",
        "pre_start": "2019-10-01",
        "event_start": "2020-02-19",
        "event_end": "2020-03-23",
        "post_end": "2020-08-01",
    },
    "yen_carry_2024": {
        "label": "Yen carry unwind (Aug 2024)",
        "pre_start": "2024-04-01",
        "event_start": "2024-07-31",
        "event_end": "2024-08-09",
        "post_end": "2024-12-13",
    },
}

# Map series tickers -> firm labels for tables/charts.
FIRM_LABELS = {
    "JPM": "JPMorgan (equity)",
    "JEPI": "JPMorgan (JEPI)",
    "JEPQ": "JPMorgan (JEPQ)",
    "BLK": "BlackRock (equity)",
    "IVV": "BlackRock (IVV proxy)",
    "AGG": "BlackRock (AGG proxy)",
    "TLT": "BlackRock (TLT proxy)",
    "Bridgewater_replicator": "Bridgewater (replicator)",
    "TwoSigma_factor_proxy": "Two Sigma (factor proxy)",
    "MTUM": "Two Sigma (momentum proxy)",
    "DBMF": "Two Sigma (managed-fut. proxy)",
    "^GSPC": "S&P 500 (benchmark)",
    "^N225": "Nikkei 225 (benchmark)",
    "^VIX": "VIX (level)",
}


# --------------------------------------------------------------------------
# Helpers
# --------------------------------------------------------------------------

def _load_returns() -> pd.DataFrame:
    p = CLEAN_DIR / "returns_daily.parquet"
    if not p.exists():
        raise SystemExit(
            f"No clean returns file at {p}. Run data_pipeline.py first."
        )
    df = pd.read_parquet(p)
    df.index = pd.to_datetime(df.index)
    return df.sort_index()


def _load_spreads() -> pd.DataFrame:
    p = CLEAN_DIR / "spreads_corwin_schultz.parquet"
    if not p.exists():
        log.warning(f"No spread file at {p}; Analysis 4 will skip.")
        return pd.DataFrame()
    df = pd.read_parquet(p)
    df.index = pd.to_datetime(df.index)
    return df.sort_index()


def _slice(df: pd.DataFrame, start: str, end: str) -> pd.DataFrame:
    return df.loc[start:end]


# --------------------------------------------------------------------------
# Analysis 1: Drawdown comparison
# --------------------------------------------------------------------------

def analysis_1_drawdowns(rets: pd.DataFrame) -> pd.DataFrame:
    """Per (series, event), compute peak-to-trough drawdown, vol, recovery."""
    rows = []
    for event_name, ev in EVENTS.items():
        for ticker in rets.columns:
            s = rets[ticker].dropna()
            in_event = _slice(s, ev["event_start"], ev["event_end"])
            pre = _slice(s, ev["pre_start"], ev["event_start"])
            full = _slice(s, ev["event_start"], ev["post_end"])
            if in_event.shape[0] < 3 or full.empty:
                continue

            wealth = (1.0 + np.expm1(full)).cumprod()
            wealth = wealth / wealth.iloc[0]  # normalize to 1.0 at event start
            dd = (wealth / wealth.cummax() - 1.0)
            max_dd = float(dd.min())
            max_dd_date = dd.idxmin()

            recovered = wealth.loc[max_dd_date:]
            recovery_idx = recovered[recovered >= 1.0].index
            ttr_days = (recovery_idx[0] - max_dd_date).days \
                if len(recovery_idx) else None

            rows.append({
                "event": event_name,
                "ticker": ticker,
                "label": FIRM_LABELS.get(ticker, ticker),
                "pre_vol_ann": float(pre.std() * np.sqrt(252)) if not pre.empty else np.nan,
                "event_vol_ann": float(in_event.std() * np.sqrt(252)),
                "max_drawdown": max_dd,
                "trough_date": str(max_dd_date.date()),
                "recovery_days": ttr_days,
                "event_total_return": float(np.expm1(in_event.sum())),
            })

    df = pd.DataFrame(rows)
    df.to_csv(TABLES_DIR / "table1_drawdowns.csv", index=False)
    log.info(f"Analysis 1: wrote table1_drawdowns.csv with {len(df)} rows")

    # Companion bar chart per event
    for event_name in EVENTS:
        sub = df[df["event"] == event_name].copy()
        focus = ["JPM", "IVV", "Bridgewater_replicator", "TwoSigma_factor_proxy",
                "^GSPC"]
        sub = sub[sub["ticker"].isin(focus)].set_index("label")
        if sub.empty:
            continue
        fig, ax = plt.subplots(figsize=(7, 4))
        ax.barh(sub.index, sub["max_drawdown"] * 100, color=NAVY)
        ax.set_xlabel("Max drawdown (%)")
        ax.set_title(
            f"Peak-to-trough drawdowns: {EVENTS[event_name]['label']}",
            loc="left",
        )
        ax.invert_yaxis()
        for i, v in enumerate(sub["max_drawdown"].values * 100):
            ax.text(v - 0.3, i, f"{v:.1f}%", va="center", ha="right",
                    color="white", fontsize=9)
        plt.savefig(FIGURES_DIR / f"fig1_drawdowns_{event_name}.png")
        plt.close(fig)

    return df


# --------------------------------------------------------------------------
# Analysis 2: Correlation regime-shift
# --------------------------------------------------------------------------

def analysis_2_correlations(rets: pd.DataFrame) -> dict:
    """For each event, compute pre / event / post correlation matrices for
    the four firm proxies + S&P 500. Save matrices to CSV and produce
    side-by-side heatmaps."""
    focus = [t for t in [
        "JPM", "IVV", "AGG", "TLT", "EEM", "HYG",
        "Bridgewater_replicator", "TwoSigma_factor_proxy",
        "MTUM", "VLUE", "DBMF",
        "^GSPC", "^N225"
    ] if t in rets.columns]

    out = {}
    for event_name, ev in EVENTS.items():
        pre = _slice(rets[focus], ev["pre_start"], ev["event_start"]).dropna()
        in_ev = _slice(rets[focus], ev["event_start"], ev["event_end"]).dropna()
        post = _slice(rets[focus], ev["event_end"], ev["post_end"]).dropna()

        for window_name, window in [("pre", pre), ("event", in_ev), ("post", post)]:
            if window.shape[0] < 5:
                continue
            corr = window.corr()
            corr.to_csv(TABLES_DIR / f"table2_corr_{event_name}_{window_name}.csv")

        # Headline metric: average off-diagonal correlation per window.
        def avg_off_diag(c: pd.DataFrame) -> float:
            arr = c.values.copy()
            np.fill_diagonal(arr, np.nan)
            return float(np.nanmean(arr))

        out[event_name] = {
            "pre_avg_corr": avg_off_diag(pre.corr()) if pre.shape[0] >= 5 else None,
            "event_avg_corr": avg_off_diag(in_ev.corr()) if in_ev.shape[0] >= 5 else None,
            "post_avg_corr": avg_off_diag(post.corr()) if post.shape[0] >= 5 else None,
        }

        # Side-by-side heatmaps
        fig, axes = plt.subplots(1, 3, figsize=(15, 5))
        for ax, (window_name, window) in zip(
            axes, [("Pre", pre), ("Event", in_ev), ("Post", post)]
        ):
            if window.shape[0] < 5:
                ax.text(0.5, 0.5, "insufficient data",
                        ha="center", va="center", transform=ax.transAxes)
                ax.set_title(f"{window_name} (n={window.shape[0]})", loc="left")
                continue
            c = window.corr()
            im = ax.imshow(c.values, vmin=-1, vmax=1, cmap="RdBu_r", aspect="auto")
            labels = [FIRM_LABELS.get(t, t) for t in c.columns]
            ax.set_xticks(range(len(labels)))
            ax.set_yticks(range(len(labels)))
            ax.set_xticklabels(labels, rotation=45, ha="right", fontsize=7)
            ax.set_yticklabels(labels, fontsize=7)
            ax.set_title(f"{window_name} (n={window.shape[0]} days)", loc="left")
        plt.suptitle(
            f"Correlation regime shift: {EVENTS[event_name]['label']}",
            x=0.02, ha="left", fontsize=11, y=1.02,
        )
        plt.tight_layout()
        cbar = fig.colorbar(im, ax=axes, shrink=0.7, pad=0.02)
        cbar.set_label("Pearson correlation")
        plt.savefig(FIGURES_DIR / f"fig2_corr_{event_name}.png")
        plt.close(fig)

    with (TABLES_DIR / "table2_avg_correlation_summary.json").open("w") as f:
        json.dump(out, f, indent=2)
    log.info(f"Analysis 2: average off-diagonal correlations: {out}")
    return out


# --------------------------------------------------------------------------
# Analysis 3: Realized vs target volatility breach
# --------------------------------------------------------------------------

def analysis_3_vol_breach(rets: pd.DataFrame) -> pd.DataFrame:
    """For each strategy, compare event-window realized vol to its long-run
    realized vol (the strategy's de facto vol target). Vol breach ratio > 3x
    is meaningful evidence of risk-model failure."""
    focus = [t for t in [
        "Bridgewater_replicator", "TwoSigma_factor_proxy",
        "JEPI", "JEPQ", "IVV", "AGG", "MTUM", "DBMF",
    ] if t in rets.columns]

    rows = []
    for ticker in focus:
        s = rets[ticker].dropna()
        if s.shape[0] < 252:
            continue
        long_run_vol = float(s.std() * np.sqrt(252))
        for event_name, ev in EVENTS.items():
            in_ev = _slice(s, ev["event_start"], ev["event_end"])
            if in_ev.shape[0] < 3:
                continue
            event_vol = float(in_ev.std() * np.sqrt(252))
            rows.append({
                "ticker": ticker,
                "label": FIRM_LABELS.get(ticker, ticker),
                "event": event_name,
                "long_run_vol_ann": long_run_vol,
                "event_vol_ann": event_vol,
                "breach_ratio": event_vol / long_run_vol if long_run_vol > 0 else np.nan,
            })
    df = pd.DataFrame(rows)
    df.to_csv(TABLES_DIR / "table3_vol_breach.csv", index=False)
    log.info(f"Analysis 3: wrote table3_vol_breach.csv ({len(df)} rows)")

    # Chart: breach ratio per strategy per event
    if not df.empty:
        for event_name in EVENTS:
            sub = df[df["event"] == event_name].sort_values("breach_ratio")
            if sub.empty:
                continue
            fig, ax = plt.subplots(figsize=(7, 4))
            colors = [RUST if r > 3 else NAVY for r in sub["breach_ratio"]]
            ax.barh(sub["label"], sub["breach_ratio"], color=colors)
            ax.axvline(1.0, color=GRAY, linestyle="--", linewidth=0.8,
                       label="long-run vol")
            ax.axvline(3.0, color=RUST, linestyle=":", linewidth=0.8,
                       label="3x breach threshold")
            ax.set_xlabel("Event-window vol / long-run vol (ratio)")
            ax.set_title(
                f"Volatility breach ratios: {EVENTS[event_name]['label']}",
                loc="left",
            )
            ax.legend(loc="lower right")
            plt.savefig(FIGURES_DIR / f"fig3_vol_breach_{event_name}.png")
            plt.close(fig)
    return df


# --------------------------------------------------------------------------
# Analysis 4: Liquidity dependency regression
# --------------------------------------------------------------------------

def analysis_4_liquidity_regression(
    rets: pd.DataFrame,
    spreads: pd.DataFrame,
) -> pd.DataFrame:
    """For each firm proxy, regress daily return on:
      - own lagged Corwin-Schultz spread (liquidity)
      - S&P return (market beta)
      - VIX change (vol-of-vol)
    Coefficient on lagged spread tests whether returns are explained by
    liquidity stress beyond market beta. Significant negative coefficient
    means the strategy is hurt when bid-ask spreads widen -- a hallmark of
    crowded / liquidity-fragile positioning."""
    if spreads.empty:
        log.warning("Spread file unavailable; skipping Analysis 4")
        return pd.DataFrame()

    focus = [t for t in ["IVV", "AGG", "TLT", "HYG", "MTUM", "DBMF",
                         "Bridgewater_replicator", "TwoSigma_factor_proxy"]
             if t in rets.columns]
    if "^GSPC" not in rets.columns or "^VIX" not in rets.columns:
        log.warning("Need ^GSPC and ^VIX for Analysis 4; skipping")
        return pd.DataFrame()

    sp = rets["^GSPC"].rename("sp500_ret")
    vix_chg = rets["^VIX"].rename("vix_ret")  # log returns of VIX level

    rows = []
    for ticker in focus:
        if ticker not in rets.columns:
            continue
        # Use IVV spread as a market-liquidity proxy when ticker has no spread
        if ticker in spreads.columns:
            sp_series = spreads[ticker].rename("own_spread_lag").shift(1)
        elif "IVV" in spreads.columns:
            sp_series = spreads["IVV"].rename("own_spread_lag").shift(1)
        else:
            continue

        df = pd.concat([rets[ticker].rename("ret"), sp, vix_chg, sp_series],
                       axis=1).dropna()
        if df.shape[0] < 250:
            continue

        X = df[["sp500_ret", "vix_ret", "own_spread_lag"]]
        X = sm.add_constant(X)
        y = df["ret"]
        model = sm.OLS(y, X).fit(cov_type="HAC", cov_kwds={"maxlags": 5})
        rows.append({
            "ticker": ticker,
            "label": FIRM_LABELS.get(ticker, ticker),
            "n_obs": int(df.shape[0]),
            "alpha_daily": float(model.params["const"]),
            "beta_sp500": float(model.params["sp500_ret"]),
            "beta_vix": float(model.params["vix_ret"]),
            "beta_spread_lag": float(model.params["own_spread_lag"]),
            "spread_lag_tstat": float(model.tvalues["own_spread_lag"]),
            "spread_lag_pvalue": float(model.pvalues["own_spread_lag"]),
            "r_squared": float(model.rsquared),
        })
    df_out = pd.DataFrame(rows)
    df_out.to_csv(TABLES_DIR / "table4_liquidity_regression.csv", index=False)
    log.info(f"Analysis 4: wrote table4_liquidity_regression.csv "
             f"({len(df_out)} rows)")
    return df_out


# --------------------------------------------------------------------------
# Analysis 4b: Liquidity regression BY EVENT WINDOW
# --------------------------------------------------------------------------

def analysis_4b_liquidity_regression_by_window(
    rets: pd.DataFrame,
    spreads: pd.DataFrame,
) -> pd.DataFrame:
    """Same specification as analysis_4 but restricted to the event window
    plus 30 trading days on each side. Tests whether the spread coefficient
    is significant within each event specifically — if significant in 2020
    but not 2024, that supports the credit-liquidity mechanism hypothesis."""
    if spreads.empty:
        log.warning("Spread file unavailable; skipping Analysis 4b")
        return pd.DataFrame()

    focus = [t for t in ["IVV", "AGG", "TLT", "HYG", "MTUM", "DBMF",
                         "Bridgewater_replicator", "TwoSigma_factor_proxy"]
             if t in rets.columns]
    if "^GSPC" not in rets.columns or "^VIX" not in rets.columns:
        log.warning("Need ^GSPC and ^VIX for Analysis 4b; skipping")
        return pd.DataFrame()

    sp = rets["^GSPC"].rename("sp500_ret")
    vix_chg = rets["^VIX"].rename("vix_ret")

    rows = []
    for event_name, ev in EVENTS.items():
        # Extend window by ~30 trading days on each side
        window_start = pd.Timestamp(ev["event_start"]) - pd.Timedelta(days=45)
        window_end = pd.Timestamp(ev["event_end"]) + pd.Timedelta(days=45)

        for ticker in focus:
            if ticker not in rets.columns:
                continue
            if ticker in spreads.columns:
                sp_series = spreads[ticker].rename("own_spread_lag").shift(1)
            elif "IVV" in spreads.columns:
                sp_series = spreads["IVV"].rename("own_spread_lag").shift(1)
            else:
                continue

            df = pd.concat([rets[ticker].rename("ret"), sp, vix_chg, sp_series],
                           axis=1).loc[window_start:window_end].dropna()
            if df.shape[0] < 20:
                continue

            X = df[["sp500_ret", "vix_ret", "own_spread_lag"]]
            X = sm.add_constant(X)
            y = df["ret"]
            # Use OLS with HAC; fewer lags for shorter window
            n_lags = min(5, max(1, df.shape[0] // 10))
            model = sm.OLS(y, X).fit(cov_type="HAC", cov_kwds={"maxlags": n_lags})
            rows.append({
                "event": event_name,
                "ticker": ticker,
                "label": FIRM_LABELS.get(ticker, ticker),
                "n_obs": int(df.shape[0]),
                "beta_sp500": float(model.params["sp500_ret"]),
                "beta_vix": float(model.params["vix_ret"]),
                "beta_spread_lag": float(model.params["own_spread_lag"]),
                "spread_lag_tstat": float(model.tvalues["own_spread_lag"]),
                "spread_lag_pvalue": float(model.pvalues["own_spread_lag"]),
                "r_squared": float(model.rsquared),
            })
    df_out = pd.DataFrame(rows)
    df_out.to_csv(TABLES_DIR / "table4b_liquidity_regression_by_window.csv", index=False)
    log.info(f"Analysis 4b: wrote table4b_liquidity_regression_by_window.csv "
             f"({len(df_out)} rows)")
    return df_out


# --------------------------------------------------------------------------
# Analysis 5: Cross-event synthesis
# --------------------------------------------------------------------------

def analysis_5_cross_event(t1: pd.DataFrame, t3: pd.DataFrame) -> pd.DataFrame:
    """Combine drawdown table (T1) with vol-breach table (T3) to produce the
    paper's headline cross-event synthesis: which architectures consistently
    breached vol target AND drew down hardest, vs. which broke in only one
    event. The two-event design is what makes this defensible -- single-event
    failure is luck; consistent two-event failure is architecture."""
    if t1.empty or t3.empty:
        return pd.DataFrame()

    pivot_dd = t1.pivot_table(
        index=["ticker", "label"],
        columns="event",
        values="max_drawdown",
    )
    pivot_breach = t3.pivot_table(
        index=["ticker", "label"],
        columns="event",
        values="breach_ratio",
    )
    merged = pivot_dd.join(
        pivot_breach,
        lsuffix="_drawdown",
        rsuffix="_volbreach",
    ).reset_index()
    merged.to_csv(TABLES_DIR / "table5_cross_event_synthesis.csv", index=False)
    log.info(f"Analysis 5: wrote table5_cross_event_synthesis.csv")

    # Scatter: drawdown in COVID vs drawdown in yen-carry
    if "covid_2020_drawdown" in merged.columns and "yen_carry_2024_drawdown" in merged.columns:
        plot_df = merged.dropna(
            subset=["covid_2020_drawdown", "yen_carry_2024_drawdown"]
        )
        if not plot_df.empty:
            fig, ax = plt.subplots(figsize=(6.5, 6.5))
            ax.scatter(
                plot_df["covid_2020_drawdown"] * 100,
                plot_df["yen_carry_2024_drawdown"] * 100,
                color=NAVY, s=50, alpha=0.8,
            )
            for _, row in plot_df.iterrows():
                ax.annotate(
                    row["label"],
                    (row["covid_2020_drawdown"] * 100,
                     row["yen_carry_2024_drawdown"] * 100),
                    fontsize=7, alpha=0.8, xytext=(4, 4),
                    textcoords="offset points",
                )
            ax.set_xlabel("Max drawdown, COVID 2020 (%)")
            ax.set_ylabel("Max drawdown, yen carry 2024 (%)")
            ax.set_title("Architecture stress: how the same strategies fared "
                         "in two different regime breaks", loc="left")
            ax.axhline(0, color="black", linewidth=0.5)
            ax.axvline(0, color="black", linewidth=0.5)
            plt.savefig(FIGURES_DIR / "fig5_cross_event_scatter.png")
            plt.close(fig)
    return merged


# --------------------------------------------------------------------------
# Main
# --------------------------------------------------------------------------

def main() -> None:
    log.info("Analysis layer starting")
    rets = _load_returns()
    spreads = _load_spreads()
    log.info(f"Loaded returns: {rets.shape}, spreads: {spreads.shape}")

    t1 = analysis_1_drawdowns(rets)
    t2 = analysis_2_correlations(rets)
    t3 = analysis_3_vol_breach(rets)
    t4 = analysis_4_liquidity_regression(rets, spreads)
    t4b = analysis_4b_liquidity_regression_by_window(rets, spreads)
    t5 = analysis_5_cross_event(t1, t3)

    summary = {
        "n_drawdown_rows": len(t1),
        "avg_correlations_by_event": t2,
        "n_volbreach_rows": len(t3),
        "n_regression_rows": len(t4),
        "n_regression_by_window_rows": len(t4b),
        "n_synthesis_rows": len(t5),
    }
    with (OUTPUT_DIR / "analysis_summary.json").open("w") as f:
        json.dump(summary, f, indent=2, default=str)
    log.info(f"Analysis complete. Summary: {summary}")
    log.info(f"Tables: {TABLES_DIR}")
    log.info(f"Figures: {FIGURES_DIR}")


if __name__ == "__main__":
    main()
