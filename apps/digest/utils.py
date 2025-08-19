import feedparser
from datetime import datetime
from .models import Source, Article

def fetch_articles():
    sources = Source.objects  # all RSS sources
    for src in sources:
        feed = feedparser.parse(src.rss_url)
        for entry in feed.entries[:5]:  # limit for now
            if not Article.objects(url=entry.link):  # avoid duplicates
                art = Article(
                    title=entry.title,
                    url=entry.link,
                    source=src,
                    published_at=getattr(entry, "published_parsed", None) and datetime(*entry.published_parsed[:6]),
                    text=getattr(entry, "summary", ""),
                    summary="",  # we’ll fill later after summarization
                )
                art.save()
                print(f"✅ Saved: {entry.title}")
            else:
                print(f"⚠️ Skipped duplicate: {entry.title}")
