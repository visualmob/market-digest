# Market Digest (Free, GitHub Actions)

This repo generates a **daily stock market digest** after the close using only free sources.
It produces:
- `daily.png` — a social image (1080×1350) with top headlines and market summary
- `daily.md` — a caption/markdown with top news (linked), market wrap, sector moves, and a "personal take" section

The workflow runs on weekdays around **5:15pm US/Eastern (21:15 UTC)** via GitHub Actions.

## How it works
- Pulls news from RSS (Reuters/CNBC/MarketWatch/SEC) and Google News RSS for megacap queries.
- Detects tickers from $TICKER patterns and company names.
- Uses `yfinance` 1-min data to compute 15-minute price impact for each headline.
- Ranks items by absolute move, source weight, and volume spike flag.
- Builds a simple PNG card (Pillow) and a markdown file for your post caption.

## Local test
```bash
python -m venv .venv
. .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python -m src.run
```

Artifacts will be created in the repo root: `daily.png`, `daily.md`.

## GitHub Actions
The workflow is in `.github/workflows/daily.yml`. It schedules at 21:15 UTC (M–F). You can also run it manually from the Actions tab with "Run workflow".
