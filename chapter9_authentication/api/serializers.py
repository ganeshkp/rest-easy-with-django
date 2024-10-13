from rest_framework import serializers
from django.contrib.auth import get_user_model
from chapter3_project_setup.models import WatchList, StreamPlatform, Review


User = get_user_model()

class WatchListModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = WatchList
        fields = "__all__"        
    
class StreamPlatformModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = StreamPlatform
        fields = "__all__"

class ReviewModelSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    class Meta:
        model = Review
        fields = "__all__"
              