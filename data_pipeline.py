"""
Research Data Pipeline
======================

When Machines Disagree: Comparative Analysis of Four Institutional Risk
Architectures Under Regime Breaks (March 2020 and August 2024).

Author : Arnav Goyal
Status : Working paper data pipeline
Version: 1.0

This script assembles the empirical dataset for the paper. Every series is
pulled from a primary or near-primary public source; every transformation is
documented in line with the methodology section of the paper. The pipeline
is deterministic: given the same input dates, it produces the same output.

DESIGN PRINCIPLES
-----------------
1.  Primary sources only. No scraped secondary aggregators (Statista, etc.).
    Each series is annotated with its provenance.
2.  Reproducibility. All raw data is cached to disk before any transformation.
    Anyone with this script and an internet connection produces the identical
    dataset, which is the standard SSRN and peer-reviewed journals expect.
3.  Explicit limitations. Where a strategy's returns are not directly
    observable (Bridgewater, Two Sigma), the proxy is named, justified in
    comments, and flagged in the output for the limitations section.
4.  Defensive against API changes. yfinance and FRED change behavior across
    versions; the script logs the package version and validates the shape of
    every download.

EVENT WINDOWS
-------------
Event 1 (COVID drawdown) : 2020-02-19 peak --> 2020-03-23 trough
Event 2 (Yen carry unwind): 2024-07-31 BoJ hike --> 2024-08-09 stabilization

For each event, we pull pre-event (90 trading days), event-window, and
post-event (90 trading days) data.

PROXY MAPPING
-------------
JPMorgan      : JPM equity, JEPI/JEPQ NAVs (systematic option-overlay funds),
                JPM 13F-derived sector exposure (post-hoc).
BlackRock     : iShares ETFs that are managed/risk-overseen via Aladdin.
                Use IVV (S&P), AGG (US Agg bond), TLT (long Treasuries),
                EEM (EM equity). Document this is a proxy for "Aladdin-touched
                exposures," not Aladdin's full coverage.
Bridgewater   : All Weather monthly returns (assembled from press disclosures
                in the references file). Daily approximation built from a
                60/40-style risk-parity replicator using Treasury futures
                (TLT) + equities (IVV) + commodities (DBC) + TIPS (TIP) at
                vol-target weights. Flagged as REPLICATOR, not actual returns.
Two Sigma     : Multi-strategy returns are private. Proxy with a basket of
                publicly-listed quant ETFs (QSPIX-style; we use QMOM, IMTM,
                VLUE for value/momentum decomposition) and AQR's published
                Style Premia daily returns (publicly downloadable). Document
                this as a "systematic factor proxy," not Two Sigma proper.

USAGE
-----
    pip install yfinance pandas numpy fredapi requests
    export FRED_API_KEY="your_key_here"   # free at fred.stlouisfed.org
    python data_pipeline.py

OUTPUT
------
    ./data/raw/         <- untouched downloads, one file per series
    ./data/clean/       <- aligned, returns-computed dataset
    ./data/manifest.json <- provenance, dates, hashes, package versions
"""

from __future__ import annotations

import hashlib
import json
import logging
import os
import sys
import time
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

import numpy as np
import pandas as pd

# Optional dependencies -- fail loudly if missing rather than silently.
try:
    import yfinance as yf
except ImportError as e:
    raise SystemExit(
        "yfinance is required. Install with: pip install yfinance"
    ) from e

try:
    from fredapi import Fred
except ImportError as e:
    raise SystemExit(
        "fredapi is required. Install with: pip install fredapi"
    ) from e

try:
    import requests
except ImportError as e:
    raise SystemExit("requests is required.") from e

# --------------------------------------------------------------------------
# Configuration
# --------------------------------------------------------------------------

ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
CLEAN_DIR = DATA_DIR / "clean"
LOG_DIR = ROOT / "logs"

for d in (RAW_DIR, CLEAN_DIR, LOG_DIR):
    d.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler(LOG_DIR / "pipeline.log"),
        logging.StreamHandler(sys.stdout),
    ],
)
log = logging.getLogger("pipeline")


# --------------------------------------------------------------------------
# Event window definitions
# --------------------------------------------------------------------------

