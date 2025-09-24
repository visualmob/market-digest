TZ = "America/New_York"
RTH_ONLY = True          # set False to allow extended hours for impact calc
IMPACT_WINDOW_MIN = 15
MIN_HEADLINE_IMPORTANCE = 0.5   # filter low-score noise

WATCH_TICKERS = None     # None = infer from headlines; or set list like ["AAPL","TSLA","NVDA"]

# Use ^VIX (index) for true VIX
INDICES = ["SPY","QQQ","DIA","^VIX"]
SECTOR_ETFS = ["XLK","XLF","XLE","XLV","XLY","XLP","XLI","XLB","XLRE","XLU","XLC"]

SOURCE_WEIGHTS = {
  "reuters": 1.3, "cnbc": 1.1, "marketwatch": 1.0, "sec.gov": 1.0,
  "sec": 1.0, "prnewswire": 0.9, "businesswire": 0.9, "generic": 1.0
}
