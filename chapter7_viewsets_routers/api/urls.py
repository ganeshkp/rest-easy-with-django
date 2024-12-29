from django.urls import path, include
from rest_framework.routers import DefaultRouter
from chapter7_viewsets_routers.api import views
from chapter7_viewsets_routers.api.custom_routers import CustomRouter

router = DefaultRouter()

# Using ViewSet
router.register(r"watchlist-viewset", views.WatchListViewSet, basename="c7-watchlist-viewset")

# Using GenericViewSet
router.register(r"watchlist-generic-viewset", views.WatchListGenericViewSet, basename="watchlist-generic-viewset")

# Using ModelViewSet
router.register(r"watchlist-model-viewset", views.WatchListModelViewSet, basename="watchlist-model-viewset")
router.register(r"streamplatform-model-viewset", views.StreamPlatformModelViewSet, basename="streamplatform-model-viewset")

# Using ReadOnlyModelViewSet
router.register(r"watchlist-readonly-model-viewset", views.WatchListReadOnlyModelViewSet, basename="watchlist-readonly-model-viewset")

# Using HyperLinkedModelSerializer
router1 = DefaultRouter()
router1.register(r"watchlist-hlms-viewset", views.WatchListHLMSViewset, basename="watchlist-hlms-viewset")
router1.register(r"streamplatform-hlms-viewset", views.StreamPlatformHLMSViewset, basename="streamplatform-hlms-viewset")

router2 = CustomRouter()
router2.register(r"streamplatform-custom-viewset", views.StreamPlatformModelViewSet, basename="streamplatform-custom-viewset")

urlpatterns = [   
    # Using ViewSet
    path("", include(router.urls)),
    
    #Using HyperlinkedModelSerializer
    path('', include((router1.urls, 'app_name'), namespace='instance_name')),
    
    # Using CustomRouter1
    path("", include(router2.urls)),    
]
