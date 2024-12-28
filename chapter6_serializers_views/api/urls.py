from django.urls import path
from chapter6_serializers_views.api import views

urlpatterns = [   
    # Using Basic Serializer for the views
    path('watchlist-basic-serializer/', views.WatchlistBasicSerializerView.as_view(), name="watchlist-basic-serializer"),
    path('watchlist-detail-basic-serializer/<int:pk>/', views.WatchlistDetailBasicSerializerView.as_view(), name="watchlist-detail-basic-serializer"),
    path('streamplatform-detail-basic-serializer/<int:pk>/', views.StreamPlatformBasicSerializerView.as_view(), name="streamplatform-detail-basic-serializer"),
    path('reviewlist-basic-serializer/', views.ReviewlistBasicSerializerView.as_view(), name="reviewlist-basic-serializer"),
    
    # Using ModelSerializer for the views
    path('watchlist-model-serializer/', views.WatchlistModelSerializerView.as_view(), name="watchlist-model-serializer"),
    path('streamplatform-model-serializer/', views.StreamPlatformListView2.as_view(), name="streamplatform-model-serializer"),
    path('streamplatform-detail-model-serializer/<int:pk>/', views.StreamPlatformDetailView2.as_view(), name="streamplatform-detail-model-serializer"),
    
    # Using HyperlinkedModelSerializer for the views
    path('watchlist-hm-serializer/', views.WatchlistHMSerializerView.as_view(), name="watchlist-hm-serializer"),
    path('watchlist-detail-hm-serializer/<int:pk>/', views.WatchlistDetailHMSerializerView.as_view(), name="watchlist-detail-hm-serializer"),
    path('streamplatform-detail-hm-serializer/<int:pk>/', views.StreamPlatformDetailHMSerializerView.as_view(), name="streamplatform-detail-hm-serializer"),
    
    # Using ListSerializer for the views
    path('watchlist-list-serializer/', views.WatchlistListSerializerView.as_view(), name="watchlist-list-serializer"),
    
    # Using BaseSerializer for the views
    path('watchlist-base-serializer/', views.WatchlistBaseSerializerView.as_view(), name="watchlist-base-serializer"),
    
    # Using GenericAPIView for the views
    path('watchlist-generic-api/', views.WatchlistGAPIView.as_view(), name="watchlist-generic-api"),
    path('watchlist-detail-generic-api/<str:title>/', views.WatchlistDetailGAPIView.as_view(), name="watchlist-detail-generic-api"),
    
    #Using ListModelMixin and GenericAPIView for views
    path('watchlist-list-model-mixin/', views.WatchlistListModelMixinView.as_view(), name="watchlist-list-model-mixin"),
    
    #Using CreateModelMixin and GenericAPIView for views
    path('watchlist-create-model-mixin/', views.WatchlistCreateModelMixinView.as_view(), name="watchlist-create-model-mixin"),    
    
    #Using RetrieveModelMixin and GenericAPIView for views
    path('watchlist-retrieve-model-mixin/<int:pk>/', views.WatchlistRetrieveModelMixinView.as_view(), name="watchlist-retrieve-model-mixin"),
    
    #Using UpdateModelMixin and GenericAPIView for views
    path('watchlist-update-model-mixin/<int:pk>/', views.WatchlistUpdateModelMixinView.as_view(), name="watchlist-update-model-mixin"),
    
    #Using DestroyModelMixin and GenericAPIView for views
    path('watchlist-destroy-model-mixin/<int:pk>/', views.WatchlistDestroyModelMixinView.as_view(), name="watchlist-destroy-model-mixin"),
    
    #Using CreateAPIView for views
    path('watchlist-create-api/', views.WatchlistCreateAPIView.as_view(), name="watchlist-create-api"),
    
    #Using ListAPIView for views
    path('watchlist-list-api/', views.WatchlistListAPIView.as_view(), name="watchlist-list-api"),
    
    #Using RetrieveAPIView for views
    path('watchlist-retrieve-api/<str:title>/', views.WatchlistRetrieveAPIView.as_view(), name="watchlist-retrieve-api"),
    
    #Using DestroyAPIView for views
    path('watchlist-destroy-api/<str:title>/', views.WatchlistDestroyAPIView.as_view(), name="watchlist-destroy-api"),
    
    #Using UpdateAPIView
    path('watchlist-update-api/<int:pk>/', views.WatchlistUpdateAPIView.as_view(), name="watchlist-update-api"),
    
    #Using ListCreateAPIView for views
    path('watchlist-list-create-api/', views.WatchlistListCreateAPIView.as_view(), name="watchlist-list-create-api"),
    
    #Using RetrieveUpdateAPIView
    path('watchlist-retrieve-update-api/<int:pk>/', views.WatchlistRetrieveUpdateAPIView.as_view(), name="watchlist-retrieve-update-api"),
    
    #Using RetrieveDestroyAPIView
    path('watchlist-retrieve-destroy-api/<int:pk>/', views.WatchlistRetrieveDestroyAPIView.as_view(), name="watchlist-retrieve-destroy-api"),
    
    #Using RetrieveUpdateDestroyAPIView
    path('watchlist-rud-api/<int:pk>/', views.WatchlistRudAPIView.as_view(), name="watchlist-rud-api"),
    
    #Using MultipleFieldLookupMixin
    path('watchlist-mfl-mixin/<str:title>/', views.WatchlistMFLMixinView.as_view(), name='watchlist-mfl-mixin'),
    
    #Using Custom Base class for views
    path('watchlist-inherited-list-api/', views.WatchlistIListAPIView.as_view(), name="watchlist-inherited-list-api"),
    path('watchlist-inherited-create-api/', views.WatchlistICreateAPIView.as_view(), name="watchlist-inherited-create-api"),
    
]
