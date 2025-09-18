from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ItemViewSet,
    FavoriteViewSet,
    DashboardView,
    LeaderboardView,
    PopulationView,
    AuthView,
    RegisterView,
    PasswordResetRequestView,
    PriceHistoryView,
)

router = DefaultRouter()
router.register(r"items", ItemViewSet, basename="item")
router.register(r"favorites", FavoriteViewSet, basename="favorite")

urlpatterns = [
    path("auth/", AuthView.as_view(), name="auth"),
    path("auth/register/", RegisterView.as_view(), name="register"),
    path("auth/password-reset/", PasswordResetRequestView.as_view(), name="password_reset"),
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
    path("leaderboard/", LeaderboardView.as_view(), name="leaderboard"),
    path("population/", PopulationView.as_view(), name="population"),
    path("items/<str:item_id>/history/", PriceHistoryView.as_view(), name="price_history"),
    path("", include(router.urls)),
]


