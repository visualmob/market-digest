import pytz, datetime as dt, pandas as pd, yfinance as yf
from .config import TZ, RTH_ONLY, IMPACT_WINDOW_MIN, INDICES, SECTOR_ETFS, MIN_HEADLINE_IMPORTANCE
from .symbols import load_symbol_map
from .news import extract_entries, guess_tickers
from .impact import ret_15m
from .ranking import score
from .compose import market_summary, sectors_line, bullets
from .image_card import make_card

def run_daily():
    tz = pytz.timezone(TZ)
    name_map = load_symbol_map()
    items = extract_entries(tz)
    today = dt.datetime.now(tz).date()
    # keep items from today (ET date), generous window to catch late posts
    items = [x for x in items if x["ts_utc"].astimezone(tz).date() == today]

    rows=[]
    for it in items:
        ticks = guess_tickers(it, name_map)
        if not ticks: 
            continue
        ts_et = it["ts_utc"].astimezone(tz)
        for sym in set(ticks):
            try:
                res = ret_15m(sym, ts_et, rth_only=RTH_ONLY, window=IMPACT_WINDOW_MIN)
                if not res: 
                    continue
                rows.append({
                  "symbol": sym, "title": it["title"], "source": it["source"],
                  "link": it["link"], "ts_et": ts_et, **res
                })
            except Exception:
                continue

    if not rows:
        print("No scored news today.")
        # still produce a market wrap card so the feed isn't empty
        _produce_minimal(today)
        return

    df = pd.DataFrame(rows)
    df["ret15"] = df["ret15"].astype(float)
    df["score"] = df.apply(lambda r: score(r), axis=1)
    df = df.sort_values("score", ascending=False)

    # Market & sectors (close vs previous close)
    tickers = INDICES + SECTOR_ETFS
    quotes = yf.download(tickers, period="5d", interval="1d", auto_adjust=False, progress=False)
    close = quotes["Close"].iloc[-1]
    prev  = quotes["Close"].iloc[-2] if len(quotes) >= 2 else close
    pct = ((close/prev)-1)*100
    idx_line = market_summary(pct.to_dict())
    sector_pct = {k: float(pct[k]) for k in SECTOR_ETFS if k in pct}
    sect_str = sectors_line(sector_pct)

    # Compose text
    top = df[df["score"]>=MIN_HEADLINE_IMPORTANCE].head(5).to_dict("records")
    bullet_lines = bullets(top)
    date_str = today.strftime("%b %d, %Y")

    # Markdown (for ZORA description)
    md_parts = []
    md_parts.append("# Daily Market Bites — " + date_str + "\n")
    md_parts.append("## Top News\n" + bullet_lines + "\n")
    md_parts.append("## Market Summary\n" + idx_line + "\n")
    md_parts.append("## Sector Moves\n" + sect_str + "\n")
    md_parts.append("## Personal Take\n- Your notes here (macro tone, flows, notable options, etc.)\n\n*Sources:* \n")
    for t in top:
        md_parts.append("- " + t["source"] + " — " + t["link"] + "\n")
    md = "\n".join(md_parts)

    with open("daily.md","w",encoding="utf-8") as f: 
        f.write(md)

    # Image card (first 3 bullets)
    bullets_list = bullet_lines.split("\n")[:3] if bullet_lines else ["No major 15m movers detected today."]
    make_card(date_str, bullets_list, idx_line, sect_str, out_path="daily.png")

def _produce_minimal(today):
    # Fallback card on low-news days
    import yfinance as yf
    from .compose import market_summary, sectors_line
    from .image_card import make_card

    tickers = ["SPY","QQQ","DIA","^VIX","XLK","XLF","XLE","XLV","XLY","XLP","XLI","XLB","XLRE","XLU","XLC"]
    quotes = yf.download(tickers, period="5d", interval="1d", auto_adjust=False, progress=False)
    close = quotes["Close"].iloc[-1]
    prev  = quotes["Close"].iloc[-2] if len(quotes) >= 2 else close
    pct = ((close/prev)-1)*100
    idx_line = market_summary(pct.to_dict())
    sector_pct = {k: float(pct[k]) for k in ["XLK","XLF","XLE","XLV","XLY","XLP","XLI","XLB","XLRE","XLU","XLC"] if k in pct}
    sect_str = sectors_line(sector_pct)
    date_str = today.strftime("%b %d, %Y")
    make_card(date_str, ["Quiet news day — refer to market summary below."], idx_line, sect_str, out_path="daily.png")
    with open("daily.md","w",encoding="utf-8") as f:
        f.write("# Daily Market Bites — " + date_str + "\n\n" + idx_line + "\n\n" + sect_str + "\n")

if __name__=="__main__":
    run_daily()
