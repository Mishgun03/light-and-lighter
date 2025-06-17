from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PriceHistoryListView, FavoriteViewSet, ListingViewSet

router = DefaultRouter()
router.register(r'favorites', FavoriteViewSet, basename='favorite')

api_patterns = [
    path('listings/', ListingViewSet.as_view(), name='listing'),
    path('items/<str:item_id>/history/', PriceHistoryListView.as_view(), name='price-history'),
]

user_patterns = [
    path('', include(router.urls)),
]

urlpatterns = api_patterns + user_patterns