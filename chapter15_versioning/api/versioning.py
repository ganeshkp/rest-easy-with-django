from rest_framework.versioning import BaseVersioning

class XAPIVersionScheme(BaseVersioning):
    def determine_version(self, request, *args, **kwargs):
        # Extract the version from the custom header 'X-API-Version'
        return request.META.get('HTTP_X_API_VERSION', None)
    
    def reverse(self, viewname, args=None, kwargs=None, request=None, format=None):
        # Append version to the URL as a query parameter for demonstration
        url = super().reverse(viewname, args, kwargs, request, format)
        version = self.determine_version(request)
        if version:
            return f"{url}?version={version}"
        return url
