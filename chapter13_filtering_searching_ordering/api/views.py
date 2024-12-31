from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from chapter3_project_setup.models import WatchList, Review
from chapter13_filtering_searching_ordering.api import serializers
from chapter13_filtering_searching_ordering.api.filters import IsReviewOwnerFilterBackend, WatchlistCategoryFilter

#Filtering against the current user----------------------------------------------------
class ReviewsListCurrentUserFilterView(generics.ListAPIView):
    serializer_class = serializers.ReviewModelSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Return reviews where `review_user` matches the current user
        return Review.objects.filter(review_user=self.request.user)
    
#Filtering against the URL---------------------------------------------------------------
class ReviewListUrlFilterView(generics.ListAPIView):
    serializer_class = serializers.ReviewModelSerializer

    def get_queryset(self):
        # Extract 'watchlist_id' from the URL using 'self.kwargs'
        watchlist_id = self.kwargs['watchlist_id']
        # Filter reviews that are related to the specified watchlist
        return Review.objects.filter(watchlist_id=watchlist_id)
    
class ReviewsUrlFilterWithValidationView(generics.ListAPIView):
    serializer_class = serializers.ReviewModelSerializer

    def get_queryset(self):
        # Extract 'watchlist_id' from the URL
        watchlist_id = self.kwargs['watchlist_id']
        
        # Ensure 'watchlist_id' corresponds to an existing WatchList
        watchlist = get_object_or_404(WatchList, id=watchlist_id)
        
        # If the WatchList exists, filter reviews by 'watchlist_id'
        return Review.objects.filter(watchlist=watchlist)

    def list(self, request, *args, **kwargs):
        # Custom response to handle the case where no reviews exist
        queryset = self.get_queryset()
        if not queryset.exists():
            return Response({"detail": "No reviews found for the specified watchlist."}, status=status.HTTP_404_NOT_FOUND)
        return super().list(request, *args, **kwargs)
    
#Filtering against query parameters----------------------------------------------
class ReviewsFilterQueryParamsView(generics.ListAPIView):
    serializer_class = serializers.ReviewModelSerializer

    def get_queryset(self):
        # Start with the base queryset for all reviews
        queryset = Review.objects.all()

        # Get query parameters from the request
        rating = self.request.query_params.get('rating')
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')

        # Apply filters based on query parameters if they are present
        if rating is not None:
            queryset = queryset.filter(rating=rating)

        if start_date is not None:
            queryset = queryset.filter(review_date__gte=start_date)

        if end_date is not None:
            queryset = queryset.filter(review_date__lte=end_date)

        return queryset
    
#Generic Filtering-----------------------------------------------------------------------
class ReviewsGenericFilteringView(generics.ListAPIView):
    queryset = Review.objects.all()
    serializer_class = serializers.ReviewModelSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['rating', 'review_user', 'active']  # Fields to filter on

#Overriding the initial queryset-----------------------------------------------------------
class ReviewsOverridingQuerysetView(generics.ListAPIView):
    serializer_class = serializers.ReviewModelSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['rating', 'active']

    def get_queryset(self):
        """
        Optionally restricts the returned reviews to only those related to the
        currently authenticated user.
        """
        user = self.request.user
        if user.is_authenticated:
            # Filter reviews where the `review_user` is the currently authenticated user
            return Review.objects.filter(review_user=user)
        # For unauthenticated users, you can return an empty queryset or handle it differently
        return Review.objects.none()
    
#searchFilter---------------------------------------------------------------------
class WatchlistSearchFilterView(generics.ListAPIView):
    queryset = WatchList.objects.all()
    serializer_class = serializers.WatchListModelSerializer
    filter_backends = [SearchFilter]
    search_fields = ['title', 'storyline']    

#----------------------
class WatchlistAdvacedSearchView(generics.ListAPIView):
    queryset = WatchList.objects.all()
    serializer_class = serializers.WatchListModelSerializer
    filter_backends = [SearchFilter]
    search_fields = [
        'title',  # Default behavior: partial match, case insensitive
        '^title',  # Starts-with search for titles
        '=platform__name',  # exact match for platform name
        '$storyline'  # regex search on storyline
    ]
    
#-------------------------------------------------------------------
class CustomSearchFilter(SearchFilter):
    def get_search_fields(self, view, request):
        # Dynamically adjust search fields based on a query parameter
        if request.query_params.get('title_only'):
            return ['title']
        return super().get_search_fields(view, request)

# Applying the custom filter
class WatchlistDynamicSearchFieldView(generics.ListAPIView):
    queryset = WatchList.objects.all()
    serializer_class = serializers.WatchListModelSerializer
    filter_backends = [CustomSearchFilter]
    search_fields = ['title', 'storyline']
    
#OrderingFilter=====================================================
class WatchListOrderingView(generics.ListAPIView):
    queryset = WatchList.objects.all()
    serializer_class = serializers.WatchListModelSerializer
    filter_backends = [OrderingFilter]
    ordering_fields = ['title', 'imdb_rating', 'created', 'episodes', 'platform__name']
    
#-------------------------------------------------------
class WatchListFullOrderingView(generics.ListAPIView):
    queryset = WatchList.objects.all()
    serializer_class = serializers.WatchListModelSerializer
    filter_backends = [OrderingFilter]
    ordering_fields = '__all__'  # Allow ordering on all fields
    
#----------------------------------------------------
class WatchlistOrderedView(generics.ListAPIView):
    queryset = WatchList.objects.all()
    serializer_class = serializers.WatchListModelSerializer
    filter_backends = [OrderingFilter]
    ordering_fields = ['title', 'imdb_rating', 'created', 'category']  # Allowed ordering fields
    ordering = ['imdb_rating']  # Default: Order by IMDB rating (ascending)
    
#----------------------------------------------------------------
class UserReviewListView(generics.ListAPIView):
    """
    View to list all reviews created by the logged-in user, with optional filtering by watchlist.
    """
    queryset = Review.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.ReviewModelSerializer
    filter_backends = [IsReviewOwnerFilterBackend, SearchFilter]
    search_fields = ['watchlist__title']
    
#--------------------------------------------------------------------
class WatchlistCategoryFilterView(generics.ListAPIView):
    """
    API endpoint to list Watchlist objects, with filtering by category.
    Includes a browsable API interface for category selection.
    """
    queryset = WatchList.objects.all()
    serializer_class = serializers.WatchListModelSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    filter_backends = [WatchlistCategoryFilter, SearchFilter]
    search_fields = ['title', 'storyline']
    
