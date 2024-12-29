from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.authentication import BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework import status
from chapter3_project_setup.models import WatchList, Review, StreamPlatform
from chapter9_authentication.api import serializers


class WatchListViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]  # Ensure that the user is authenticated
    queryset = WatchList.objects.all()
    serializer_class = serializers.WatchListModelSerializer
    
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])  # Require authentication
@authentication_classes([TokenAuthentication])  # Token-based authentication
def streamplatform_list(request):
    # Handle GET requests
    if request.method == 'GET':
        platforms = StreamPlatform.objects.all()
        serializer = serializers.StreamPlatformModelSerializer(platforms, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    # Handle POST requests
    elif request.method == 'POST':
        serializer = serializers.StreamPlatformModelSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])  # Require authentication
@authentication_classes([TokenAuthentication])  # Token-based authentication
def streamplatform_detail(request, pk):
    try:
        platform = StreamPlatform.objects.get(pk=pk)
    except StreamPlatform.DoesNotExist:
        return Response({"error": "StreamPlatform not found."}, status=status.HTTP_404_NOT_FOUND)

    # Handle GET request
    if request.method == 'GET':
        serializer = serializers.StreamPlatformModelSerializer(platform, context={'request': request})
        return Response(serializer.data)

    # Handle PUT request
    elif request.method == 'PUT':
        serializer = serializers.StreamPlatformModelSerializer(platform, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Handle DELETE request
    elif request.method == 'DELETE':
        platform.delete()
        return Response({"message": "StreamPlatform deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
    
class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = serializers.ReviewModelSerializer
    authentication_classes = [TokenAuthentication,]
    permission_classes = [IsAuthenticated,]  # Ensure that the user is authenticated
    
    def perform_create(self, serializer):
        pk = self.kwargs.get('pk')
        watchlist = WatchList.objects.get(pk=pk)

        review_user = self.request.user
        review_queryset = Review.objects.filter(watchlist=watchlist, review_user=review_user)

        if review_queryset.exists():
            raise ValidationError("You have already reviewed this movie!")

        if watchlist.number_rating == 0:
            watchlist.imdb_rating = serializer.validated_data['rating']
        else:
            watchlist.imdb_rating = (watchlist.imdb_rating + serializer.validated_data['rating'])/2

        watchlist.number_rating = watchlist.number_rating + 1
        watchlist.save()

        serializer.save(watchlist=watchlist, review_user=review_user)
