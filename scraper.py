import feedparser
import json
from datetime import datetime

# RSS 來源列表
rss_feeds = {
    "Ottawa Citizen": "https://ottawacitizen.com/feed/",
    "CBC Ottawa": "https://www.cbc.ca/cmlink/rss-canada-ottawa",
    "Global News Canada": "https://globalnews.ca/canada/feed/",
    "CityNews Ottawa": "https://ottawa.citynews.ca/rss"
}

articles = []

# 處理每個 RSS 來源
for source_name, url in rss_feeds.items():
    feed = feedparser.parse(url)
    for entry in feed.entries:
        try:
            published_parsed = entry.published_parsed
            published_iso = datetime(*published_parsed[:6]).isoformat()
            published_date = datetime(*published_parsed[:3]).strftime("%Y-%m-%d")
        except:
            published_iso = None
            published_date = "未知日期"

        articles.append({
            "source": source_name,
            "title": entry.title,
            "url": entry.link,
            "published": published_iso,
            "date": published_date
        })

# 按時間排序（新到舊）
articles.sort(key=lambda x: x["published"] or "", reverse=True)

news_data = {
    "sources": list(rss_feeds.keys()),
    "updated_at": datetime.utcnow().isoformat() + "Z",
    "article_count": len(articles),
    "articles": articles,
}

# 輸出為 JSON 檔案
with open("data/news.json", "w", encoding="utf-8") as f:
    json.dump(news_data, f, ensure_ascii=False, indent=2)
