from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views


router = DefaultRouter()
# Using ViewSet
router.register(r"watchlist-throttling", views.WatchlistThrottlingView, basename="watchlist-throttling")
router.register(r"streamplatform-throttling", views.StreamPlatformThrottlingView, basename="streamplatform-throttling")
router.register(r"review-throttling", views.ReviewThrottlingView, basename="review-throttling")
router.register(r"watchlist-scopedratethrottle", views.WatchlistScopedRateThrottleView, basename="watchlist-scopedratethrottle")
router.register(r"watchlist-customthrottle", views.WatchlistCustomThrottleView, basename="watchlist-customthrottle")


urlpatterns = [   
    # Using ViewSet
    path("", include(router.urls)),   
]