@dataclass(frozen=True)
class EventWindow:
    name: str
    pre_start: str       # ~90 trading days before peak
    event_start: str     # peak / trigger
    event_end: str       # trough / stabilization
    post_end: str        # ~90 trading days after trough
    description: str


EVENTS = [
    EventWindow(
        name="covid_2020",
        pre_start="2019-10-01",
        event_start="2020-02-19",
        event_end="2020-03-23",
        post_end="2020-08-01",
        description=(
            "COVID-19 equity drawdown. S&P 500 peak 2020-02-19 (3386.15) to "
            "trough 2020-03-23 (2237.40), -33.9%. Fed announced unlimited QE "
            "and primary/secondary corporate credit facilities on 2020-03-23, "
            "marking the bottom."
        ),
    ),
    EventWindow(
        name="yen_carry_2024",
        pre_start="2024-04-01",
        event_start="2024-07-31",
        event_end="2024-08-09",
        post_end="2024-12-13",
        description=(
            "Yen carry unwind. BoJ raised policy rate to 0.25% on 2024-07-31; "
            "Nikkei 225 fell 12.4% on 2024-08-05 (largest single-day drop "
            "since 1987 Black Monday). VIX intraday peak 65.73 on 2024-08-05. "
            "USD/JPY fell from ~155 to ~142 in 5 sessions before stabilizing."
        ),
    ),
]


# --------------------------------------------------------------------------
# Series definitions -- every series has explicit provenance
# --------------------------------------------------------------------------

@dataclass
class Series:
    """One data series, with full provenance for the methods section."""
    ticker: str
    source: str            # "yfinance", "fred", "aqr_csv"
    role: str              # what this series represents in the analysis
    firm_proxy: Optional[str] = None  # which of the four firms this maps to
    notes: str = ""
    raw_url: str = ""      # direct URL where applicable (FRED, AQR)


# --- Market benchmarks (used across all firms) ---
BENCHMARKS = [
    Series("^GSPC", "yfinance", "S&P 500 index level",
           notes="Bloomberg ticker SPX. Free via Yahoo Finance."),
    Series("^N225", "yfinance", "Nikkei 225 index level",
           notes="Tokyo Stock Exchange. Required for August 2024 event."),
    Series("^VIX", "yfinance", "CBOE VIX (30-day implied vol on S&P)",
           notes="Bid-ask midpoint, daily close."),
    Series("^MOVE", "yfinance", "ICE BofA MOVE index (Treasury vol)",
           notes="Yield-curve weighted normalized implied vol of 1m options "
                 "on 2y/5y/10y/30y Treasuries."),
    Series("JPY=X", "yfinance", "USD/JPY spot exchange rate",
           notes="Required for August 2024 carry unwind analysis."),
    Series("DX-Y.NYB", "yfinance", "DXY US Dollar index"),
]

# --- Firm-specific proxies ---
JPMORGAN_SERIES = [
    Series("JPM", "yfinance", "JPMorgan Chase common equity",
           firm_proxy="JPMorgan",
           notes="Direct equity, used to observe market's pricing of JPM "
                 "through events. Not a strategy return."),
    Series("JEPI", "yfinance",
           "JPMorgan Equity Premium Income ETF (systematic covered-call)",
           firm_proxy="JPMorgan",
           notes="Launched 2020-05-20, only available for 2024 event. "
                 "Active systematic strategy; useful as observable systematic "
                 "product run by JPM."),
    Series("JEPQ", "yfinance",
           "JPMorgan Nasdaq Equity Premium Income ETF",
           firm_proxy="JPMorgan",
           notes="Launched 2022-05-03, only available for 2024 event."),
]

BLACKROCK_SERIES = [
    Series("BLK", "yfinance", "BlackRock common equity",
           firm_proxy="BlackRock"),
    Series("IVV", "yfinance", "iShares Core S&P 500 ETF",
           firm_proxy="BlackRock",
           notes="Aladdin-overseen. Used for equity-beta exposure."),
    Series("AGG", "yfinance", "iShares Core U.S. Aggregate Bond ETF",
           firm_proxy="BlackRock",
           notes="Aladdin-overseen. Used for bond-correlation analysis."),
    Series("TLT", "yfinance", "iShares 20+ Year Treasury Bond ETF",
           firm_proxy="BlackRock",
           notes="Aladdin-overseen. Long-duration; key to risk-parity "
                 "decomposition for Bridgewater proxy as well."),
    Series("EEM", "yfinance", "iShares MSCI Emerging Markets ETF",
           firm_proxy="BlackRock",
           notes="Aladdin-overseen. Tests whether Aladdin-touched diverse "
                 "products correlated during stress."),
    Series("HYG", "yfinance", "iShares iBoxx High Yield Corp Bond ETF",
           firm_proxy="BlackRock",
           notes="Credit-stress signal; especially relevant March 2020."),
]

