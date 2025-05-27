import feedparser
import json
from datetime import datetime, timedelta
import time

# 媒體與網址對照
source_site_map = {
    "CBC": "cbc.ca",
    "Global News": "globalnews.ca",
    "CTV News": "ctvnews.ca",
    "National Post": "nationalpost.com",
    "Ottawa Citizen": "ottawacitizen.com",
    "Ottawa Sun": "ottawasun.com",
    "CityNews": "citynews.ca",
    "Hill Times": "hilltimes.com",
    "BNN Bloomberg": "bnnbloomberg.ca",
    "Canadaland": "canadaland.com",
    "iPolitics": "ipolitics.ca",
    "The Globe and Mail": "theglobeandmail.com"
}

# 關鍵字（政治主題）
search_keywords = [
    "Canada politics", "Parliament", "Justin Trudeau", "Pierre Poilievre",
    "House of Commons", "Canadian government", "federal election"
]

# 產生 Google News RSS URL（用 site: 限定網站）
def build_rss_url(site, keyword):
    keyword_encoded = keyword.replace(' ', '+')
    return f"https://news.google.com/rss/search?q={keyword_encoded}+site:{site}&hl=en-CA&gl=CA&ceid=CA:en"

# 擷取新聞（僅限近 24 小時）+ 過濾標題關聯
def fetch_articles(source, site, keyword):
    feed = feedparser.parse(build_rss_url(site, keyword))
    now = datetime.utcnow()
    cutoff = now - timedelta(days=1)
    articles = []

    if not feed.entries:
        return []

    for entry in feed.entries:
        try:
            pub = datetime(*entry.published_parsed[:6])

            if pub >= cutoff:
                articles.append({
                    "source": source,
                    "title": entry.title,
                    "url": entry.link,
                    "published": pub.isoformat(),
                    "date": pub.strftime("%Y-%m-%d")
                })
        except Exception:
            continue
    return articles


# 去除重複（title + url）
def deduplicate(articles):
    seen = set()
    unique = []
    for a in articles:
        key = (a["title"], a["url"])
        if key not in seen:
            seen.add(key)
            unique.append(a)
    return unique

# 主程式
all_articles = []
for source, site in source_site_map.items():
    print(f"🔍 媒體：{source}")
    found_count = 0
    for keyword in search_keywords:
        results = fetch_articles(source, site, keyword)
        if results:
            print(f"  ✅ {keyword} ➜ 找到 {len(results)} 筆")
            all_articles.extend(results)
            found_count += len(results)
        else:
            print(f"  ❌ {keyword} ➜ {source} 沒資料")
        time.sleep(2)

    if found_count == 0:
        print(f"⚠️  {source} 沒抓到任何政治新聞")

# 去重、排序
final_articles = deduplicate(all_articles)
final_articles.sort(key=lambda x: x["published"], reverse=True)

# 儲存成 politics.json
news_data = {
    "source": "Google News RSS + site-filtered political sources",
    "query": "Canada politics",
    "updated_at": datetime.utcnow().isoformat() + "Z",
    "article_count": len(final_articles),
    "articles": final_articles
}

with open("data/politics.json", "w", encoding="utf-8") as f:
    json.dump(news_data, f, ensure_ascii=False, indent=2)

print(f"\n✅ 共抓到 {len(final_articles)} 則政治新聞，已儲存到 data/politics.json")
