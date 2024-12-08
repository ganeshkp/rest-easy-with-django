from rest_framework.pagination import (PageNumberPagination, 
                                       LimitOffsetPagination, 
                                       CursorPagination,
                                       BasePagination)
from rest_framework.response import Response
from collections import OrderedDict

class WatchListPageNumberPagination(PageNumberPagination):
    page_size = 5  # Default number of items per page.
    page_query_param = 'p'  # Change query parameter for the page to 'p'.
    page_size_query_param = 'page_size'  # Allow clients to request custom page sizes.
    max_page_size = 20  # Prevent excessively large page sizes.
    last_page_strings = ('end',)  # Clients can use 'end' to access the last page.
    template = None  # Disable HTML pagination controls in the browsable API.
    
class CustomLimitOffsetPagination(LimitOffsetPagination):    
    default_limit = 5  # Default limit if the client does not specify a limit parameter
    max_limit = 20  # Maximum limit that a client can request
    limit_query_param = 'custom_limit'  # Custom query parameter name for limit
    offset_query_param = 'custom_offset'  # Custom query parameter name for offset
    last_page_strings = ('end', 'final')  # Custom string values to request the last page
    template = None  # Disable HTML pagination controls in the browsable API.
    
class CustomCursorPagination(CursorPagination):
    page_size = 5  # Display 5 items per page
    cursor_query_param = 'watchlist_cursor'  # Use 'watchlist_cursor' in query params
    ordering = '-created'  # Order by the `created` field (most recent first)
    template = None  # Disable HTML pagination controls in the browsable API 
    
class CustomBasePagination(BasePagination):
    """
    Custom pagination class to implement a unique pagination style.
    """
    page_size = 5  # Default number of items per page

    def paginate_queryset(self, queryset, request, view=None):
        """
        Slice the queryset based on custom pagination logic.
        """
        self.page_size = int(request.query_params.get('page_size', self.page_size))  # Allow dynamic page size
        self.page_number = int(request.query_params.get('page', 1))  # Get the current page number
        self.start_index = (self.page_number - 1) * self.page_size  # Calculate the starting index
        self.end_index = self.start_index + self.page_size  # Calculate the ending index

        # Slice the queryset for the current page
        self.total_items = len(queryset)
        if self.start_index >= self.total_items:
            return []

        return queryset[self.start_index:self.end_index]

    def get_paginated_response(self, data):
        """
        Return a custom response structure for the paginated data.
        """
        return Response({
            'meta': {
                'current_page': self.page_number,
                'page_size': self.page_size,
                'total_items': self.total_items,
                'total_pages': (self.total_items + self.page_size - 1) // self.page_size,  # Calculate total pages
            },
            'data': data  # Paginated results
        })
        
class CustomPNPagination(PageNumberPagination):
    """
    Custom pagination style with 'next' and 'previous' links nested inside a 'links' key.
    """
    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('links', {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            }),
            ('count', self.page.paginator.count),
            ('page_size', self.page_size),
            ('results', data),
        ]))