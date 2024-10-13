from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.authentication import BasicAuthentication, TokenAuthentication
from rest_framework import permissions
from chapter3_project_setup.models import WatchList, Review, StreamPlatform
from . import serializers


class WatchListViewSet1(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]  # Ensure that the user is authenticated
    queryset = WatchList.objects.all()
    serializer_class = serializers.WatchListModelSerializer
    
class StreamPlatformViewSet1(viewsets.ModelViewSet):
    queryset = StreamPlatform.objects.all()
    serializer_class = serializers.StreamPlatformModelSerializer
    
class ReviewViewSet1(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = serializers.ReviewModelSerializer
    
    def perform_create(self, serializer):
        pk = self.kwargs.get("pk")
        watchlist = WatchList.objects.get(pk=pk)
        review_user = self.request.user
        
        review_queryset = Review.objects.filter(watchlist=watchlist, review_user=review_user)
        if review_queryset.exists():
            raise ValidationError("You have already reviewed this watchlist")
        
        serializer.save(watchlist=watchlist, review_user=review_user)
        