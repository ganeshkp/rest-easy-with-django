from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter

from . import views


router = DefaultRouter()
# Using ViewSet
router.register(r"watchlist-urlpath", views.WatchListUrlPathVersioningViewSet, basename="watchlist-urlpath")
router.register(r"watchlist-namespace", views.WatchListNamespaceVersioningViewSet, basename="watchlist-namespace")


urlpatterns = [
    # Define versioned paths using a regex for versioning
    re_path(r'^(?P<version>(v1|v2))/', include(router.urls)),
    
    # Using ViewSet
    path("", include(router.urls)),   
]
