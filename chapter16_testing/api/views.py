from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import status

from chapter3_project_setup.models import WatchList, StreamPlatform, Review
from chapter16_testing.api import serializers
from chapter16_testing.api import utils

class WatchListViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = WatchList.objects.all()
    serializer_class = serializers.WatchListModelSerializer
class StreamPlatformViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = StreamPlatform.objects.all()
    serializer_class = serializers.StreamPlatformModelSerializer
class ReviewViewSet(viewsets.ModelViewSet):
    http_method_names = ["get", "post", "delete"]
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Review.objects.all()
    serializer_class = serializers.ReviewModelSerializer


class WatchlistExternalView(APIView):
    """
    API view to handle watchlist data and user-specific recommendations.
    """

    def get(self, request):
        """
        Handle GET requests to return watchlist data and recommendations.
        """
        try:
            watchlist_data = utils.fetch_watchlist_data()  # External function 1
            user_recommendations = utils.fetch_user_recommendations(request.user.id)  # External function 2

            response_data = {
                "watchlist": watchlist_data,
                "recommendations": user_recommendations
            }

            return Response(response_data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def post(self, request):
        """
        Handle POST requests to create a new watchlist item.
        """
        # Validate incoming data using external function
        if not utils.validate_external_watchlist_data(request.data):
            return Response({"error": "Invalid watchlist data"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = serializers.WatchListModelSerializer(data=request.data)
        if serializer.is_valid():
            watchlist_item = serializer.save()
            
            # Notify an external service after creation
            notification_response = utils.notify_external_service(watchlist_item)
            return Response({
                "watchlist_item": serializer.data,
                "notification": notification_response
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
