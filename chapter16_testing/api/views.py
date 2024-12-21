from rest_framework import viewsets
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from chapter3_project_setup.models import WatchList, StreamPlatform, Review
from chapter16_testing.api import serializers

User = get_user_model()

class WatchListViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = WatchList.objects.all()
    serializer_class = serializers.WatchListModelSerializer
    
class StreamPlatformViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = StreamPlatform.objects.all()
    serializer_class = serializers.StreamPlatformModelSerializer
    
class ReviewViewSet(viewsets.ModelViewSet):
    http_method_names = ["get", "post", "delete"]
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Review.objects.all()
    serializer_class = serializers.ReviewModelSerializer
    
