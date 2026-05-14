# Reproduction Guide

The complete data pipeline and analysis code for this paper are publicly available at [https://github.com/ArnavG-ProGrammer/regime-breaks](https://github.com/ArnavG-ProGrammer/regime-breaks). All Python package versions are pinned in `requirements.txt` to ensure reproducibility.

## Steps to reproduce

1. Clone the repository:
   ```
   git clone https://github.com/ArnavG-ProGrammer/regime-breaks.git
   cd regime-breaks
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Obtain a free FRED API key at [https://fred.stlouisfed.org/docs/api/api_key.html](https://fred.stlouisfed.org/docs/api/api_key.html).

4. Set the environment variable:
   ```
   export FRED_API_KEY=your_key_here
   ```

5. Run the data pipeline (downloads all price and macro data; takes 3-5 minutes):
   ```
   python data_pipeline.py
   ```

6. Run the analysis suite (generates all tables and figures; takes ~30 seconds):
   ```
   python analysis.py
   ```

7. Outputs land in `outputs/tables/` (CSV and JSON) and `outputs/figures/` (PNG).

## Data provenance

The pipeline generates a `data/manifest.json` file on each run, recording the UTC timestamp, Python version, all package versions (pandas, numpy, yfinance, etc.), and the SHA-256 hash of every raw data file downloaded. This manifest ensures bit-exact reproducibility: if the same versions are used and the upstream data sources have not changed, the outputs will be identical.
