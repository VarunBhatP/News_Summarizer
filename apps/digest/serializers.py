# apps/digest/serializers.py
from rest_framework import serializers
from .models import Article, Source, UserFavorite, UserHistory

class SourceSerializer(serializers.Serializer):
    id = serializers.CharField()
    name = serializers.CharField()
    rss_url = serializers.CharField()
    category = serializers.CharField()

class ArticleSerializer(serializers.Serializer):
    id = serializers.CharField()
    title = serializers.CharField()
    url = serializers.CharField()
    category = serializers.CharField()
    published_at = serializers.DateTimeField(allow_null=True)
    summary = serializers.CharField(allow_blank=True, allow_null=True)
    tags = serializers.ListField(child=serializers.CharField(), required=False)
    source = serializers.SerializerMethodField()

    def get_source(self, obj):
        try:
            return obj.source.name if obj.source else None
        except Exception:
            return None

class FavoriteSerializer(serializers.Serializer):
    id = serializers.CharField()
    article = ArticleSerializer()
    created_at = serializers.DateTimeField()

class HistorySerializer(serializers.Serializer):
    id = serializers.CharField()
    article = ArticleSerializer()
    viewed_at = serializers.DateTimeField()
