
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from chapter3_project_setup.models import WatchList, Review, StreamPlatform
from chapter14_pagination.api import serializers
from chapter14_pagination.api.pagination import (WatchListPageNumberPagination, 
                                                 CustomLimitOffsetPagination,
                                                 CustomCursorPagination,
                                                 CustomBasePagination,
                                                 CustomPNPagination)


User = get_user_model()

class WatchListGlobalPageNumberPaginationViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]  # Ensure that the user is authenticated
    queryset = WatchList.objects.all()
    serializer_class = serializers.WatchListModelSerializer
    
#-----------------------------------------------------------------------------
class WatchListCustomPageNumberPaginationViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]  # Ensure that the user is authenticated
    queryset = WatchList.objects.all()
    serializer_class = serializers.WatchListModelSerializer
    pagination_class = WatchListPageNumberPagination
    
#-----------------------------------------------------------------------------
class WatchListLimitOffsetPaginationViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]  # Ensure authenticated access
    queryset = WatchList.objects.all()
    serializer_class = serializers.WatchListModelSerializer
    pagination_class = CustomLimitOffsetPagination  # Apply the custom pagination
    
#----------------------------------------------------------------------------------
class WatchListCursorPaginationViewSet(viewsets.ModelViewSet):
    queryset = WatchList.objects.all()
    serializer_class = serializers.WatchListModelSerializer
    pagination_class = CustomCursorPagination
    
#------------------------------------------------------------------------------
class WatchListCBPaginationViewSet(viewsets.ModelViewSet):
    queryset = WatchList.objects.all()
    serializer_class = serializers.WatchListModelSerializer
    pagination_class = CustomBasePagination
    
#------------------------------------------------------------------------------
class WatchListCPNPaginationViewSet(viewsets.ModelViewSet):
    queryset = WatchList.objects.all()
    serializer_class = serializers.WatchListModelSerializer
    pagination_class = CustomPNPagination