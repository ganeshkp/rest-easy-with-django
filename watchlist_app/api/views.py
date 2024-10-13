from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework import generics
from rest_framework import filters
from rest_framework.pagination import PageNumberPagination
from rest_framework import mixins
from rest_framework.decorators import action
from django.db import transaction

from django.http import Http404
from chapter3_project_setup.models import WatchList, Review, StreamPlatform
from . import serializers
from watchlist_app.api.mixins import MultipleFieldLookupMixin, TotalEpisodesMixin

################################Class Based Views##############################

#=============Views Using Basic Serializer=================
class WatchlistCBView1(APIView):
    """
    View to list all Movies in the system.
    """
    def get(self, request, format=None):
        """
        Return a list of all watchlist.
        """
        watchlist = WatchList.objects.all()
        serializer = serializers.WatchlistSerializer(watchlist, many = True, context={'request': request})
        return Response(serializer.data)
    
    def post(self, request, format=None):
        """
        Create a new watchlist.
        """
        serializer = serializers.WatchlistSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class WatchlistDetailCBView1(APIView):
    """
    View in detail individual Watchlist in the system.
    """
    def get(self, request, pk, format=None):
        try:
            watchlist = WatchList.objects.get(pk=pk)
            serializer = serializers.WatchlistSerializer(watchlist)
            return Response(serializer.data)
        except WatchList.DoesNotExist:
            raise Http404
        
    def put(self, request, pk):
        try:
            watchlist = WatchList.objects.get(pk=pk)
            serializer = serializers.WatchlistSerializer(watchlist, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except WatchList.DoesNotExist:
            raise Http404

    def patch(self, request, pk):
        try:
            watchlist = WatchList.objects.get(pk=pk)
            serializer = serializers.WatchlistSerializer(watchlist, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        except WatchList.DoesNotExist:
            raise Http404
        
    def delete(self, request, pk):
        try:
            watchlist = WatchList.objects.get(pk=pk)
            watchlist.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as err:
            raise Http404
        
class StreamPlatformDetailView1(APIView):
    """
    Stream Platform Detail View
    """
    
    def get(self, request, pk):
        try:
            platform = StreamPlatform.objects.get(pk=pk)
        except StreamPlatform.DoesNotExist:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = serializers.StreamPlatformSerializer(platform)
        return Response(serializer.data)
        
class ReviewlistCBView1(APIView):
    """
    View to list all Reviews in the system.
    """
    def get(self, request, format=None):
        """
        Return a list of all watchlist.
        """
        reviews = Review.objects.all()
        serializer = serializers.ReviewSerializer(reviews, many = True)
        return Response(serializer.data)
    
    
#=============Views Using ModelSerializer=================
class WatchlistCBView2(APIView):
    """
    View to list all Movies in the system.
    """
    def get(self, request, format=None):
        """
        Return a list of all watchlist.
        """
        watchlist = WatchList.objects.all()
        serializer = serializers.WatchListModelSerializer(watchlist, many = True, context={'request': request})
        return Response(serializer.data)
    
    def post(self, request, format=None):
        """
        Create a new watchlist.
        """
        serializer = serializers.WatchListModelSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class StreamPlatformListView2(APIView):
    """
    Stream Platform List View
    """
    
    def get(self, request, format=None):
        """
        Return a list of all watchlist.
        """
        watchlist = StreamPlatform.objects.all()
        serializer = serializers.StreamPlatformModelSerializer(watchlist, many = True, context={'request': request})
        return Response(serializer.data)
    
    def post(self, request, format=None):
        """
        Create a new watchlist.
        """
        serializer = serializers.StreamPlatformModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class StreamPlatformDetailView2(APIView):
    """
    Stream Platform Detail View
    """
    
    def get(self, request, pk):
        try:
            platform = StreamPlatform.objects.get(pk=pk)
        except StreamPlatform.DoesNotExist:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = serializers.StreamPlatformModelSerializer(platform, context={'request': request})
        return Response(serializer.data)
        
class ReviewlistCBView2(APIView):
    """
    View to list all Reviews in the system.
    """
    def get(self, request, format=None):
        """
        Return a list of all watchlist.
        """
        reviews = Review.objects.all()
        serializer = serializers.ReviewModelSerializer(reviews, many = True)
        return Response(serializer.data)
        
#=============Views Using HyperLinkedModelSerializer=================
class WatchlistCBView3(APIView):
    """
    View to list all Movies in the system.
    """
    def get(self, request, format=None):
        """
        Return a list of all watchlist.
        """
        watchlist = WatchList.objects.all()
        serializer = serializers.WatchListHyperlinkedModelSerializer(watchlist, many = True, context={'request': request})
        return Response(serializer.data)
    
    def post(self, request, format=None):
        """
        Create a new watchlist.
        """
        serializer = serializers.WatchListHyperlinkedModelSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class WatchlistDetailCBView3(APIView):
    """
    View in detail individual Watchlist in the system.
    """
    def get(self, request, pk, format=None):
        try:
            watchlist = WatchList.objects.get(pk=pk)
            serializer = serializers.WatchListHyperlinkedModelSerializer(watchlist, context={'request': request})
            return Response(serializer.data)
        except WatchList.DoesNotExist:
            raise Http404
        

class StreamPlatformDetailView3(APIView):
    """
    Stream Platform Detail View
    """
    
    def get(self, request, pk):
        try:
            platform = StreamPlatform.objects.get(pk=pk)
        except StreamPlatform.DoesNotExist:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = serializers.StreamPlatformHyperlinkedModelSerializer(platform, context={'request': request})
        return Response(serializer.data)
  
#=============Views Using ListModelSerializer=================
class WatchlistCBView4(APIView):
    """
    View to list all Movies in the system.
    """
    def get(self, request, format=None):
        """
        Return a list of all watchlist.
        """
        watchlist = WatchList.objects.all()
        serializer = serializers.WatchlistDemoListSerializer(watchlist, many = True, context={'request': request})
        return Response(serializer.data)
    
    def post(self, request, format=None):
        """
        Create a new watchlist.
        """
        serializer = serializers.WatchlistDemoListSerializer(data=request.data, many=True, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def put(self, request, format=None):
        serializer = serializers.WatchlistDemoListSerializer(data=request.data, many=True, context={'request': request})
        serializer.is_valid(raise_exception=True)

        # Perform the bulk update
        serializer.save()

        return Response(serializer.data)


#=============Views Using BaseSerializer=================
class WatchlistCBView5(APIView):
    """
    View to list all Movies in the system.
    """
    def get(self, request, format=None):
        """
        Return a list of all watchlist.
        """
        watchlist = WatchList.objects.all()
        serializer = serializers.WatchlistBaseSerializer(watchlist, many = True)
        return Response(serializer.data)
    
    def post(self, request, format=None):
        """
        Create a new watchlist.
        """
        serializer = serializers.WatchlistBaseSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

#=============Views Using GenericAPIView=================
class WatchlistCBView6(generics.GenericAPIView):
    queryset = WatchList.objects.all()
    serializer_class = serializers.WatchListModelSerializer
    pagination_class = PageNumberPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]  # Set the filter backends
    
    # Specify the fields that can be used for search and ordering
    search_fields = ['title','imdb_rating']
    ordering_fields = ['title', 'imdb_rating', 'created']
    
    def get_queryset(self):
        # Custom queryset logic, e.g., applying filters or ordering
        return WatchList.objects.filter(active=True).order_by('title')
    
    def get_serializer_class(self):
        # Determine the serializer class based on the request method
        if self.request.method == 'POST':
            return serializers.WatchListModelSerializer
        elif self.request.method == 'GET':
            return serializers.WatchlistModelBasicSerializer
    
    def get(self, request, *args, **kwargs):
        """
        Return a list of all watchlist.
        """
        watchlist = self.filter_queryset(self.get_queryset())  # Apply search filter
        serializer_class = self.get_serializer_class()
        page = self.paginate_queryset(watchlist)
        if page is not None:            
            serializer = serializer_class(watchlist, many=True, context=self.get_serializer_context())
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(watchlist, many=True)
        return Response(serializer.data)
    
    def post(self, request, *args, **kwargs):
        """
        Create a new watchlist.
        """
        serializer_class = self.get_serializer_class(data=request.data)
        serializer = serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def get_serializer_context(self):
        context = super().get_serializer_context()
        # You can add more context data here
        context["name"] = "TEST"
        return context
    
    
class WatchlistDetailVBView6(generics.GenericAPIView):
    queryset = WatchList.objects.all()
    serializer_class = serializers.WatchListModelSerializer
    lookup_field = "title" # Set the lookup field to 'title' or any other field you prefer
    lookup_url_kwarg = 'title'

    # Specify the fields that can be used for search and ordering
    search_fields = ['title','imdb_rating']
    ordering_fields = ['title', 'imdb_rating', 'created']
    
    def get_queryset(self):
        return WatchList.objects.filter(active=True)
    
    def filter_queryset(self, queryset):
        # Apply filters based on the lookup field (e.g., title)
        filter_kwargs = {self.lookup_field: self.kwargs[self.lookup_field]}
        queryset = queryset.filter(**filter_kwargs)
        return queryset
    
    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        filter_kwargs = {self.lookup_field: self.kwargs[self.lookup_field]}  # Assuming URL pattern captures 'title'
        obj = generics.get_object_or_404(queryset, **filter_kwargs)
        return obj

    def get(self, request, *args, **kwargs):
        instance = self.get_object()  # Retrieve the instance using get_object
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
#=======================Views using ListModelMixin and GenericAPIView=====
class WatchlistCBView7(generics.GenericAPIView, mixins.ListModelMixin):
    queryset = WatchList.objects.all()
    serializer_class = serializers.WatchListModelSerializer
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
#=======================Views using CreateModelMixin and GenericAPIView=====
class WatchlistCBView8(generics.GenericAPIView, mixins.CreateModelMixin):
    queryset = WatchList.objects.all()
    serializer_class = serializers.WatchListModelSerializer
    
    def perform_create(self, serializer):
        # Customize the creation process here, e.g., setting additional fields
        # before saving the object to the database.
        serializer.save()

    def post(self,request,*args,  **kwargs):
        return self.create(request, *args, **kwargs)
        
#=======================Views using RetrieveModelMixin and GenericAPIView=====
class WatchlistCBView9(generics.GenericAPIView, mixins.RetrieveModelMixin):
    queryset = WatchList.objects.all()
    serializer_class = serializers.WatchListModelSerializer
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

#=======================Views using UpdateModelMixin and GenericAPIView=====
class WatchlistCBView10(generics.GenericAPIView, mixins.UpdateModelMixin):
    queryset = WatchList.objects.all()
    serializer_class = serializers.WatchListModelSerializer
    
    def perform_update(self, serializer):
        # Customize the update process here, e.g., perform additional
        # actions before saving the updated object.
        serializer.save()  # Saving the updated object
        
    def put(self,request, *args , **kwargs):
        # Use the update method provided by UpdateModelMixin
        return self.update(request, *args, **kwargs)
    
#=======================Views using DestroyModelMixin and GenericAPIView=====
class WatchlistCBView11(generics.GenericAPIView, mixins.DestroyModelMixin):
    queryset = WatchList.objects.all()
    serializer_class = serializers.WatchListModelSerializer
    
    def perform_destroy(self, instance):
        # Customize the destruction process here, e.g., perform additional
        # actions before deleting the object.
        instance.delete()  # Delete the object

    def delete(self,request, *args , **kwargs):
        return self.destroy(request, *args, **kwargs)
    
#=======================Views using CreateAPIView=======================
class WatchlistCBView12(generics.CreateAPIView):
    queryset = WatchList.objects.all()
    serializer_class = serializers.WatchListModelSerializer
    
    def perform_create(self, serializer):
        # Customize the creation process here, e.g., setting additional fields
        # before saving the object to the database.
        serializer.save()

#=======================Views using ListAPIView=======================   
class WatchlistCBView13(generics.ListAPIView):
    queryset = WatchList.objects.all()
    serializer_class = serializers.WatchListModelSerializer

    def get_queryset(self):
        # Customize the queryset here, e.g., apply filters or annotations
        return WatchList.objects.filter(active=True)
    
#=======================Views using RetrieveAPIView====================
class WatchlistCBView14(generics.RetrieveAPIView):
    queryset = WatchList.objects.all()
    serializer_class = serializers.WatchListModelSerializer
    lookup_field = "title" # Set the lookup field to 'title' or any other field you prefer
    
    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        filter_kwargs = {self.lookup_field: self.kwargs[self.lookup_field]}  # Assuming URL pattern captures 'title'
        obj = generics.get_object_or_404(queryset, **filter_kwargs)
        return obj
    
#=======================Views using DestroyAPIView====================
class WatchlistCBView15(generics.DestroyAPIView):
    queryset = WatchList.objects.all()
    serializer_class = serializers.WatchListModelSerializer
    lookup_field = "title" # Set the lookup field to 'title' or any other field you prefer
    
    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        filter_kwargs = {self.lookup_field: self.kwargs[self.lookup_field]}  # Assuming URL pattern captures 'title'
        obj = generics.get_object_or_404(queryset, **filter_kwargs)
        return obj
    
    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({"detail": "WatchList object deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
    
#=======================Views using UpdateAPIView======================
class WatchlistCBView16(generics.UpdateAPIView):
    queryset = WatchList.objects.all()
    serializer_class = serializers.WatchListModelSerializer
    
#=======================Views using ListCreateAPIView======================
class WatchlistCBView17(generics.ListCreateAPIView):
    queryset = WatchList.objects.all()
    serializer_class = serializers.WatchListModelSerializer
    
#=======================Views using RetrieveUpdateAPIView======================
class WatchlistCBView18(generics.RetrieveUpdateAPIView):
    queryset = WatchList.objects.all()
    serializer_class = serializers.WatchListModelSerializer
    
#=======================Views using RetrieveDestroyAPIView======================
class WatchlistCBView19(generics.RetrieveDestroyAPIView):
    queryset = WatchList.objects.all()
    serializer_class = serializers.WatchListModelSerializer
    
#=======================Views using RetrieveUpdateDestroyAPIView======================
class WatchlistCBView20(generics.RetrieveUpdateDestroyAPIView):
    queryset = WatchList.objects.all()
    serializer_class = serializers.WatchListModelSerializer

#=======================Views using MultipleFieldLookupMixin======================
class WatchlistCBView21(MultipleFieldLookupMixin, generics.RetrieveAPIView):
    """
    Retrieve a WatchList object using multiple field lookup.
    """
    queryset = WatchList.objects.all()
    serializer_class = serializers.WatchListModelSerializer

    # Define the fields to use for multiple field lookup
    lookup_fields = ['title']  # Customize this based on your needs

    # Optionally, you can override other methods or add custom behavior as needed.
    
#=======================Views using Custom Base class======================
class WatchListBaseView1():
    """
    Custom base view class for WatchList.
    """
    queryset = WatchList.objects.all()
    serializer_class = serializers.WatchListModelSerializer
    
class WatchlistCBView22(WatchListBaseView1, generics.ListAPIView):
    """
    View to list Watchlist or to create a new watchlist
    """
    pass
    # Add view-specific logic here


class WatchlistCBView23(WatchListBaseView1, generics.CreateAPIView):
    """
    View to list Watchlist or to create a new watchlist
    """
    pass
    # Add view-specific logic here
    
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
    
    