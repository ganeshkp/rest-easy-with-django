from rest_framework import serializers
from chapter3_project_setup.models import WatchList

class WatchListModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = WatchList
        fields = "__all__"     
        ref_name = 'C11WatchListModelSerializer'   
                  