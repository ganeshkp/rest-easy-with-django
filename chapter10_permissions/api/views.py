from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.authentication import BasicAuthentication, TokenAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly, DjangoModelPermissions, IsAdminUser
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.permissions import DjangoObjectPermissions
from rest_framework.viewsets import ModelViewSet
from django.contrib.auth import get_user_model
from guardian.shortcuts import assign_perm, get_perms
from chapter3_project_setup.models import WatchList, Review, StreamPlatform
from chapter10_permissions.api import serializers
from chapter10_permissions.api.permissions import IsReviewUserOrReadOnly, IsAdminOrReadOnly, MultiplePermissionsRequired

User = get_user_model()

#AllowAny
class WatchlistAllowAnyView(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication,]
    permission_classes = [AllowAny]  # Ensure that the user is authenticated
    queryset = WatchList.objects.all()
    serializer_class = serializers.WatchListModelSerializer

#IsAuthenticated
class WatchListIsAuthenticatedView(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication,]
    permission_classes = [IsAuthenticated,]  # Ensure that the user is authenticated
    queryset = WatchList.objects.all()
    serializer_class = serializers.WatchListModelSerializer
    
#IsAuthenticatedOrReadOnly
class WatchListIsAuthenticatedOrReadOnlyView(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication,]
    permission_classes = [IsAuthenticatedOrReadOnly,]
    queryset = WatchList.objects.all()
    serializer_class = serializers.WatchListModelSerializer    

#IsAdminUser
class WatchListIsAdminUserView(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication,]
    permission_classes = [IsAuthenticated, IsAdminUser]  # Ensure that the user is authenticated
    queryset = WatchList.objects.all()
    serializer_class = serializers.WatchListModelSerializer
    

#DjangoModelPermissions
class WatchListModelPermView(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication,]
    permission_classes = [DjangoModelPermissions]
    queryset = WatchList.objects.all()
    serializer_class = serializers.WatchListModelSerializer
    
#DjangoObjectPermissions   
class WatchListObjectPermissionsView(viewsets.ModelViewSet):
    queryset = WatchList.objects.all()
    serializer_class = serializers.WatchListModelSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [DjangoObjectPermissions,]  # Use DjangoObjectPermissions
    
    def perform_create(self, serializer): # new function
        instance = serializer.save()
        assign_perm("delete_watchlist", self.request.user, instance)
        assign_perm("change_watchlist", self.request.user, instance)
    
    
    
#added view level permissions
class WatchListMultiplePermView(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication,]
    permission_classes = [MultiplePermissionsRequired,]
    permissions = {
        "get": ("chapter3_project_setup.can_view_watchlist",),
        "post": ("chapter3_project_setup.can_create_watchlist",),
        "put": ("chapter3_project_setup.can_update_watchlist",),
        "patch": ("chapter3_project_setup.can_partially_update_watchlist",),
        "delete": ("chapter3_project_setup.can_delete_watchlist",),
    }
    queryset = WatchList.objects.all()
    serializer_class = serializers.WatchListModelSerializer

    
# This view allows only admin users to create watchlist
#remaining users only can get list of movies.
class WatchListView1(APIView):
    permission_classes = [IsAdminOrReadOnly]

    def get(self, request):
        movies = WatchList.objects.all()
        serializer = serializers.WatchListModelSerializer(movies, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = serializers.WatchListModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
    
    
# Function based view with basic authentication
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([BasicAuthentication])
def stream_platform_view1(request):
    if request.method == 'GET':
        # Handle GET request
        watchlist = StreamPlatform.objects.all()
        serializer = serializers.StreamPlatformModelSerializer(watchlist, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        # Handle POST request
        serializer = serializers.StreamPlatformModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Gets all review lists for authenticated users   
class ReviewList1(generics.ListAPIView):
    serializer_class = serializers.ReviewModelSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        pk = self.kwargs['pk']
        return Review.objects.filter(watchlist=pk)
        
# This view prevents user from update/delete operations 
# for non review users 
class ReviewDetail1(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = serializers.ReviewModelSerializer
    permission_classes = [IsReviewUserOrReadOnly]
    


            
    
