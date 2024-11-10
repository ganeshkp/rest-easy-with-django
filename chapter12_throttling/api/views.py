from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle, ScopedRateThrottle
from chapter3_project_setup.models import WatchList, StreamPlatform, Review
from chapter11_caching.api import serializers
from chapter12_throttling.api.throttling import CustomCacheRateThrottle, ExceptionCustomMessageThrottle

#----------------------------------------------------------------
class WatchlistThrottlingView(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication,]
    permission_classes = [IsAuthenticated]  # Ensure that the user is authenticated
    queryset = WatchList.objects.all()
    serializer_class = serializers.WatchListModelSerializer
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    
class StreamPlatformThrottlingView(viewsets.ModelViewSet):
    queryset = StreamPlatform.objects.all()
    serializer_class = serializers.StreamPlatformModelSerializer
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    
class ReviewThrottlingView(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = serializers.ReviewModelSerializer
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    
#-----------------------ScopedRateThrottle----------------
class WatchlistScopedRateThrottleView(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication,]
    permission_classes = [IsAuthenticated]  # Ensure that the user is authenticated
    queryset = WatchList.objects.all()
    serializer_class = serializers.WatchListModelSerializer
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'watchlist'  # Set a scope name for this view
    
#-----------------------Custom Throttle---------------------
class WatchlistCustomThrottleView(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication,]
    permission_classes = [IsAuthenticated]  # Ensure that the user is authenticated
    queryset = WatchList.objects.all()
    serializer_class = serializers.WatchListModelSerializer
    throttle_classes = [CustomCacheRateThrottle, ExceptionCustomMessageThrottle]
