import pandas as pd

def market_summary(indices):
    # indices: dict with keys SPY, QQQ, DIA, ^VIX
    spy = indices.get("SPY", 0.0)
    qqq = indices.get("QQQ", 0.0)
    dia = indices.get("DIA", 0.0)
    vix = indices.get("^VIX", 0.0)
    return f"S&P (SPY) {spy:+.2f}% | QQQ {qqq:+.2f}% | DIA {dia:+.2f}% | VIX {vix:+.2f}%"

def sectors_line(sector_changes):
    # sector_changes: dict ETF -> %
    pairs = [f"{k} {v:+.2f}%" for k,v in sector_changes.items()]
    return " | ".join(pairs)

def bullets(top):
    lines=[]
    for x in top[:5]:
        host = x['source'].split('/')[0]
        lines.append(f"- ${x['symbol']} {x['ret15']:+.2f}% in 15m after: {x['title']} (source: {host})")
    return "\n".join(lines)
