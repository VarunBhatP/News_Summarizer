from rest_framework import serializers
from .models import Article, Source


class ArticleSerializer(serializers.Serializer):
    id = serializers.CharField()
    title = serializers.CharField()
    url = serializers.CharField()
    published_at = serializers.DateTimeField()
    summary = serializers.CharField()
    text = serializers.CharField(required=False, allow_blank=True)
    tags = serializers.ListField(child=serializers.CharField(), required=False)
    score = serializers.FloatField()
    created_at = serializers.DateTimeField()
    source = serializers.CharField(source="source.name", required=False)  # show source name instead of object ID
