from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.authentication import BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from chapter3_project_setup.models import WatchList, Review, StreamPlatform
from . import serializers


class WatchListViewSet1(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]  # Ensure that the user is authenticated
    queryset = WatchList.objects.all()
    serializer_class = serializers.WatchListModelSerializer
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([BasicAuthentication])
def stream_platform_view(request, format=None):
    content = {
        'status': 'request was permitted'
    }
    return Response(content)
    
class StreamPlatformViewSet1(viewsets.ModelViewSet):
    queryset = StreamPlatform.objects.all()
    serializer_class = serializers.StreamPlatformModelSerializer
    
class ReviewViewSet1(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = serializers.ReviewModelSerializer
    
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
        