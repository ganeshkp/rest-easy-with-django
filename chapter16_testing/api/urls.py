from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter

from . import views


router = DefaultRouter()
# Using ViewSet
router.register(r"watchlists", views.WatchListViewSet, basename="watchlists")
router.register(r"stream-platforms", views.StreamPlatformViewSet, basename="stream-platforms")
router.register(r"reviews", views.ReviewViewSet, basename="reviews")

urlpatterns = [
    # Define versioned paths using a regex for versioning
    
    # Using ViewSet
    path("", include(router.urls)),   
]
