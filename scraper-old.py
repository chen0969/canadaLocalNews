import feedparser
import json
from datetime import datetime

# Google News RSS feed（地區：加拿大，搜尋關鍵字：Ottawa 或 Canada）
rss_url = "https://news.google.com/rss/search?q=Ottawa+OR+Canada+when:7d&hl=en-CA&gl=CA&ceid=CA:en"

feed = feedparser.parse(rss_url)

articles = []
for entry in feed.entries:
    try:
        published_parsed = entry.published_parsed
        published_iso = datetime(*published_parsed[:6]).isoformat()
        published_date = datetime(*published_parsed[:3]).strftime("%Y-%m-%d")
    except:
        published_iso = None
        published_date = "未知日期"

    articles.append({
        "source": "Google News (Canada)",
        "title": entry.title,
        "url": entry.link,
        "published": published_iso,
        "date": published_date
    })

# 按時間新到舊排序
articles.sort(key=lambda x: x["published"] or "", reverse=True)

news_data = {
    "source": "Google News RSS",
    "query": "Ottawa OR Canada",
    "updated_at": datetime.utcnow().isoformat() + "Z",
    "article_count": len(articles),
    "articles": articles
}

# 儲存為 data/news.json
with open("data/news.json", "w", encoding="utf-8") as f:
    json.dump(news_data, f, ensure_ascii=False, indent=2)
