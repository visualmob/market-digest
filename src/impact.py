import yfinance as yf
from datetime import timedelta
import pandas as pd

def _localize_utc(idx):
    # yfinance sometimes returns tz-naive UTC; ensure tz-aware UTC
    try:
        tz = idx.tz
    except Exception:
        tz = None
    if tz is None:
        return idx.tz_localize("UTC")
    return idx

def ret_15m(symbol, ts_et, rth_only=True, window=15):
    # Fetch 1m bars for the day around ts
    start = (ts_et - timedelta(minutes=60)).strftime("%Y-%m-%d")
    end   = (ts_et + timedelta(minutes=60)).strftime("%Y-%m-%d")
    df = yf.download(symbol, interval="1m", start=start, end=end, auto_adjust=False, progress=False)
    if df.empty: return None
    # Normalize to ET
    idx = _localize_utc(df.index)
    df.index = idx.tz_convert("America/New_York")
    if rth_only:
        df = df.between_time("09:30", "16:00", include_end=True)
    # Find first bar at/after news time
    t0 = df.index[df.index >= ts_et]
    if len(t0)==0: return None
    t0 = t0[0]
    # Last bar within +window minutes (clamp to session end)
    t1 = df.index[df.index <= t0 + timedelta(minutes=window)]
    if len(t1)==0: return None
    t1 = t1[-1]
    px0, px1 = float(df.loc[t0, "Close"]), float(df.loc[t1, "Close"])
    vol0, vol1 = float(df.loc[t0, "Volume"]), float(df.loc[t1, "Volume"])
    return {"t0": t0, "t1": t1, "ret15": (px1/px0-1)*100.0, "vol0": vol0, "vol1": vol1}