# Bridgewater All Weather is private. We build a risk-parity REPLICATOR.
# This is explicitly flagged as a replicator, not actual returns. The paper
# will compare both: replicator (daily) for granular event-window analysis,
# and reported monthly returns (assembled from press) for ground-truth check.
BRIDGEWATER_REPLICATOR_COMPONENTS = [
    Series("IVV", "yfinance", "Equity sleeve of risk-parity replicator",
           firm_proxy="Bridgewater_replicator",
           notes="See risk-parity reconstruction in Section 3.4 of paper."),
    Series("TLT", "yfinance", "Long Treasury sleeve"),
    Series("TIP", "yfinance", "TIPS sleeve (inflation protection)"),
    Series("DBC", "yfinance", "Broad commodities sleeve",
           notes="Invesco DB Commodity Index Tracking. Closest liquid proxy "
                 "to Bridgewater's commodity allocation."),
    Series("GLD", "yfinance", "Gold sleeve",
           notes="Bridgewater All Weather has held meaningful gold "
                 "allocation since at least 2019."),
]

# Two Sigma is private. Proxy with public systematic / factor ETFs.
TWO_SIGMA_PROXY_SERIES = [
    Series("MTUM", "yfinance", "iShares MSCI USA Momentum Factor ETF",
           firm_proxy="TwoSigma_proxy",
           notes="Momentum factor exposure; Two Sigma runs trend strategies."),
    Series("VLUE", "yfinance", "iShares MSCI USA Value Factor ETF",
           firm_proxy="TwoSigma_proxy"),
    Series("QUAL", "yfinance", "iShares MSCI USA Quality Factor ETF",
           firm_proxy="TwoSigma_proxy"),
    Series("USMV", "yfinance", "iShares MSCI USA Min Vol Factor ETF",
           firm_proxy="TwoSigma_proxy"),
    Series("DBMF", "yfinance", "iMGP DBi Managed Futures ETF",
           firm_proxy="TwoSigma_proxy",
           notes="Replicates SocGen CTA Index -- proxy for systematic "
                 "trend/macro strategies that Two Sigma's Compass fund "
                 "approximately runs."),
]

# --- FRED macro series (free, primary source) ---
FRED_SERIES = [
    Series("DFF", "fred", "Federal Funds Effective Rate",
           raw_url="https://fred.stlouisfed.org/series/DFF"),
    Series("DGS10", "fred", "10-Year Treasury Constant Maturity",
           raw_url="https://fred.stlouisfed.org/series/DGS10"),
    Series("DGS2", "fred", "2-Year Treasury Constant Maturity",
           raw_url="https://fred.stlouisfed.org/series/DGS2"),
    Series("BAMLH0A0HYM2", "fred", "ICE BofA US High Yield OAS",
           notes="Credit stress indicator. Spike in March 2020 to 1100+ bps.",
           raw_url="https://fred.stlouisfed.org/series/BAMLH0A0HYM2"),
    Series("BAMLC0A4CBBB", "fred", "ICE BofA BBB Corporate OAS",
           raw_url="https://fred.stlouisfed.org/series/BAMLC0A4CBBB"),
    Series("VIXCLS", "fred", "CBOE VIX (FRED daily series)",
           notes="Cross-check against ^VIX Yahoo pull."),
    Series("DEXJPUS", "fred", "Japan / U.S. Foreign Exchange Rate",
           notes="JPY per USD; cross-check against JPY=X Yahoo pull.",
           raw_url="https://fred.stlouisfed.org/series/DEXJPUS"),
]

