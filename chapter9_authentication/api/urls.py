from django.urls import path, include
from rest_framework.routers import DefaultRouter

from chapter9_authentication.api import views


router = DefaultRouter()
# Using ViewSet
router.register(r"watchlist-viewset", views.WatchListViewSet)
router.register(r"review-viewset", views.ReviewViewSet)

urlpatterns = [   
    path('streamplatforms/', views.streamplatform_list, name="streamplatform-list"),
    path('streamplatforms/<int:pk>/', views.streamplatform_detail, name="streamplatform-detail"),
    # Using ViewSet
    path("", include(router.urls)),    
]