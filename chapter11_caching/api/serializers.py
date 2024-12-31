from rest_framework import serializers
from django.contrib.auth import get_user_model
from chapter3_project_setup.models import WatchList

User = get_user_model()

class WatchListModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = WatchList
        fields = "__all__"        
                  