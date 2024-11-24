from django.utils.safestring import mark_safe
from rest_framework.filters import BaseFilterBackend

class IsReviewOwnerFilterBackend(BaseFilterBackend):
    """
    Filter that only allows users to see their own reviews.
    """
    def filter_queryset(self, request, queryset, view):
        return queryset.filter(review_user=request.user)

class WatchlistCategoryFilter(BaseFilterBackend):
    """
    Filter to allow filtering Watchlist objects by category.
    Also includes a customized HTML interface for the browsable API.
    """
    def filter_queryset(self, request, queryset, view):
        category = request.query_params.get('category', None)
        if category:
            return queryset.filter(category=category)
        return queryset

    def to_html(self, request, queryset, view):
        # Get unique categories from the queryset
        categories = queryset.values_list('category', flat=True).distinct()
        # Generate dropdown HTML
        html = "<label for='category'>Category:</label>"
        html += "<select id='category' name='category'>"
        html += "<option value=''>All</option>"
        for category in categories:
            html += f"<option value='{category}'>{category}</option>"
        html += "</select>"
        return mark_safe(html)  # Mark the string as safe HTML