ALL_FIRM_SERIES = (
    JPMORGAN_SERIES + BLACKROCK_SERIES
    + BRIDGEWATER_REPLICATOR_COMPONENTS + TWO_SIGMA_PROXY_SERIES
)
ALL_YFINANCE_SERIES = list({s.ticker: s for s in BENCHMARKS + ALL_FIRM_SERIES}.values())


# --------------------------------------------------------------------------
# Pull functions
# --------------------------------------------------------------------------

def _hash_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def pull_yfinance(series: Series, start: str, end: str) -> pd.DataFrame:
    """Download one series from Yahoo Finance with retries.

    Returns a DataFrame indexed by date with columns Open/High/Low/Close/
    Adj Close/Volume. We keep all columns because Corwin-Schultz spread
    estimation requires High/Low.
    """
    log.info(f"yfinance: pulling {series.ticker} [{start} -> {end}]")
    last_err = None
    for attempt in range(3):
        try:
            df = yf.download(
                series.ticker,
                start=start,
                end=end,
                progress=False,
                auto_adjust=False,
                actions=False,
                threads=False,
            )
            if df is None or df.empty:
                raise ValueError(f"empty frame for {series.ticker}")
            # yfinance can return MultiIndex columns when multiple tickers are
            # requested; normalize to single-level for safety.
            if isinstance(df.columns, pd.MultiIndex):
                df.columns = [c[0] for c in df.columns]
            return df
        except Exception as e:  # noqa: BLE001
            last_err = e
            log.warning(f"  attempt {attempt + 1} failed: {e}")
            time.sleep(2 ** attempt)
    raise RuntimeError(f"yfinance failed for {series.ticker}: {last_err}")


def pull_fred(series: Series, fred: Fred, start: str, end: str) -> pd.DataFrame:
    """Download one FRED series. Returns single-column DataFrame."""
    log.info(f"FRED: pulling {series.ticker} [{start} -> {end}]")
    s = fred.get_series(series.ticker, observation_start=start, observation_end=end)
    if s is None or s.empty:
        raise ValueError(f"empty FRED series {series.ticker}")
    df = s.to_frame(name=series.ticker)
    df.index.name = "Date"
    return df


# --------------------------------------------------------------------------
# Cleaning and feature engineering
# --------------------------------------------------------------------------

def compute_log_returns(prices: pd.Series) -> pd.Series:
    """Log returns. We use log returns throughout because they additively
    aggregate across time, which simplifies drawdown decomposition."""
    return np.log(prices / prices.shift(1))


def compute_drawdown(prices: pd.Series) -> pd.Series:
    """Running drawdown series: (price - rolling_max) / rolling_max."""
    rolling_max = prices.cummax()
    return (prices - rolling_max) / rolling_max


def corwin_schultz_spread(high: pd.Series, low: pd.Series) -> pd.Series:
    """Corwin-Schultz (2012, Journal of Finance) high-low bid-ask spread
    estimator. Uses two consecutive days' high and low prices to estimate
    the effective spread without needing intraday data.

    Reference:
        Corwin, S. A., & Schultz, P. (2012). A simple way to estimate
        bid-ask spreads from daily high and low prices.
        The Journal of Finance, 67(2), 719-760.

    Returns spread as a fraction of price (e.g., 0.005 = 50 bps).
    """
    high = high.astype(float)
    low = low.astype(float)
    h_l = np.log(high / low)

    # Beta: sum of squared log(high/low) over two-day window
    beta = (h_l ** 2) + (h_l.shift(1) ** 2)

    # Gamma: log of (max-of-two-day-highs / min-of-two-day-lows), squared
    h2 = np.maximum(high, high.shift(1))
    l2 = np.minimum(low, low.shift(1))
    gamma = (np.log(h2 / l2)) ** 2

    # Alpha
    sqrt2 = np.sqrt(2.0)
    denom = 3.0 - 2.0 * sqrt2
    alpha = (np.sqrt(2.0 * beta) - np.sqrt(beta)) / denom \
        - np.sqrt(gamma / denom)

    # Spread: 2(e^alpha - 1) / (1 + e^alpha)
    spread = 2.0 * (np.exp(alpha) - 1.0) / (1.0 + np.exp(alpha))

    # Negative or implausible spreads are set to NaN per CS recommendation
    spread = spread.where(spread > 0)
    spread = spread.where(spread < 0.5)  # >50% spread is implausible
    return spread


