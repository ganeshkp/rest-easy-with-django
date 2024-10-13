from django.urls import path
from watchlist_app.api import views

urlpatterns = [   
    # Using Basic Serializer for the views
    path('watchlist-cbv-try1/', views.WatchlistCBView1.as_view(), name="watchlist-cbv-try1"),
    path('watchlist-detail-cbv-try1/<int:pk>/', views.WatchlistDetailCBView1.as_view(), name="watchlist-detail-cbv-try1"),
    path('streamplatform-detail-cbv-try1/<int:pk>/', views.StreamPlatformDetailView1.as_view(), name="streamplatform-detail-cbv-try1"),
    path('reviewlist-cbv-try1/', views.ReviewlistCBView1.as_view(), name="reviewlist-cbv-try1"),
    
    # Using ModelSerializer for the views
    path('watchlist-cbv-try2/', views.WatchlistCBView2.as_view(), name="watchlist-cbv-try2"),
    path('streamplatform-cbv-try2/', views.StreamPlatformListView2.as_view(), name="streamplatform-cbv-try2"),
    path('streamplatform-detail-cbv-try2/<int:pk>/', views.StreamPlatformDetailView2.as_view(), name="streamplatform-detail-cbv-try2"),
    
    # Using HyperlinkedModelSerializer for the views
    path('watchlist-cbv-try3/', views.WatchlistCBView3.as_view(), name="watchlist-cbv-try3"),
    path('watchlist-detail-cbv-try3/<int:pk>/', views.WatchlistDetailCBView3.as_view(), name="watchlist-detail-cbv-try3"),
    path('streamplatform-detail-cbv-try3/<int:pk>/', views.StreamPlatformDetailView3.as_view(), name="streamplatform-detail-cbv-try3"),
    
    # Using ListSerializer for the views
    path('watchlist-cbv-try4/', views.WatchlistCBView4.as_view(), name="watchlist-cbv-try4"),
    
    # Using BaseSerializer for the views
    path('watchlist-cbv-try5/', views.WatchlistCBView5.as_view(), name="watchlist-cbv-try5"),
    
    # Using GenericAPIView for the views
    path('watchlist-cbv-try6/', views.WatchlistCBView6.as_view(), name="watchlist-cbv-try6"),
    path('watchlist-detail-cbv-try6/<str:title>/', views.WatchlistDetailVBView6.as_view(), name="watchlist-detail-cbv-try6"),
    
    #Using ListModelMixin and GenericAPIView for views
    path('watchlist-cbv-try7/', views.WatchlistCBView7.as_view(), name="watchlist-cbv-try7"),
    
    #Using CreateModelMixin and GenericAPIView for views
    path('watchlist-cbv-try8/', views.WatchlistCBView8.as_view(), name="watchlist-cbv-try8"),    
    
    #Using RetrieveModelMixin and GenericAPIView for views
    path('watchlist-cbv-try9/<int:pk>/', views.WatchlistCBView9.as_view(), name="watchlist-cbv-try9"),
    
    #Using UpdateModelMixin and GenericAPIView for views
    path('watchlist-cbv-try10/<int:pk>/', views.WatchlistCBView10.as_view(), name="watchlist-cbv-try10"),
    
    #Using DestroyModelMixin and GenericAPIView for views
    path('watchlist-cbv-try11/<int:pk>/', views.WatchlistCBView11.as_view(), name="watchlist-cbv-try11"),
    
    #Using CreateAPIView for views
    path('watchlist-cbv-try12/', views.WatchlistCBView12.as_view(), name="watchlist-cbv-try12"),
    
    #Using ListAPIView for views
    path('watchlist-cbv-try13/', views.WatchlistCBView13.as_view(), name="watchlist-cbv-try13"),
    
    #Using RetrieveAPIView for views
    path('watchlist-cbv-try14/<str:title>/', views.WatchlistCBView14.as_view(), name="watchlist-cbv-try14"),
    
    #Using DestroyAPIView for views
    path('watchlist-cbv-try15/<str:title>/', views.WatchlistCBView15.as_view(), name="watchlist-cbv-try15"),
    
    #Using UpdateAPIView
    path('watchlist-cbv-try16/<int:pk>/', views.WatchlistCBView16.as_view(), name="watchlist-cbv-try16"),
    
    #Using ListCreateAPIView for views
    path('watchlist-cbv-try17/', views.WatchlistCBView17.as_view(), name="watchlist-cbv-try17"),
    
    #Using RetrieveUpdateAPIView
    path('watchlist-cbv-try18/<int:pk>/', views.WatchlistCBView18.as_view(), name="watchlist-cbv-try18"),
    
    #Using RetrieveDestroyAPIView
    path('watchlist-cbv-try19/<int:pk>/', views.WatchlistCBView19.as_view(), name="watchlist-cbv-try19"),
    
    #Using RetrieveUpdateDestroyAPIView
    path('watchlist-cbv-try20/<int:pk>/', views.WatchlistCBView20.as_view(), name="watchlist-cbv-try20"),
    
    #Using MultipleFieldLookupMixin
    path('watchlist-cbv-try21/<str:title>/', views.WatchlistCBView21.as_view(), name='watchlist-cbv-try21'),
    
    #Using Custom Base class for views
    path('watchlist-cbv-try22/', views.WatchlistCBView22.as_view(), name="watchlist-cbv-try22"),
    path('watchlist-cbv-try23/', views.WatchlistCBView23.as_view(), name="watchlist-cbv-try23"),
    
]
