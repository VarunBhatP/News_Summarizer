# apps/digest/views.py
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from .nlp import summarize_text_simple
from django.utils.timezone import now
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from .models import Source, Article, UserFavorite, UserHistory
from .serializers import SourceSerializer, ArticleSerializer, FavoriteSerializer, HistorySerializer
from .pipeline import fetch_and_store_articles
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response

@api_view(["POST"])
def register_user(request):
    username = request.data.get("username")
    email = request.data.get("email")
    password = request.data.get("password")

    if User.objects.filter(username=username).exists():
        return Response({"error": "Username already exists"}, status=400)

    user = User.objects.create_user(username=username, email=email, password=password)
    return Response({"message": "User registered successfully", "username": user.username}, status=status.HTTP_201_CREATED)

@api_view(["GET"])
def list_sources(request):
    sources = Source.objects.all()
    return Response(SourceSerializer(sources, many=True).data)

@api_view(["GET"])
def list_articles(request):
    """
    Filters:
      - category=business|sports|general|...
      - tag=ai
      - q=free text search in title/summary/text (very simple)
      - limit=20 (default 20)
    """
    category = request.GET.get("category")
    tag = request.GET.get("tag")
    q = request.GET.get("q")
    limit = int(request.GET.get("limit", 20))

    qs = Article.objects
    if category:
        qs = qs.filter(category=category)
    if tag:
        qs = qs.filter(tags__icontains=tag)
    if q:
        # Basic OR match across fields
        qs = qs.filter(__raw__={"$or": [
            {"title": {"$regex": q, "$options": "i"}},
            {"summary": {"$regex": q, "$options": "i"}},
            {"text": {"$regex": q, "$options": "i"}},
        ]})

    articles = qs.order_by("-published_at")[:limit]
    return Response(ArticleSerializer(articles, many=True).data)

@api_view(["POST"])
def fetch_articles(request):
    category = request.data.get("category")  # None or "business"/...
    try:
        fetch_and_store_articles(category)
        return Response({"message": f"Fetched {category or 'all'} sources"}, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# ------- Minimal auth-based features -------
@api_view(["POST"])
@authentication_classes([JWTAuthentication])   # ✅ Use JWT, not Token/Session
@permission_classes([IsAuthenticated])
def add_favorite(request):
    article_id = request.data.get("article_id")
    if not article_id:
        return Response({"error": "article_id required"}, status=400)

    article = Article.objects(id=article_id).first()
    if not article:
        return Response({"error": "Article not found"}, status=404)

    fav = UserFavorite.objects(user_id=str(request.user.id), article=article).first()
    if not fav:
        fav = UserFavorite(user_id=str(request.user.id), article=article)
        fav.save()
    return Response({"message": "added", "id": str(fav.id)})


@api_view(["GET"])
@authentication_classes([JWTAuthentication])   # ✅ same here
@permission_classes([IsAuthenticated])
def list_favorites(request):
    favs = UserFavorite.objects(user_id=str(request.user.id))
    payload = []
    for f in favs:
        payload.append({
            "id": str(f.id),
            "created_at": f.created_at,
            "article": ArticleSerializer(f.article).data if f.article else None
        })
    return Response(payload)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def record_view(request):
    article_id = request.data.get("article_id")
    if not article_id:
        return Response({"error": "article_id required"}, status=400)
    article = Article.objects(id=article_id).first()
    if not article:
        return Response({"error": "Article not found"}, status=404)
    UserHistory(user_id=str(request.user.id), article=article, viewed_at=now()).save()
    return Response({"message": "recorded"})
    
@api_view(["GET"])
@permission_classes([IsAuthenticated]) 
def list_history(request):
    hist = UserHistory.objects(user_id=str(request.user.id)).order_by("-viewed_at")[:100]
    payload = []
    for h in hist:
        payload.append({
            "id": str(h.id),
            "viewed_at": h.viewed_at,
            "article": ArticleSerializer(h.article).data if h.article else None
        })
    return Response(payload)

@api_view(["GET"])
def search_articles(request):
    """Search articles by keyword in title or summary"""
    query = request.GET.get("q", "")

    if not query:
        return Response({"error": "Please provide a search query (?q=keyword)"}, status=status.HTTP_400_BAD_REQUEST)

    articles = Article.objects.filter(
        __raw__={
            "$or": [
                {"title": {"$regex": query, "$options": "i"}},
                {"summary": {"$regex": query, "$options": "i"}}
            ]
        }
    ).order_by("-published_at")[:20]

    serializer = ArticleSerializer(articles, many=True)
    return Response(serializer.data)


@api_view(["POST"])
def summarize_text(request):
    """Summarize raw text input"""
    text = request.data.get("text", "")

    if not text.strip():
        return Response({"error": "No text provided"}, status=status.HTTP_400_BAD_REQUEST)

    summary = summarize_text_simple(text)
    return Response({"summary": summary})
