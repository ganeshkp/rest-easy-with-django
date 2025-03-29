from rest_framework.throttling import UserRateThrottle, BaseThrottle
from rest_framework.exceptions import Throttled
from django.core.cache import cache
import time
   
class CustomCacheRateThrottle(BaseThrottle):
    rate_limit = 5  # Maximum requests allowed
    window_duration = 60  # Time window in seconds (1 minute)

    def get_cache_key(self, request):
        # Identify user uniquely based on authentication status or IP address
        user_identifier = request.user.username if request.user.is_authenticated else request.META['REMOTE_ADDR']
        return f"throttle_{user_identifier}"

    def allow_request(self, request, view):
        cache_key = self.get_cache_key(request)
        current_time = time.time()

        # Get existing request timestamps list from cache
        request_history = cache.get(cache_key, [])

        # Filter out timestamps that are outside of the window duration
        request_history = [timestamp for timestamp in request_history if current_time - timestamp < self.window_duration]

        if len(request_history) >= self.rate_limit:
            # Deny request if rate limit is reached
            return False

        # Add current timestamp to request history
        request_history.append(current_time)
        # Save updated request history back to cache
        cache.set(cache_key, request_history, timeout=self.window_duration)
        return True
    
class ExceptionCustomMessageThrottle(UserRateThrottle):
    def throttle_failure(self):
        # Raise a Throttled exception with a custom detail message
        raise Throttled(detail="Custom message: You have exceeded your request limit. Please wait before retrying.")