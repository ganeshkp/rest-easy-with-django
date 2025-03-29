from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views


router = DefaultRouter()
# Using ViewSet
# router.register(r"watchlist-caching", views.WatchlistCachingView, basename="watchlist-caching")

urlpatterns = [
    path('reviews/', views.ReviewsListCurrentUserFilterView.as_view(), name='reviews-current-user'),
    path('watchlist/<int:watchlist_id>/reviews/', views.ReviewListUrlFilterView.as_view(), name='reviews-url-filter'),
    path('watchlists/<int:watchlist_id>/reviews/', views.ReviewsUrlFilterWithValidationView.as_view(), name='reviews-url-filter-with-validation'),
    path('reviews-query-params/', views.ReviewsFilterQueryParamsView.as_view(), name='reviews-query-params'),
    path('reviews-generic-filter/', views.ReviewsGenericFilteringView.as_view(), name='reviews-generics-filter'),
    path('reviews-overriding-queryset-filter/', views.ReviewsGenericFilteringView.as_view(), name='reviews-overriding-queryset-filter'),
    path('watchlist-search-filter/', views.WatchlistSearchFilterView.as_view(), name='watchlist-search-filter'),
    path('watchlist-advanced-search/', views.WatchlistAdvacedSearchView.as_view(), name='watchlist-advanced-search'),
    path('watchlist-dynamic-search-field/', views.WatchlistDynamicSearchFieldView.as_view(), name='watchlist-dynamic-search-field'),
    path('watchlist-ordering/', views.WatchListOrderingView.as_view(), name='watchlist-ordering'),
    path('watchlist-full-ordering/', views.WatchListFullOrderingView.as_view(), name='watchlist-full-ordering'),
    path('watchlist-ordered/', views.WatchlistOrderedView.as_view(), name='watchlist-ordered'),
    path('user-review-list/', views.UserReviewListView.as_view(), name='user-review-list'),
    path('watchlist-category-filter/', views.WatchlistCategoryFilterView.as_view(), name='watchlist-category-filter'),
    
    # Using ViewSet
    path("", include(router.urls)),   
]

