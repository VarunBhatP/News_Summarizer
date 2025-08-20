from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Article
from .serializers import ArticleSerializer

@api_view(["GET"])
def summarized_articles(request):
    articles = Article.objects(summary__ne="").order_by("-published")[:20]  # last 20
    serializer = ArticleSerializer(articles, many=True)
    return Response(serializer.data)