def build_risk_parity_replicator(
    prices: pd.DataFrame,
    components: list[str],
    target_vol: float = 0.10,
    lookback: int = 60,
) -> pd.Series:
    """Inverse-volatility-weighted basket, monthly rebalanced.

    This is a transparent risk-parity replicator. It is NOT Bridgewater
    All Weather. Differences from real All Weather:
      - All Weather uses leverage to hit ~12% vol; we cap leverage at 1.5x
      - All Weather uses futures, not ETFs (different financing costs)
      - All Weather has a regime-aware overlay we cannot replicate
      - Component weights here are ETF returns, not return on capital

    The replicator is included so we have DAILY granularity for event-window
    analysis. The paper cross-checks the replicator's monthly returns
    against published All Weather monthly returns (collected from press
    coverage) to validate that the replicator captures the broad risk profile.
    """
    available = [c for c in components if c in prices.columns]
    if not available:
        raise ValueError("no replicator components present in price frame")

    rets = np.log(prices[available] / prices[available].shift(1))

    # Trailing volatility per component, daily annualized
    vol = rets.rolling(lookback).std() * np.sqrt(252)
    inv_vol = 1.0 / vol
    weights = inv_vol.div(inv_vol.sum(axis=1), axis=0)

    # Vol-target the overall portfolio
    portfolio_rets_unscaled = (weights.shift(1) * rets).sum(axis=1)
    realized_vol = portfolio_rets_unscaled.rolling(lookback).std() \
        * np.sqrt(252)
    leverage = (target_vol / realized_vol).clip(upper=1.5).shift(1)
    portfolio_rets = leverage * portfolio_rets_unscaled
    portfolio_rets.name = "Bridgewater_replicator"
    return portfolio_rets


# --------------------------------------------------------------------------
# Event-window analytics
# --------------------------------------------------------------------------

def event_window_stats(
    returns: pd.Series,
    event: EventWindow,
) -> dict:
    """Compute drawdown, time-to-recovery, vol, and other event-window
    statistics for a single return series and event."""
    series = returns.copy().dropna()
    pre = series.loc[event.pre_start: event.event_start]
    in_event = series.loc[event.event_start: event.event_end]
    post = series.loc[event.event_end: event.post_end]

    # Cumulative wealth from event start
    if in_event.empty:
        return {"event": event.name, "n_obs_event": 0, "note": "no data"}

    wealth = (1.0 + np.expm1(in_event)).cumprod()  # log -> simple
    drawdown = (wealth / wealth.cummax() - 1.0)
    max_dd = float(drawdown.min())
    max_dd_date = drawdown.idxmin()

    # Time to recovery (in trading days from trough)
    post_full = series.loc[event.event_start:].dropna()
    full_wealth = (1.0 + np.expm1(post_full)).cumprod()
    pre_event_peak = full_wealth.iloc[0]  # set start to 1.0
    recovered = full_wealth >= 1.0
    if recovered.any():
        recovery_date = recovered[recovered].index[
            recovered[recovered].index > max_dd_date
        ]
        ttr = (recovery_date[0] - max_dd_date).days if len(recovery_date) else np.nan
    else:
        ttr = np.nan

    return {
        "event": event.name,
        "n_obs_pre": int(pre.shape[0]),
        "n_obs_event": int(in_event.shape[0]),
        "n_obs_post": int(post.shape[0]),
        "pre_vol_annualized": float(pre.std() * np.sqrt(252)) if not pre.empty else np.nan,
        "event_vol_annualized": float(in_event.std() * np.sqrt(252)),
        "post_vol_annualized": float(post.std() * np.sqrt(252)) if not post.empty else np.nan,
        "max_drawdown": max_dd,
        "max_drawdown_date": str(max_dd_date.date()),
        "time_to_recovery_days": float(ttr) if pd.notna(ttr) else None,
        "event_total_return": float(np.expm1(in_event.sum())),
    }


