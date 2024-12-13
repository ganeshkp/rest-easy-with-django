from rest_framework import viewsets
from django.contrib.auth import get_user_model
from rest_framework.versioning import URLPathVersioning, NamespaceVersioning
from chapter3_project_setup.models import WatchList
from chapter15_versioning.api import serializers

User = get_user_model()

class WatchListUrlPathVersioningViewSet(viewsets.ModelViewSet):
    queryset = WatchList.objects.all()
    serializer_class = serializers.WatchListModelSerializer
    versioning_class = URLPathVersioning
    
    def get_serializer_class(self):
        if self.request.version == 'v1':
            return serializers.WatchListModelSerializer  # Define this serializer for v1
        return serializers.WatchListEnhancedSerializer  # Define this serializer for v2


class WatchListNamespaceVersioningViewSet(viewsets.ModelViewSet):
    queryset = WatchList.objects.all()
    serializer_class = serializers.WatchListModelSerializer
    versioning_class = NamespaceVersioning
    
    def get_serializer_class(self):
        if self.request.version == 'v1':
            return serializers.WatchListModelSerializer  # Define this serializer for v1
        return serializers.WatchListEnhancedSerializer  # Define this serializer for v2
    
    
