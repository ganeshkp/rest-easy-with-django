from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views


router = DefaultRouter()
# Using ViewSet
router.register(r"watchlist-allowany", views.WatchlistAllowAnyView, basename="watchlist-allowany")
router.register(r"watchlist-isauthenticated", views.WatchListIsAuthenticatedView, basename="watchlist-isauthenticated")
router.register(r"watchlist-isauthenticatedorreadonly", views.WatchListIsAuthenticatedOrReadOnlyView, basename="watchlist-isauthenticatedorreadonly")
router.register(r"watchlist-adminuser", views.WatchListIsAdminUserView, basename="watchlist-adminuser")
router.register(r"watchlist-modelperm", views.WatchListModelPermView, basename="watchlist-modelperm")
router.register(r"watchlist-multiplepermview", views.WatchListMultiplePermView, basename="watchlist-multiplepermview")
router.register(r"watchlist-objectpermissionview", views.WatchListObjectPermissionsView, basename="watchlist-objectpermissionview")
router.register(r"watchlist-objectpermissionmapview", views.WatchListObjectPermissionsMapView, basename="watchlist-objectpermissionmapview")

urlpatterns = [   
    path(r"stream-platform", views.stream_platform_isauthenticated_view),
    path('<int:pk>/reviews1/', views.ReviewList1.as_view(), name='review-list1'),
    path('reviews1/<int:pk>/', views.ReviewDetailCustomPermissionView.as_view(), name='review-detail1'),
    path('watchlist/', views.WatchlistCustomPermissionView.as_view(), name='watchlist'),
    
    # Using ViewSet
    path("", include(router.urls)),   
]
