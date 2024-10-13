from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework import generics
from rest_framework import filters
from rest_framework.pagination import PageNumberPagination
from rest_framework import mixins
from rest_framework.decorators import action
from django.db import transaction
from chapter3_project_setup.models import WatchList, Review, StreamPlatform
from . import serializers


#=======================Views using ViewSets======================
class WatchListViewSet1(viewsets.ViewSet):
    queryset = WatchList.objects.all()
    def list(self, request):        
        serializer = serializers.WatchListModelSerializer(self.queryset, many=True, context={"request":request})
        return Response(serializer.data)

    def create(self, request):
        serializer = serializers.WatchListModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        watchlist = generics.get_object_or_404(self.queryset, pk=pk)
        serializer = serializers.WatchListModelSerializer(watchlist, context={"request":request})
        return Response(serializer.data)

    def update(self, request, pk=None):
        watchlist = generics.get_object_or_404(self.queryset, pk=pk)
        serializer = serializers.WatchListModelSerializer(watchlist, data=request.data, context={"request":request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        watchlist = generics.get_object_or_404(self.queryset, pk=pk)
        serializer = serializers.WatchListModelSerializer(watchlist, data=request.data, partial=True, context={"request":request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        watchlist = generics.get_object_or_404(self.queryset, pk=pk)
        watchlist.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    @action(detail=False, methods=['get'])
    def watchlist_count(self, request):
        movies = WatchList.objects.filter(category="MOVIE").count()
        series = WatchList.objects.filter(category="SERIES").count()
        return Response({"movies":movies, "series":series})

#=======================Views using GenericViewSet======================
class WatchListViewSet2(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    queryset = WatchList.objects.all()
    serializer_class = serializers.WatchListModelSerializer
    
    def get_queryset(self):
        # Custom queryset logic, e.g., applying filters or ordering
        return WatchList.objects.filter(active=True).order_by('title')

    # Custom action to mark a watchlist item as 'inactive'
    @action(detail=False, methods=['get'])
    def watchlist_count(self, request):
        movies = WatchList.objects.filter(category="MOVIE").count()
        series = WatchList.objects.filter(category="SERIES").count()
        return Response({"movies":movies, "series":series})
    
#=======================Views using ModelViewSet======================
class WatchListViewSet3(viewsets.ModelViewSet):
    queryset = WatchList.objects.all()
    serializer_class = serializers.WatchListModelSerializer
    
    def get_queryset(self):
        # Custom queryset logic, e.g., applying filters or ordering
        return WatchList.objects.filter(active=True).order_by('title')

    # Custom action to get summary information
    @action(detail=False, methods=['get'])
    def watchlist_count(self, request):
        movies = WatchList.objects.filter(category="MOVIE").count()
        series = WatchList.objects.filter(category="SERIES").count()
        return Response({"movies":movies, "series":series})
    
    
class StreamPlatformViewSet3(viewsets.ModelViewSet):
    queryset = StreamPlatform.objects.all()
    serializer_class = serializers.StreamPlatformModelSerializer
    
    @action(detail=True, url_path="watchlist", url_name="watchlist")
    def get_watchlist(self, request, pk=None):
        try:
            stream_platform = self.get_object()
            serializer = serializers.WatchListModelSerializer(stream_platform.watchlist, many=True, context={"request":request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)    
        
    @get_watchlist.mapping.put
    def update_streamplatform(self, request, pk=None, *args, **kwargs):
        try:
            partial = kwargs.pop('partial', False)
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)

            if getattr(instance, '_prefetched_objects_cache', None):
                # If 'prefetch_related' has been applied to a queryset, we need to
                # forcibly invalidate the prefetch cache on the instance.
                instance._prefetched_objects_cache = {}

            return Response(serializer.data)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post', 'put'], url_path="bulk-update", url_name="bulk_update")
    def bulk_update(self, request):
        # Implement the logic for bulk updates here
        data = request.data

        # Extract a list of IDs and corresponding updates
        ids_to_update = [item['id'] for item in data]
        updates = {item['id']: item for item in data}

        # Perform bulk updates
        try:
            with transaction.atomic():
                for streamplatform_item in StreamPlatform.objects.filter(id__in=ids_to_update):
                    update_data = updates.get(streamplatform_item.id)
                    if update_data:
                        streamplatform_item.name = update_data.get('name', streamplatform_item.name)
                        streamplatform_item.about = update_data.get('about', streamplatform_item.about)
                        streamplatform_item.website = update_data.get('website', streamplatform_item.website)
                        # Add more fields to update as needed
                        streamplatform_item.save()
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'message': 'Bulk update successful'})
    
    @action(detail=False, methods=['delete'], url_path="bulk-delete", url_name="bulk_delete")
    def bulk_delete(self, request):
        # Implement the logic for bulk deletes here
        data = request.data

        # Extract a list of IDs to delete
        ids_to_delete = [item['id'] for item in data]

        # Perform bulk deletes
        try:
            StreamPlatform.objects.filter(id__in=ids_to_delete).delete()
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'message': 'Bulk delete successful'})
    
    
    
    
    
#=======================Views using ReadOnlyModelViewSet======================
class WatchListViewSet4(viewsets.ReadOnlyModelViewSet):
    queryset = WatchList.objects.all()
    serializer_class = serializers.WatchListModelSerializer
    
#=======================Views using ModelViewSet======================
class WatchListViewSet5(viewsets.ModelViewSet):
    queryset = WatchList.objects.all()
    serializer_class = serializers.WatchListHyperlinkedModelSerializer1
    
class StreamPlatformViewSet5(viewsets.ModelViewSet):
    queryset = StreamPlatform.objects.all()
    serializer_class = serializers.StreamPlatformHyperlinkedModelSerializer1


################################Function Based Views##############################
@api_view(['GET', 'POST'])
def WatchlistFunctionView(request):
    if request.method == 'GET':
        watchlist = WatchList.objects.all()
        serializer = serializers.WatchlistSerializer(watchlist, many=True)
        # Handle GET request
        data = {'message': 'This is a GET request'}
        return Response(serializer.data)
    elif request.method == 'POST':
        # Handle POST request
        data = {'message': 'This is a POST request'}
        return Response(data)
    
    