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
from chapter6_serializers_views.api.mixins import MultipleFieldLookupMixin, TotalEpisodesMixin

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
        serializer = serializers.WatchListModelSerializer(data=request.data)
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

        serializer = serializers.StreamPlatformModelSerializer(platform)
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
        serializer = serializers.WatchlistDemoListSerializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def put(self, request, format=None):
        serializer = serializers.WatchlistDemoListSerializer(data=request.data, many=True)
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