from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views


router = DefaultRouter()
# Using ViewSet
router.register(r"watchlist-viewset1", views.WatchListViewSet1)
router.register(r"platform-viewset1", views.StreamPlatformViewSet1)
router.register(r"review-viewset1", views.ReviewViewSet1)

urlpatterns = [   
    # Using ViewSet
    path("", include(router.urls)),    
]