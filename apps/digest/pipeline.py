import feedparser
from datetime import datetime
from apps.digest.models import Source, Article

def fetch_and_store_articles():
    # Get all sources from DB
    sources = Source.objects()

    for source in sources:
        feed = feedparser.parse(source.rss_url)

        for entry in feed.entries:
            try:
                # Avoid duplicates by URL
                if not Article.objects(url=entry.link):
                    article = Article(
                        title=entry.title,
                        url=entry.link,
                        source=source,
                        published_at=getattr(entry, "published", datetime.utcnow()),
                        text=getattr(entry, "summary", ""),   # summary = snippet, not our own summary
                    )
                    article.save()
                    print(f"Saved: {entry.title}")
            except Exception as e:
                print(f"Error saving article: {e}")
