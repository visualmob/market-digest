import pandas as pd, requests, io

def load_symbol_map():
    # NASDAQ publishes a list; sometimes rate limits — in practice this is fine for daily job.
    url = "https://www.nasdaqtrader.com/dynamic/SymDir/nasdaqlisted.txt"
    try:
        r = requests.get(url, timeout=20)
        r.raise_for_status()
    except Exception:
        # fallback to minimal set to avoid breaking
        return {
          "apple inc.": "AAPL",
          "microsoft corporation": "MSFT",
          "alphabet inc.": "GOOGL",
          "amazon.com, inc.": "AMZN",
          "meta platforms, inc.": "META",
          "tesla, inc.": "TSLA",
          "nvidia corporation": "NVDA"
        }
    df = pd.read_csv(io.StringIO(r.text), sep="|")
    if "Test Issue" in df.columns:
        df = df[df["Test Issue"] == "N"]
    # Map both full names and short names when possible
    name_map = {}
    for _, row in df.iterrows():
        sym = str(row["Symbol"]).strip()
        nm  = str(row["Security Name"]).strip().lower()
        name_map[nm] = sym
        # add first token
        short = nm.split(" ")[0]
        if short and short not in name_map:
            name_map[short] = sym
    # add some manual aliases
    name_map["alphabet"] = "GOOGL"
    name_map["google"] = "GOOGL"
    name_map["meta"] = "META"
    name_map["facebook"] = "META"
    return name_map
