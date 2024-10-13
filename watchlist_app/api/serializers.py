from rest_framework import serializers
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth import get_user_model
from chapter3_project_setup.models import WatchList, StreamPlatform, Review
from watchlist_app.api import fields

User = get_user_model()

class StreamPlatformSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=30)
    about = serializers.CharField(max_length=150)
    website = serializers.URLField(max_length=100)

class WatchlistSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=30)
    storyline = serializers.CharField(max_length=200)
    active = serializers.BooleanField()
    # platform = StreamPlatformSerializer()
    # platform = serializers.StringRelatedField()
    # platform = serializers.HyperlinkedRelatedField(view_name='streamplatform-detail-cbv-try1', read_only=True)
    # platform = serializers.HyperlinkedIdentityField(view_name='streamplatform-detail-cbv-try1', read_only=True)
    platform = serializers.SlugRelatedField(slug_field="name", queryset=StreamPlatform.objects.all())
    imdb_rating = serializers.FloatField(default=0)
    created = serializers.DateTimeField()
    episodes = serializers.IntegerField(default=0)
    category = serializers.CharField(max_length=30) 
    
    def create(self, validated_data):
        return WatchList.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        """
        Update and return an existing `Watchlist` instance, given the validated data.
        """
        instance.title = validated_data.get('title', instance.title)
        instance.storyline = validated_data.get('storyline', instance.storyline)
        instance.active = validated_data.get('active', instance.active)
        instance.platform = validated_data.get('platform', instance.platform)
        instance.imdb_rating = validated_data.get('imdb_rating', instance.imdb_rating)
        instance.created = validated_data.get('created', instance.created)
        instance.episodes = validated_data.get('episodes', instance.episodes)
        instance.category = validated_data.get('category', instance.category)
        instance.save()
        return instance
    
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
    
class ReviewSerializer(serializers.Serializer):
    review_user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all()
    )
    rating = serializers.IntegerField()
    description = serializers.CharField(max_length=200)
    watchlist = WatchlistSerializer()
    active = serializers.BooleanField()
    created = serializers.DateTimeField()
    update = serializers.DateTimeField()
    
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
        
#############################HyperlinkedModelSerializer#########################

class WatchListHyperlinkedModelSerializer(serializers.HyperlinkedModelSerializer):
   
    class Meta:
        model = WatchList
        fields = "__all__"
        read_only_fields = ['full_title']
        extra_kwargs = {
            'imdb_rating': {'validators':[MinValueValidator(1.0), MaxValueValidator(5.0)]},
            'platform': {'view_name':'streamplatform-detail-cbv-try3'},
            'url': {'view_name': 'watchlist-detail-cbv-try3', 'lookup_field': 'pk'},         
        }
        
    
    
class StreamPlatformHyperlinkedModelSerializer(serializers.HyperlinkedModelSerializer):
    watchlist = WatchListHyperlinkedModelSerializer(many=True, read_only=True)

    class Meta:
        model = StreamPlatform
        fields = "__all__"
        depth = 1
        extra_kwargs = {
            'about':{'allow_null':True, 'default':""},
            'website':{'required': False},
            'url':{'view_name':'streamplatform-detail-cbv-try3', 'lookup_field':'pk'}            
        }

##################################ListSerializer##########################

class CustomWatchlistListSerializer(serializers.ListSerializer):
    update_data=[]
    
    def create(self, validated_data):
        # You can do some validation here before making bulk create
        watchlist = [WatchList(**item) for item in validated_data]
        result = WatchList.objects.bulk_create(watchlist)
        self.create_or_update(self.instance, validated_data)
        return result
    
    def create_or_update(self, instance, validated_data):
        # Maps for id->instance and id->data item.
        watchlist_mapping = {watchlist.id: watchlist for watchlist in instance}
        data_mapping = {item['id']: item for item in validated_data}

        # Perform creations and updates.
        ret = []
        for watchlist_id, data in data_mapping.items():
            watchlist = watchlist_mapping.get(watchlist_id, None)
            if watchlist is None:
                ret.append(self.child.create(data))
            else:
                ret.append(self.child.update(watchlist, data))

        # Perform deletions.
        for watchlist_id, watchlist in watchlist_mapping.items():
            if watchlist_id not in data_mapping:
                watchlist.delete()

        return ret

    
    def validate(self, attrs):
        return super().validate(attrs)
    
    
    
class WatchlistDemoListSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    
    class Meta:
        model = WatchList
        fields = "__all__"
        extra_kwargs = {
            'imdb_rating': {'validators':[MinValueValidator(1.0), MaxValueValidator(5.0)]}
        }
        
        list_serializer_class = CustomWatchlistListSerializer
        
    def create(self, validated_data):
        instance = WatchList(**validated_data)
        
        if(isinstance(self._kwargs["data"], dict)):
            instance.save()
            
        return instance

##################################BaseSerializer##########################
class WatchlistBaseSerializer(serializers.BaseSerializer):
    def to_representation(self, instance):
        return {
            'title': instance.title,
            'platform': instance.platform.name,
            'category': instance.category,
        }
        
    def to_internal_value(self, data):
        instance_data = data["resource"]
        title = instance_data.get('title')
        storyline = instance_data.get('storyline')
        category = instance_data.get('category')
        imdb_rating = instance_data.get("imdb_rating")
        created = instance_data.get("created")
        platform = instance_data.get('platform')
        platform = StreamPlatform.objects.filter(name=platform).first()     

        # Perform the data validation.
        if not title:
            raise serializers.ValidationError({
                'title': 'This field is required.'
            })
        if not category:
            raise serializers.ValidationError({
                'category': 'This field is required.'
            })
        if len(title) > 50:
            raise serializers.ValidationError({
                'title': 'May not be more than 50 characters.'
            })
            
        if not platform:
            raise serializers.ValidationError({
                'platform': 'Valid platform name is required.'
            })

        # Return the validated values. This will be available as
        # the `.validated_data` property.
        return {
            'title': title,
            'category': category,
            'platform': platform,
            'storyline': storyline,
            'imdb_rating': imdb_rating,
            'created': created
        }

    def create(self, validated_data):
        return WatchList.objects.create(**validated_data)

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