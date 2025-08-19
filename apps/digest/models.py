# apps/digest/models.py

from mongoengine import Document, StringField, DateTimeField, ReferenceField, ListField, FloatField
from datetime import datetime

class Source(Document):
    name = StringField(required=True)       # "BBC News"
    rss_url = StringField(required=True)    # "http://feeds.bbci.co.uk/news/rss.xml"
    category = StringField(default="general")
    created_at = DateTimeField(default=datetime.utcnow)

class Article(Document):
    title = StringField(required=True)                
    url = StringField(required=True, unique=True)     
    source = ReferenceField(Source)                   
    published_at = DateTimeField()
    text = StringField()                              
    summary = StringField()                           
    tags = ListField(StringField())                   
    score = FloatField(default=0.0)                   
    created_at = DateTimeField(default=datetime.utcnow)
