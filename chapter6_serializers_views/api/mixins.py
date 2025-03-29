from chapter3_project_setup.models import WatchList
from django.db.models import Sum
from rest_framework import generics

class MultipleFieldLookupMixin:
    """
    Apply this mixin to any view or viewset to get multiple field filtering
    based on a `lookup_fields` attribute, instead of the default single field filtering.
    """
    def get_object(self):
        queryset = self.get_queryset()             # Get the base queryset
        queryset = self.filter_queryset(queryset)  # Apply any filter backends
        filter = {}
        for field in self.lookup_fields:
            if self.kwargs.get(field): # Ignore empty fields.
                filter[field] = self.kwargs[field]
        obj = generics.get_object_or_404(queryset, **filter)  # Lookup the object
        self.check_object_permissions(self.request, obj)
        return obj

class TotalEpisodesMixin:
    """
    Custom mixin for WatchList model to count number of episodes
    """
    
    def calculate_total_episodes(self):
        """
        Calculate the total number of episodes across all watchlists.
        """
        total_episodes = WatchList.objects.aggregate(total_episodes=Sum('episodes'))
        return total_episodes['total_episodes']
    
