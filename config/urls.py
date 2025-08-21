# config/urls.py
from django.contrib import admin
from django.urls import path
from apps.digest.views import (
    register_user,
    list_sources,
    list_articles,
    fetch_articles,
    add_favorite,
    list_favorites,
    record_view,
    list_history,
    search_articles,
    summarize_text_api,   # ✅ use new name
)

from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path("admin/", admin.site.urls),

    path("api/register/", register_user, name="register"),


    # Auth token (login to get token)
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    # Core APIs
    path("api/sources/", list_sources),
    path("api/articles/", list_articles),
    path("api/fetch/", fetch_articles),

    # User features
    path("api/favorites/", list_favorites),
    path("api/favorites/add/", add_favorite),
    path("api/history/", list_history),
    path("api/history/record/", record_view),

    path("api/articles/search/", search_articles, name="search_articles"),
    path("api/summarize/", summarize_text_api, name="summarize_text"),
]
