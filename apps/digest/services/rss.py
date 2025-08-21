# apps/digest/services/rss.py

import feedparser
from datetime import datetime
import time
from ..models import Source, Article

def fetch_and_store_articles():
    """Fetch RSS feeds from all sources and store new articles in DB."""
    sources = Source.objects()  # all defined sources

    for source in sources:
        feed = feedparser.parse(source.rss_url)

        for entry in feed.entries:
            # Avoid duplicates (check URL)
            if Article.objects(url=entry.link).first():
                continue

            # Handle published_at conversion
            published_at = None
            if hasattr(entry, "published_parsed") and entry.published_parsed:
                published_at = datetime.fromtimestamp(time.mktime(entry.published_parsed))

            article = Article(
                title=entry.title,
                url=entry.link,
                source=source,
                published_at=published_at,
                text=entry.get("summary", ""),
            )
            article.save()
            print(f"Saved article: {article.title}")
