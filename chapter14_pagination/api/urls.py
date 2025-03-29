from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views


router = DefaultRouter()
# Using ViewSet
router.register(r"watchlist-pagenum-global-setting", views.WatchListGlobalPageNumberPaginationViewSet, basename="watchlist-pagenum-global-setting")
router.register(r"watchlist-pagenum-custom-setting", views.WatchListCustomPageNumberPaginationViewSet, basename="watchlist-pagenum-custom-setting")
router.register(r"watchlist-limit-offset", views.WatchListLimitOffsetPaginationViewSet, basename="watchlist-limit-offset")
router.register(r"watchlist-cursor", views.WatchListCursorPaginationViewSet, basename="watchlist-cursor")
router.register(r"watchlist-custom-base", views.WatchListCBPaginationViewSet, basename="watchlist-custom-base")
router.register(r"watchlist-custom-pn", views.WatchListCPNPaginationViewSet, basename="watchlist-custom-pn")

urlpatterns = [
    # path('reviews/', views.ReviewsListCurrentUserFilterView.as_view(), name='reviews-current-user'),
    
    # Using ViewSet
    path("", include(router.urls)),   
]
