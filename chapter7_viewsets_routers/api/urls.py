from django.urls import path, include
from watchlist_app.api import views
from rest_framework.routers import DefaultRouter
from watchlist_app.api.custom_routers import CustomRouter1

router = DefaultRouter()
# Using ViewSet
router.register(r"watchlist-viewset1", views.WatchListViewSet1)

# Using GenericViewSet
router.register(r"watchlist-viewset2", views.WatchListViewSet2, basename="watchlist-viewset2")

# Using ModelViewSet
router.register(r"watchlist-viewset3", views.WatchListViewSet3, basename="watchlist_viewset3")
router.register(r"streamplatform-viewset3", views.StreamPlatformViewSet3, basename="streamplatform_viewset3")

# Using ReadOnlyModelViewSet
router.register(r"watchlist-viewset4", views.WatchListViewSet4, basename="watchlist_viewset4")


# Using HyperLinkedModelSerializer
router1 = DefaultRouter()
router1.register(r"watchlist-viewset5", views.WatchListViewSet5, basename="watchlist-viewset5")
router1.register(r"streamplatform-viewset5", views.StreamPlatformViewSet5, basename="streamplatform-viewset5")

router2 = CustomRouter1()
router2.register(r"streamplatform-viewset3-custom", views.StreamPlatformViewSet3, basename="streamplatform_viewset3_custom")

urlpatterns = [   
    # Using ViewSet
    path("", include(router.urls)),
    
    #Using HyperlinkedModelSerializer
    path('', include((router1.urls, 'app_name'), namespace='instance_name')),
    
    # Using CustomRouter1
    path("", include(router2.urls)),
    
]

# urlpatterns += router.urls
# urlpatterns += router2.urls
