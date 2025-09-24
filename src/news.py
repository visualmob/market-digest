import feedparser, re, datetime as dt, pytz
from bs4 import BeautifulSoup
from .sources import RSS_FEEDS, google_news_rss, TOP_NAMES

TICKER_RE = re.compile(r"\$([A-Z]{1,5})(?![A-Z])")

def extract_entries(tz):
    feeds = list(RSS_FEEDS)
    # Add Google News queries for megacaps on reputable domains
    for n in TOP_NAMES:
        q = "\"$\" " + n + " site:reuters.com OR site:cnbc.com OR site:marketwatch.com"
        feeds.append(google_news_rss(q))

    items = []
    for url in feeds:
        d = feedparser.parse(url)
        for e in d.entries:
            title = e.title
            link = e.link
            summ = BeautifulSoup(getattr(e, "summary", ""), "html.parser").get_text(" ", strip=True)
            src = link.split("/")[2].lower() if "://" in link else "generic"
            ts = getattr(e, "published_parsed", None) or getattr(e, "updated_parsed", None)
            if not ts:
                continue
            ts_utc = dt.datetime(*ts[:6], tzinfo=dt.timezone.utc)
            items.append({"title": title, "summary": summ, "link": link, "source": src, "ts_utc": ts_utc})
    # de-dupe by (title, link)
    seen = set(); out = []
    for x in items:
        k = (x["title"], x["link"])
        if k in seen: continue
        seen.add(k); out.append(x)
    return out

def guess_tickers(item, name_map):
    text = (item["title"] + " " + item["summary"])
    ticks = set(TICKER_RE.findall(text))
    title_lower = text.lower()
    if len(ticks) < 5:
        for name, sym in list(name_map.items())[:3000]:
            if name in title_lower:
                ticks.add(sym)
            if len(ticks) >= 5:
                break
    return list(ticks)
