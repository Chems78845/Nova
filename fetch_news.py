import os
import feedparser
from supabase import create_client

SUPABASE_URL = os.environ["SUPABASE_URL"]
SUPABASE_KEY = os.environ["SUPABASE_KEY"]

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# Liste des flux RSS de médias gaming FRANÇAIS fiables
FEEDS = [
    "https://www.jeuxvideo.com/rss/rss.xml",
    "https://www.gamekult.com/feed.xml",
    "https://www.numerama.com/feed/",
    "https://www.actugaming.net/feed/",
    "https://www.gamergen.com/rss/news"
]

print("Démarrage de la récupération des news en français...")

for feed_url in FEEDS:
    try:
        feed = feedparser.parse(feed_url)
        print(f"Lecture de : {feed.feed.get('title', feed_url)}")
        
        # On prend les 10 derniers articles de chaque site
        for entry in feed.entries[:10]:
            article = {
                "title": entry.title,
                "description": entry.get("summary", ""),
                "source_name": feed.feed.get("title", "Source FR"),
                "source_url": entry.link,
                "published_at": entry.get("published", None),
            }
            
            # On tente d'insérer l'article. 
            # La contrainte "UNIQUE" sur source_url évite les doublons.
            try:
                supabase.table("articles").upsert(
                    article, on_conflict="source_url"
                ).execute()
            except Exception as e:
                print("Erreur d'insertion pour un article:", e)
                
    except Exception as e:
        print(f"Erreur avec le flux {feed_url}: {e}")

print("Terminé.")
