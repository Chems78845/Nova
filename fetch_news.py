import os
import feedparser
from supabase import create_client

SUPABASE_URL = os.environ["SUPABASE_URL"]
SUPABASE_KEY = os.environ["SUPABASE_KEY"]

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

FEEDS = [
    "https://www.pcgamer.com/rss/",
    "https://www.eurogamer.net/feed",
    "https://blog.playstation.com/feed/",
    "https://news.xbox.com/en-us/feed/",
]

for feed_url in FEEDS:
    feed = feedparser.parse(feed_url)
    for entry in feed.entries[:10]:
        article = {
            "title": entry.title,
            "description": entry.get("summary", ""),
            "source_name": feed.feed.get("title", "Source"),
            "source_url": entry.link,
            "published_at": entry.get("published", None),
        }
        try:
            supabase.table("articles").upsert(
                article, on_conflict="source_url"
            ).execute()
        except Exception as e:
            print("Erreur:", e)

print("Terminé.")
