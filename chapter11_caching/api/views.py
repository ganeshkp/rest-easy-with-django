from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie, vary_on_headers
from django.core.cache import cache
from chapter3_project_setup.models import WatchList
from chapter11_caching.api import serializers
from chapter11_caching.api.mixins import CacheMixin

User = get_user_model()

#----------------------------------------------------------------
class WatchlistCachingView(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication,]
    permission_classes = [IsAuthenticated]  # Ensure that the user is authenticated
    queryset = WatchList.objects.all()
    serializer_class = serializers.WatchListModelSerializer
    
    @method_decorator(cache_page(60 * 15))  # Cache for 15 minutes
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @method_decorator(cache_page(60 * 15))  # Cache for 15 minutes
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
# List View for WatchList with 15 minutes caching
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@cache_page(60 * 15)  # Cache for 15 minutes
def watchlist_list_view(request):
    queryset = WatchList.objects.all()
    serializer = serializers.WatchListModelSerializer(queryset, many=True)
    return Response(serializer.data)

# Retrieve View for WatchList with 15 minutes caching
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@cache_page(60 * 15)  # Cache for 15 minutes
def watchlist_detail_view(request, pk):
    try:
        watchlist_item = WatchList.objects.get(pk=pk)
    except WatchList.DoesNotExist:
        return Response({"error": "WatchList item not found"}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = serializers.WatchListModelSerializer(watchlist_item)
    return Response(serializer.data)

#--------------------------------------------------
#low level caching
class WatchLowLevelCachingView(APIView):
    def get(self, request):
        cached_data = cache.get("watchlist_data")
        if not cached_data:
            # Expensive database query or operation
            queryset = WatchList.objects.all()
            serializer = serializers.WatchListModelSerializer(queryset, many=True)
            cached_data = serializer.data
            cache.set("watchlist_data", cached_data, timeout=60*15)
        return Response(cached_data)
    

class WatchListObjectLevelCachingView(APIView):
    def get(self, request, pk):
        cache_key = f"watchlist_{pk}"
        cached_data = cache.get(cache_key)
        if not cached_data:
            try:
                watchlist_item = WatchList.objects.get(pk=pk)
                cached_data = serializers.WatchListModelSerializer(watchlist_item).data
                cache.set(cache_key, cached_data, timeout=60*15)
            except WatchList.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(cached_data)

#---------------------------------------------------
class WatchListCacheMixinListView(CacheMixin, APIView):
    def get(self, request):
        cache_key = "watchlist_all"  # Define a unique cache key for the list view
        queryset = self.get_cached_response(cache_key, WatchList.objects.all())
        serializer = serializers.WatchListModelSerializer(queryset, many=True)
        return Response(serializer.data)
    
class WatchListCacheMixinDetailView(CacheMixin, APIView):
    def get(self, request, pk):
        cache_key = f"watchlist_{pk}"  # Define a unique cache key per watchlist object
        try:
            queryset = self.get_cached_response(
                cache_key, WatchList.objects.get(id=pk)
            )
        except WatchList.DoesNotExist:
            return Response(
                {"error": "WatchList item not found"}, status=status.HTTP_404_NOT_FOUND
            )
        serializer = serializers.WatchListModelSerializer(queryset)
        return Response(serializer.data)
    
#------------------------------------------------------------------------
class WatchListVaryOnHeaderCacheView(APIView):
    authentication_classes = [TokenAuthentication,]
    permission_classes = [IsAuthenticated]  # Only authenticated users can access

    # Apply caching for 15 minutes and vary based on Authorization header
    @method_decorator(cache_page(60 * 15))  # Cache response for 15 minutes
    @method_decorator(vary_on_headers("Authorization"))
    def get(self, request):
        # Cache key is created internally by cache_page; varying on Authorization
        watchlist_items = WatchList.objects.all()
        serializer = serializers.WatchListModelSerializer(watchlist_items, many=True)
        return Response(serializer.data)
    
#-----------------------------------------------------------------
class WatchListVaryOnCookieCacheView(APIView):
    # Apply caching for 15 minutes and vary based on the user's session cookie
    @method_decorator(cache_page(60 * 15))  # Cache response for 15 minutes
    @method_decorator(vary_on_cookie)
    def get(self, request):
        # This will cache separate responses for each unique cookie value
        watchlist_items = WatchList.objects.all()
        serializer = serializers.WatchListModelSerializer(watchlist_items, many=True)
        return Response(serializer.data)
