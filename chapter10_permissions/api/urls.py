from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views


router = DefaultRouter()
# Using ViewSet
router.register(r"watchlist-isauthenticated", views.WatchListIsAuthenticatedView, basename="watchlist-isauthenticated")
router.register(r"watchlist-isauthenticatedadmin", views.WatchListIsAuthenticatedAdminView, basename="watchlist-isauthenticatedadmin")
router.register(r"watchlist-multiplepermview", views.WatchListMultiplePermView, basename="watchlist-multiplepermview")
router.register(r"watchlist-modelperm", views.WatchListModelPermView, basename="watchlist-modelperm")

urlpatterns = [   
    path(r"stream-platform", views.stream_platform_view1),
    path('<int:pk>/reviews1/', views.ReviewList1.as_view(), name='review-list1'),
    path('reviews1/<int:pk>/', views.ReviewDetail1.as_view(), name='review-detail1'),
    path('watchlist/', views.WatchListView1.as_view(), name='watchlist'),
    # Using ViewSet
    path("", include(router.urls)),   
]
