# apps/digest/pipeline.py
import feedparser
from dateutil import parser as dateparser
from datetime import datetime

from .models import Source, Article
from .summarizer import summarize_text
from .keywords import extract_keywords

def parse_pub_date(entry):
    # Prefer structured date if available
    if getattr(entry, "published_parsed", None):
        try:
            # published_parsed is a time.struct_time
            return datetime(*entry.published_parsed[:6])
        except Exception:
            pass
    # Fallback to 'published' string
    if getattr(entry, "published", None):
        try:
            return dateparser.parse(entry.published)
        except Exception:
            pass
    return None

def fetch_and_store_articles(category: str | None = None):
    """
    Fetch RSS for all sources (optionally limited by category),
    summarize, keyword-tag, and upsert into MongoDB by `url`.
    """
    sources = Source.objects
    if category:
        sources = sources.filter(category=category)

    for source in sources:
        print(f"Fetching from {source.name} ({source.rss_url})")
        feed = feedparser.parse(source.rss_url)

        for entry in feed.entries:
            try:
                url = getattr(entry, "link", None)
                if not url:
                    continue

                # Build text content
                raw_text = (
                    getattr(entry, "summary", None)
                    or getattr(entry, "description", None)
                    or getattr(entry, "title", "")
                )

                # Summarize + keywords
                summary = summarize_text(raw_text)
                tags = extract_keywords(summary or getattr(entry, "title", ""))

                # Parse date safely
                published_at = parse_pub_date(entry)

                # UPSERT by URL to avoid duplicates
                Article.objects(url=url).modify(
                    upsert=True,
                    new=True,
                    set__title=getattr(entry, "title", "")[:500],
                    set__source=source,
                    set__category=source.category,
                    set__published_at=published_at,
                    set__text=raw_text,
                    set__summary=summary,
                    set__tags=tags,
                )
            except Exception as e:
                print(f"[WARN] Failed to process entry: {e}")
