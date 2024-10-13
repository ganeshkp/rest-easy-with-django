from rest_framework import serializers
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth import get_user_model
from chapter3_project_setup.models import WatchList, StreamPlatform, Review
from watchlist_app.api import fields

User = get_user_model()


#############################ModelSerializer#########################

class WatchlistModelBasicSerializer(serializers.ModelSerializer):
    platform = serializers.StringRelatedField()
    
    class Meta:
        model=WatchList
        fields = ["title", "platform", "imdb_rating", "created"]

class WatchListModelSerializer(serializers.ModelSerializer):
    full_title = serializers.SerializerMethodField()
    user = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())
    
    # created = CustomDateTimeSerializerField()    
    # serializer_field_mapping = {
    #     models.DateTimeField: CustomDateTimeField,
    # }
    serializer_related_field = fields.CustomPrimaryKeyRelatedField
    # platform = serializers.HyperlinkedRelatedField(view_name='streamplatform-detail-cbv-try2', read_only=True)
    # serializer_url_field = fields.CustomHyperlinkedRelatedField
    serializer_choice_field = fields.CustomChoiceField
    
    class Meta:
        model = WatchList
        fields = "__all__"
        # fields = ["title", "storyline", "platform"]
        read_only_fields = ['full_title']
        extra_kwargs = {
            'imdb_rating': {'validators':[MinValueValidator(1.0), MaxValueValidator(5.0)]}
        }
        
        
    def get_full_title(self, obj):
        return obj.full_title
        
    def validate_title(self, value):
        if "@" in value:
            serializers.ValidationError("Invalid Title")
        return value
    
    def validate_storyline(self, value):
        if "@" in value:
            serializers.ValidationError("Invalid Storyline")
        return value
    
    def validate_category(self, value):
        if value not in ["MOVIE", "SERIES"]:
            serializers.ValidationError("Not a valid category")
        return value
    
    def validate_platform(self, value):
        return value
    
    def validate(self, data):
        title = data.get("title", None)
        storyline = data.get("storyline", None)
        if (title and storyline) and (len(title) > len(storyline)):
            raise serializers.ValidationError("Length of title is bigger than storyline")
        return super().validate(data)
    
class StreamPlatformModelSerializer(serializers.ModelSerializer):
    watchlist = WatchListModelSerializer(many=True, read_only=True)
    serializer_url_field = fields.CustomHyperlinkedRelatedField

    class Meta:
        model = StreamPlatform
        fields = "__all__"
        depth = 1
        extra_kwargs = {
            'about':{'allow_null':True, 'default':""},
            'website':{'required': False}
        }

class ReviewModelSerializer(serializers.ModelSerializer):
    review_user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Review
        exclude = ('watchlist',)
        # fields = "__all__"

################ Create HyperLinkedModelSerializer to use it for ModelViewSet##############
class WatchListHyperlinkedModelSerializer1(serializers.HyperlinkedModelSerializer):
   
    class Meta:
        model = WatchList
        fields = "__all__"
        read_only_fields = ['full_title']
        extra_kwargs = {
            'platform': {'view_name':'instance_name:streamplatform-viewset5-detail'},
            'url': {'view_name': 'instance_name:watchlist-viewset5-detail', 'lookup_field': 'pk'},         
        }
        
class StreamPlatformHyperlinkedModelSerializer1(serializers.HyperlinkedModelSerializer):
    watchlist = WatchListHyperlinkedModelSerializer1(many=True, read_only=True)

    class Meta:
        model = StreamPlatform
        fields = "__all__"
        extra_kwargs = {
            'url':{'view_name':'instance_name:streamplatform-viewset5-detail', 'lookup_field':'pk'}            
        }