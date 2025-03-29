from django.core.cache import cache

class CacheMixin:
    cache_timeout = 60 * 15  # 15 minutes timeout

    def get_cached_response(self, cache_key, queryset):
        cached_data = cache.get(cache_key)
        if not cached_data:
            cached_data = queryset
            cache.set(cache_key, cached_data, timeout=self.cache_timeout)
        return cached_data