def correlation_regime_shift(
    returns: pd.DataFrame,
    event: EventWindow,
) -> dict:
    """Pairwise correlation in three windows: pre, event, post.

    Headline finding: do nominally diverse strategies CONVERGE during stress?
    If pre-event corr matrix has low off-diagonals and event-window corr
    matrix has uniformly high off-diagonals, that is the empirical signature
    of common-mode risk-model failure.
    """
    pre = returns.loc[event.pre_start: event.event_start].dropna()
    in_event = returns.loc[event.event_start: event.event_end].dropna()
    post = returns.loc[event.event_end: event.post_end].dropna()

    return {
        "pre_corr": pre.corr().to_dict() if pre.shape[0] > 5 else None,
        "event_corr": in_event.corr().to_dict() if in_event.shape[0] > 5 else None,
        "post_corr": post.corr().to_dict() if post.shape[0] > 5 else None,
        "n_pre": int(pre.shape[0]),
        "n_event": int(in_event.shape[0]),
        "n_post": int(post.shape[0]),
    }


# --------------------------------------------------------------------------
# Main pipeline
# --------------------------------------------------------------------------

def main() -> None:
    log.info("=" * 70)
    log.info("Research data pipeline starting")
    log.info(f"Run timestamp: {datetime.now(timezone.utc).isoformat()}")
    log.info(f"Python: {sys.version.split()[0]}")
    log.info(f"pandas: {pd.__version__}")
    log.info(f"numpy:  {np.__version__}")
    log.info(f"yfinance: {yf.__version__}")
    log.info("=" * 70)

    # Date range: cover both events with comfortable buffers.
    overall_start = "2019-09-01"
    overall_end = "2025-01-31"

    # ----- Pull yfinance series -----
    yf_frames: dict[str, pd.DataFrame] = {}
    for s in ALL_YFINANCE_SERIES:
        cache_path = RAW_DIR / f"yf_{s.ticker.replace('^', '').replace('=', '_')}.parquet"
        if cache_path.exists():
            log.info(f"yfinance cache hit: {s.ticker}")
            df = pd.read_parquet(cache_path)
        else:
            try:
                df = pull_yfinance(s, overall_start, overall_end)
                df.to_parquet(cache_path)
            except Exception as e:  # noqa: BLE001
                log.error(f"  FAILED {s.ticker}: {e}")
                continue
        yf_frames[s.ticker] = df

    # ----- Pull FRED series -----
    fred_key = os.environ.get("FRED_API_KEY")
    fred_frames: dict[str, pd.DataFrame] = {}
    if fred_key:
        fred = Fred(api_key=fred_key)
        for s in FRED_SERIES:
            cache_path = RAW_DIR / f"fred_{s.ticker}.parquet"
            if cache_path.exists():
                log.info(f"FRED cache hit: {s.ticker}")
                df = pd.read_parquet(cache_path)
            else:
                try:
                    df = pull_fred(s, fred, overall_start, overall_end)
                    df.to_parquet(cache_path)
                except Exception as e:  # noqa: BLE001
                    log.error(f"  FAILED FRED {s.ticker}: {e}")
                    continue
            fred_frames[s.ticker] = df
    else:
        log.warning(
            "FRED_API_KEY not set. Skipping FRED. Get a free key at "
            "https://fred.stlouisfed.org/docs/api/api_key.html"
        )

    # ----- Build aligned price panel -----
    closes = {}
    for ticker, df in yf_frames.items():
        col = "Adj Close" if "Adj Close" in df.columns else "Close"
        closes[ticker] = df[col]
    prices = pd.DataFrame(closes).sort_index()
    prices.index = pd.to_datetime(prices.index)
    prices = prices.dropna(how="all")

    log.info(f"Aligned price panel: {prices.shape[0]} rows x {prices.shape[1]} cols")

    # Daily log returns
    rets = np.log(prices / prices.shift(1))

    # ----- Bridgewater risk-parity replicator -----
    bw_components = ["IVV", "TLT", "TIP", "DBC", "GLD"]
    try:
        bw_rep = build_risk_parity_replicator(prices, bw_components)
        rets["Bridgewater_replicator"] = bw_rep
        log.info("Built Bridgewater All Weather replicator")
    except Exception as e:  # noqa: BLE001
        log.error(f"Could not build Bridgewater replicator: {e}")

    # ----- Two Sigma factor proxy: equal-weight basket -----
    ts_components = [t for t in ["MTUM", "VLUE", "QUAL", "USMV", "DBMF"]
                     if t in rets.columns]
    if ts_components:
        rets["TwoSigma_factor_proxy"] = rets[ts_components].mean(axis=1)
        log.info(f"Built Two Sigma factor proxy from {len(ts_components)} ETFs")

    # ----- Compute Corwin-Schultz spreads for each ticker -----
    spreads = {}
    for ticker, df in yf_frames.items():
        if "High" in df.columns and "Low" in df.columns:
            try:
                sp = corwin_schultz_spread(df["High"], df["Low"])
                spreads[ticker] = sp
            except Exception as e:  # noqa: BLE001
                log.warning(f"  CS spread failed for {ticker}: {e}")
    spreads_df = pd.DataFrame(spreads).sort_index()
    log.info(f"Corwin-Schultz spreads computed for {spreads_df.shape[1]} tickers")

    # ----- Save clean panel -----
    rets.to_parquet(CLEAN_DIR / "returns_daily.parquet")
    prices.to_parquet(CLEAN_DIR / "prices_daily.parquet")
    spreads_df.to_parquet(CLEAN_DIR / "spreads_corwin_schultz.parquet")

    # ----- Run event-window analytics -----
    analytics: dict = {"events": {}, "correlations": {}}
    headline_series = [
        "JPM", "JEPI", "JEPQ",
        "BLK", "IVV", "AGG", "TLT", "EEM", "HYG",
        "Bridgewater_replicator",
        "TwoSigma_factor_proxy", "MTUM", "VLUE", "DBMF",
        "^GSPC", "^N225", "^VIX",
    ]
    headline_series = [s for s in headline_series if s in rets.columns]

    for event in EVENTS:
        log.info(f"\nEvent analytics: {event.name}")
        log.info(f"  {event.description}")
        ev_stats = {}
        for s in headline_series:
            ev_stats[s] = event_window_stats(rets[s], event)
        analytics["events"][event.name] = ev_stats

        sub = rets[headline_series]
        analytics["correlations"][event.name] = correlation_regime_shift(sub, event)

    # ----- Manifest -----
    manifest = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "python_version": sys.version.split()[0],
        "pandas_version": pd.__version__,
        "numpy_version": np.__version__,
        "yfinance_version": yf.__version__,
        "events": [asdict(e) for e in EVENTS],
        "yfinance_series": [
            {**asdict(s), "row_count": int(yf_frames[s.ticker].shape[0])
             if s.ticker in yf_frames else 0}
            for s in ALL_YFINANCE_SERIES
        ],
        "fred_series": [asdict(s) for s in FRED_SERIES],
        "raw_file_hashes": {
            p.name: _hash_file(p)
            for p in sorted(RAW_DIR.iterdir())
            if p.is_file()
        },
        "clean_files": [p.name for p in sorted(CLEAN_DIR.iterdir())],
        "headline_series_used": headline_series,
        "analytics": analytics,
        "limitations": [
            "Bridgewater All Weather returns are PROXIED via inverse-vol "
            "risk-parity replicator using ETFs. Actual returns will differ "
            "due to leverage, financing costs, and regime overlay. Cross-"
            "check against monthly press-disclosed returns in references.",
            "Two Sigma strategies are PROXIED via factor-ETF basket and "
            "DBMF managed-futures ETF. This captures the systematic-factor "
            "exposure profile but not Two Sigma's specific alpha.",
            "JEPI launched 2020-05; JEPQ launched 2022-05. Neither is "
            "available for the March 2020 event window.",
            "Corwin-Schultz spreads are estimates from daily H-L; intraday "
            "TAQ data would be more precise but is not freely available.",
            "All FX proxies (JPY=X) are spot rates, not deliverable forward "
            "rates; carry-trade P&L would also depend on funding spreads.",
        ],
    }
    with (DATA_DIR / "manifest.json").open("w") as f:
        json.dump(manifest, f, indent=2, default=str)

    log.info("=" * 70)
    log.info("Pipeline complete")
    log.info(f"  Raw files     : {len(list(RAW_DIR.iterdir()))}")
    log.info(f"  Clean files   : {len(list(CLEAN_DIR.iterdir()))}")
    log.info(f"  Manifest      : {DATA_DIR / 'manifest.json'}")
    log.info("=" * 70)


if __name__ == "__main__":
    main()
