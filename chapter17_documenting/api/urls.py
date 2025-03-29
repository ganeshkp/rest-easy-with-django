from django.urls import path, include
from rest_framework.routers import DefaultRouter

from chapter17_documenting.api import views


router = DefaultRouter()
# Using ViewSet
router.register(r"c17-watchlists", views.WatchListViewSet, basename="c17-watchlists")

urlpatterns = [
    # Define versioned paths using a regex for versioning
    
    # Using ViewSet
    path("", include(router.urls)),   
]
