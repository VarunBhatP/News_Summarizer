import feedparser
from datetime import datetime
from apps.digest.models import Source, Article
from .summarizer import generate_summary

def fetch_and_store_articles():
    sources = Source.objects()

    for source in sources:
        feed = feedparser.parse(source.rss_url)

        for entry in feed.entries:
            try:
                if not Article.objects(url=entry.link):
                    raw_text = getattr(entry, "summary", "")
                    summary_text = generate_summary(raw_text)

                    article = Article(
                        title=entry.title,
                        url=entry.link,
                        source=source,
                        published_at=getattr(entry, "published", datetime.utcnow()),
                        text=raw_text,
                        summary=summary_text,   # ✅ auto-saved summary
                    )
                    article.save()
                    print(f"Saved: {entry.title}")
            except Exception as e:
                print(f"Error saving article: {e}")
