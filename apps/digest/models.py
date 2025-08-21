# apps/digest/models.py
from mongoengine import (
    Document, StringField, DateTimeField, ReferenceField, ListField, FloatField, signals
)
from datetime import datetime

class Source(Document):
    name = StringField(required=True)        # e.g., "BBC General"
    rss_url = StringField(required=True)     # e.g., "http://feeds.bbci.co.uk/news/rss.xml"
    category = StringField(default="general")
    created_at = DateTimeField(default=datetime.utcnow)

    meta = {"indexes": ["category", "rss_url"]}

class Article(Document):
    title = StringField(required=True)
    url = StringField(required=True, unique=True)  # RSS <link>, used for dedupe
    source = ReferenceField(Source)                # FK to Source
    category = StringField(default="general")
    published_at = DateTimeField()
    text = StringField()
    summary = StringField()
    tags = ListField(StringField())
    score = FloatField(default=0.0)
    created_at = DateTimeField(default=datetime.utcnow)

    meta = {
        "indexes": [
            "category",
            "tags",
            {"fields": ["$title", "$summary", "$text"], "default_language": "english"},
        ]
    }

# ---- Minimal user features (favorites & history) ----
# We’ll store Django user id as string to avoid ORM cross-dependency.
class UserFavorite(Document):
    user_id = StringField(required=True)               # Django User.id as str
    article = ReferenceField(Article, required=True)
    created_at = DateTimeField(default=datetime.utcnow)

    meta = {"indexes": ["user_id"]}

class UserHistory(Document):
    user_id = StringField(required=True)
    article = ReferenceField(Article, required=True)
    viewed_at = DateTimeField(default=datetime.utcnow)

    meta = {"indexes": ["user_id", "-viewed_at"]}
