from django.urls import path, include
from rest_framework.routers import DefaultRouter

from chapter9_authentication.api import views


router = DefaultRouter()
# Using ViewSet
router.register(r"watchlist-viewset", views.WatchListViewSet)
router.register(r"platform-viewset", views.StreamPlatformViewSet)
router.register(r"review-viewset", views.ReviewViewSet)

urlpatterns = [   
    # Using ViewSet
    path("", include(router.urls)),    
]