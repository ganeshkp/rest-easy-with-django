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
    # path(r"watchlist-list", views.watchlist_list_view),
    # path(r"watchlist-list/<int:pk>/", views.watchlist_detail_view),
    # path(r"watchlist-lowlevelcaching", views.WatchLowLevelCachingView.as_view()),
    # path(r"watchlist-objectlevelcaching/<int:pk>/", views.WatchListObjectLevelCachingView.as_view()),
    # path(r"watchlist-cachemixinlist", views.WatchListCacheMixinListView.as_view()),
    # path(r"watchlist-cachemixinlist/<int:pk>/", views.WatchListCacheMixinDetailView.as_view()),
    # path(r"watchlist-varyonheadercache", views.WatchListVaryOnHeaderCacheView.as_view()),
    # path(r"watchlist-varyoncookiecache", views.WatchListVaryOnCookieCacheView.as_view()),
    
    # Using ViewSet
    path("", include(router.urls)),   
]
