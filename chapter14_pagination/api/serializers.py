from rest_framework import serializers
from chapter3_project_setup.models import WatchList, StreamPlatform, Review

class WatchListModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = WatchList
        fields = "__all__"  
        ref_name = 'C14WatchListModelSerializer'       
           
    
class StreamPlatformModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = StreamPlatform
        fields = "__all__"
        ref_name = 'C14StreamPlatformModelSerializer'   

class ReviewModelSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    class Meta:
        model = Review
        fields = "__all__"
        ref_name = 'C14ReviewModelSerializer'    
              