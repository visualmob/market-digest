def google_news_rss(query: str) -> str:
    import urllib.parse as up
    return "https://news.google.com/rss/search?q=" + up.quote(query) + "&hl=en-US&gl=US&ceid=US:en"

# Core RSS feeds (expand over time)
RSS_FEEDS = [
  "https://feeds.reuters.com/reuters/businessNews",
  "https://feeds.reuters.com/reuters/USMarketsNews",
  "https://www.cnbc.com/id/100003114/device/rss/rss.html",
  "https://feeds.marketwatch.com/marketwatch/topstories/",
  # SEC Atom: latest filings (8-Ks often move stocks)
  "https://www.sec.gov/cgi-bin/browse-edgar?action=getcurrent&CIK=&type=8-K&company=&dateb=&owner=include&start=0&count=100&output=atom",
]

# High-signal megacaps to query via Google News RSS (safe, free)
TOP_NAMES = ["Apple", "Microsoft", "Amazon", "Nvidia", "Tesla", "Meta", "Alphabet"]
