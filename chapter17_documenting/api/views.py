from rest_framework import viewsets
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from drf_spectacular.types import OpenApiTypes

from chapter3_project_setup.models import WatchList
from chapter17_documenting.api import serializers


class WatchListViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for managing the WatchList.
    """
    queryset = WatchList.objects.all()
    serializer_class = serializers.WatchListModelSerializer

    @extend_schema(
        request=serializers.WatchListModelSerializer,
        responses={201: serializers.WatchListModelSerializer},
        description="Create a new WatchList item.",
        examples=[
            OpenApiExample(
                "Create Example",
                summary="Sample WatchList Creation Request",
                description="A sample request to create a new watchlist item.",
                value={
                    "title": "Example Movie",
                    "storyline": "A brief storyline of the movie.",
                    "active": True,
                    "imdb_rating": 7.5,
                    "platform": 1,
                    "category": "MOVIE"
                }
            )
        ]
    )
    def create(self, request):
        """
        Create a new watchlist item with custom behavior.
        """
        return super().create(request)

    @extend_schema(
        parameters=[
            OpenApiParameter(name='platform', description='Filter by platform ID', required=False, type=OpenApiTypes.INT),
            OpenApiParameter(
                name='imdb_rating_min',
                type=OpenApiTypes.NUMBER,
                location=OpenApiParameter.QUERY,
                description='Filter by minimum IMDb rating',
                examples=[
                    OpenApiExample(
                        'Example Rating Filter',
                        summary='Filtering example',
                        description='Filter items with IMDb rating >= 8.0.',
                        value=8.0
                    )
                ]
            )
        ],
        description="Retrieve a list of WatchList items, optionally filtered by platform or IMDb rating.",
        responses={
            200: serializers.WatchListModelSerializer(many=True),
            400: "Invalid query parameters."
        },
    )
    def list(self, request):
        """
        Custom list endpoint for WatchList.
        """
        return super().list(request)

    @extend_schema(
        request=None,
        responses={
            204: "Watchlist Item Deleted",
            404: "Watchlist Item not Found"
        },
        methods=["DELETE"],
        description="Delete a WatchList item by its ID."
    )
    def destroy(self, request, *args, **kwargs):
        """
        Custom destroy endpoint for WatchList.
        """
        return super().destroy(request, *args, **kwargs)