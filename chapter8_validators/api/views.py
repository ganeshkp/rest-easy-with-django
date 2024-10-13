from rest_framework import viewsets
from chapter3_project_setup.models import WatchList, Review, StreamPlatform
from . import serializers

class WatchListViewSet1(viewsets.ModelViewSet):
    queryset = WatchList.objects.all()
    serializer_class = serializers.WatchListModelSerializer
    
class StreamPlatformViewSet1(viewsets.ModelViewSet):
    queryset = StreamPlatform.objects.all()
    serializer_class = serializers.StreamPlatformModelSerializer
    
class ReviewViewSet1(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = serializers.ReviewModelSerializer