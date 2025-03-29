from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views


router = DefaultRouter()
# Using ViewSet
router.register(r"watchlist-caching", views.WatchlistCachingView, basename="watchlist-caching")

urlpatterns = [   
    path(r"watchlist-list", views.watchlist_list_view),
    path(r"watchlist-list/<int:pk>/", views.watchlist_detail_view),
    path(r"watchlist-lowlevelcaching", views.WatchLowLevelCachingView.as_view()),
    path(r"watchlist-objectlevelcaching/<int:pk>/", views.WatchListObjectLevelCachingView.as_view()),
    path(r"watchlist-cachemixinlist", views.WatchListCacheMixinListView.as_view()),
    path(r"watchlist-cachemixinlist/<int:pk>/", views.WatchListCacheMixinDetailView.as_view()),
    path(r"watchlist-varyonheadercache", views.WatchListVaryOnHeaderCacheView.as_view()),
    path(r"watchlist-varyoncookiecache", views.WatchListVaryOnCookieCacheView.as_view()),
    
    # Using ViewSet
    path("", include(router.urls)),   
]
