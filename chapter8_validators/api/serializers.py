from rest_framework import serializers
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from chapter3_project_setup.models import WatchList, StreamPlatform, Review
from rest_framework.validators import ( UniqueValidator, 
                                        UniqueTogetherValidator,
                                        UniqueForDateValidator,
                                    )
from chapter8_validators.api import validators

class WatchListModelSerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=50, validators=[UniqueValidator(queryset=WatchList.objects.all()), validators.validate_watchlist_title])
    
    class Meta:
        model = WatchList
        fields = "__all__"
        extra_kwargs = {
            'imdb_rating': {'validators':[MinValueValidator(1.0), MaxValueValidator(10.0)]}
        }
        validators = [validators.validate_watchlist_type,
                      validators.CreateRequiredTogetherValidator(
                          fields=("title", "category", "episodes"),
                          message= _("This field is required."),
                          missing_message=_("This field is required.")
                      )
                    ]
        ref_name = 'C8WatchListModelSerializer'
        
    
class StreamPlatformModelSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=30, validators=[UniqueValidator(queryset=StreamPlatform.objects.all())])

    class Meta:
        model = StreamPlatform
        fields = "__all__"
        validators = [
            UniqueTogetherValidator(
                queryset=StreamPlatform.objects.all(),
                fields=['name', 'website']
            )
        ]
        ref_name = 'C8StreamPlatformModelSerializer'

class ReviewModelSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
            default=serializers.CurrentUserDefault()
        )

    class Meta:
        model = Review
        fields = "__all__"
        validators = [
            UniqueTogetherValidator(
                queryset=Review.objects.all(),
                fields=['review_user', 'watchlist']
            ),
            UniqueForDateValidator(
                queryset=Review.objects.all(),
                field='rating',
                date_field='review_date'
            )
        ]
        ref_name = 'C8ReviewModelSerializer'