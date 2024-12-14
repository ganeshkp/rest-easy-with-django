from rest_framework import viewsets
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.versioning import (URLPathVersioning, 
                                       NamespaceVersioning,
                                       QueryParameterVersioning, 
                                       AcceptHeaderVersioning)
from chapter3_project_setup.models import WatchList
from chapter15_versioning.api import serializers
from chapter15_versioning.api.versioning import XAPIVersionScheme

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
    
class WatchListQueryParameterVersioningViewSet(viewsets.ModelViewSet):
    queryset = WatchList.objects.all()
    serializer_class = serializers.WatchListModelSerializer
    versioning_class = QueryParameterVersioning
    
    def get_serializer_class(self):
        if self.request.version == '1.0':
            return serializers.WatchListModelSerializer  # Define this serializer for v1
        return serializers.WatchListEnhancedSerializer  # Define this serializer for v2
    
class WatchListAcceptHeaderVersioningViewSet(viewsets.ModelViewSet):
    queryset = WatchList.objects.all()
    serializer_class = serializers.WatchListModelSerializer
    versioning_class = AcceptHeaderVersioning
    
    def get_serializer_class(self):
        if self.request.version == '1.0':
            return serializers.WatchListModelSerializer  # Define this serializer for 1.0
        return serializers.WatchListEnhancedSerializer  # Define this serializer for 2.0 or other versions
    
class WatchListCustomVersioningViewSet(viewsets.ModelViewSet):
    queryset = WatchList.objects.all()
    versioning_class = XAPIVersionScheme  # Use the custom versioning class

    def get_serializer_class(self):
        # Check the requested version and return the appropriate serializer
        if self.request.version == '1.0':
            return serializers.WatchListModelSerializer  # Basic serializer for version 1.0
        elif self.request.version == '2.0':
            return serializers.WatchListEnhancedSerializer  # Enhanced serializer for version 2.0
        return serializers.WatchListModelSerializer  # Default serializer if no version is provided

    def list(self, request, *args, **kwargs):
        # Example response includes a reverse URL for demonstration
        example_url = reverse('watchlist-custom-list', request=request)
        return Response({
            "version": request.version,
            "example_url": example_url,
            "data": super().list(request, *args, **kwargs).data
        })
    
    
