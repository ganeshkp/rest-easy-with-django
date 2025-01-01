from rest_framework import serializers
from django.contrib.auth import get_user_model
from chapter3_project_setup.models import WatchList, StreamPlatform, Review


#############################ModelSerializer#########################

class WatchlistModelBasicSerializer(serializers.ModelSerializer):
    platform = serializers.StringRelatedField()
    
    class Meta:
        model=WatchList
        fields = ["title", "platform", "imdb_rating", "created"]

class WatchListModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = WatchList
        fields = "__all__"  
        ref_name = 'C7WatchListModelSerializer'

    
class StreamPlatformModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = StreamPlatform
        fields = "__all__"
        ref_name = 'C7StreamPlatformModelSerializer'

class ReviewModelSerializer(serializers.ModelSerializer):
    review_user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Review
        fields = "__all__"
        ref_name = 'C7ReviewModelSerializer'

################ Create HyperLinkedModelSerializer to use it for ModelViewSet##############
class WatchListHyperlinkedModelSerializer(serializers.HyperlinkedModelSerializer):
   
    class Meta:
        model = WatchList
        fields = "__all__"
        read_only_fields = ['full_title']
        extra_kwargs = {
            'platform': {'view_name':'instance_name:streamplatform-hlms-viewset-detail'},
            'url': {'view_name': 'instance_name:watchlist-hlms-viewset-detail', 'lookup_field': 'pk'},         
        }
        
class StreamPlatformHyperlinkedModelSerializer(serializers.HyperlinkedModelSerializer):
    watchlist = WatchListHyperlinkedModelSerializer(many=True, read_only=True)

    class Meta:
        model = StreamPlatform
        fields = "__all__"
        extra_kwargs = {
            'url':{'view_name':'instance_name:streamplatform-hlms-viewset-detail', 'lookup_field':'pk'}            
        }